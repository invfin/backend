FOLDERS=src tests

.PHONY: requirements


build:
	docker compose -f local.yml build $(ar)

clean-build:
	docker compose -f local.yml build --no-cache $(ar)

reboot:
	$(MAKE) stop && $(MAKE) up-b

clean-start:
	make requirements
	docker compose -f local.yml build invfin
	make up-b

restart:
	docker compose -f local.yml restart $(ar)

up-b:
	docker compose -f local.yml up -d invfin
	docker compose -f local.yml logs -f invfin

up:
	docker compose -f local.yml up $(ar)

up-complements:
	docker compose -f local.yml up redis celeryworker mailhog celerybeat flower

changepassword:
	docker compose -f local.yml run --rm invfin ./manage.py changepassword $(ar)

admin-pass:
	docker compose -f local.yml run --rm invfin ./manage.py admin_pass

buildsemi:
	docker compose -f semiprod.yml build

upsemi:
	docker compose -f semiprod.yml up --build

stopsemi:
	docker compose -f local.yml stop

stop:
	docker compose -f local.yml stop

shell:
	docker compose -f local.yml exec invfin /bin/bash

# Django
up-d:
	docker compose -f local.yml up invfin

log:
	docker compose -f local.yml logs -f invfin

migrations:
	docker compose -f local.yml run --rm invfin python -u manage.py makemigrations $(ar)

migrate:
	docker compose -f local.yml run --rm invfin python -u manage.py migrate $(ar)

allmig:
	docker compose -f local.yml run --rm invfin python -u manage.py makemigrations $(ar)
	docker compose -f local.yml run --rm invfin python -u manage.py migrate $(ar)

manage:
	docker compose -f local.yml run --rm invfin ./manage.py $(ar)

collectstatic:
	docker compose -f local.yml run --rm invfin ./manage.py collectstatic --noinput
	make build ar="invfin"

col-share-static:
	docker compose -f local.yml run --rm invfin ./manage.py collectstatic --noinput
	docker compose -f local.yml build

run:
	docker compose -f local.yml run --rm invfin $(ar)

pip:
	docker exec -ti invfin_local_invfin pip install $(ar)

requirements:
	docker compose -f local.yml run invfin /requirements.sh "temp_venv/bin/pip"
	docker compose -f local.yml run invfin rm -rf temp_venv/

reset_migrations:
	docker compose -f local.yml run --rm invfin /reset_migrations.sh

# Postgres
shell_db:
	docker compose -f local.yml exec postgres /bin/sh

log-db:
	docker compose -f local.yml logs db

backup:
	docker compose -f local.yml exec postgres backup

ls_backups:
	docker compose -f local.yml exec postgres backups

rt_backups:
	@echo ls -Art $PWD/backups/*.sql.gz | tail -n 1

restore:
	docker compose -f local.yml stop
	docker compose -f local.yml up -d postgres
	docker compose -f local.yml exec postgres restore $(ar)

# Documentation
docs_check:
	docker compose -f local.yml run --rm invfin ./manage.py generate_swagger

# Testing
new-test:
	docker compose -f local.yml run --rm invfin python -u manage.py test $(ar) --noinput --settings=config.settings.test

test:
	docker compose -f local.yml run --rm invfin python -u manage.py test $(ar) --noinput --keepdb --settings=config.settings.test

pytest:
	docker compose -f local.yml run --rm invfin pytest

cov:
	docker compose -f local.yml run --rm invfin coverage run --source='.' manage.py test $(ar) --noinput --settings=config.settings.test
	docker compose -f local.yml run --rm invfin coverage report

pycov:
	docker compose -f local.yml run --rm invfin coverage run -m pytest
	docker compose -f local.yml run --rm invfin coverage report

# Style
format:
	isort ${FOLDERS} 
	black ${FOLDERS} 
	flake8 ${FOLDERS}
	mypy ${FOLDERS}

isort_check:
	isort --df -c ${FOLDERS}

black_check:
	black ${FOLDERS} --check

flake8:
	flake8 ${FOLDERS}

isort:
	isort ${FOLDERS}

black:
	black ${FOLDERS}

mypy:
	mypy ${FOLDERS}

deploy:
	./deployment.sh ${ar} ${str}