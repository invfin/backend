BLACK_FOLDERS=apps
MYPY_FOLDERS=apps

.PHONY: requirements


build:
	docker-compose -f local.yml build $(ar)

clean-build:
	docker-compose -f local.yml build --no-cache $(ar)

reboot:
	$(MAKE) stop && $(MAKE) up-b

clean-start:
	make requirements
	docker-compose -f local.yml build invfin
	make up-b

restart:
	docker-compose -f local.yml restart $(ar)

up-b:
	docker-compose -f local.yml up -d invfin
	docker-compose -f local.yml logs -f invfin

up:
	docker-compose -f local.yml up $(ar)

buildsemi:
	docker-compose -f semiprod.yml build

upsemi:
	docker-compose -f semiprod.yml up nginx invfin

stop:
	docker-compose -f local.yml stop

shell:
	docker-compose -f local.yml exec invfin /bin/bash

# Django
up-d:
	docker-compose -f local.yml up invfin

dbshell:
	docker-compose -f local.yml run --rm invfin python -u manage.py dbshell --settings=config.settings.final

log:
	docker-compose -f local.yml logs -f invfin

migrations:
	docker-compose -f local.yml run --rm invfin python -u manage.py makemigrations $(ar) --settings=config.settings.final

migrate:
	docker-compose -f local.yml run --rm invfin python -u manage.py migrate $(ar) --settings=config.settings.final

allmig:
	docker-compose -f local.yml run --rm invfin python -u manage.py makemigrations $(ar) --settings=config.settings.final
	docker-compose -f local.yml run --rm invfin python -u manage.py migrate $(ar) --settings=config.settings.final

shell_plus:
	docker-compose -f local.yml run --rm invfin ./manage.py shell_plus --settings=config.settings.final

manage:
	docker-compose -f local.yml run --rm invfin ./manage.py $(ar) --settings=config.settings.final

collectstatic:
	docker-compose -f local.yml run --rm invfin ./manage.py collectstatic --noinput --settings=config.settings.final
	make build ar="invfin"

col-share-static:
	docker-compose -f local.yml run --rm invfin ./manage.py collectstatic --noinput --settings=config.settings.final
	docker-compose -f local.yml build

run:
	docker-compose -f local.yml run --rm invfin $(ar)

pip:
	docker exec -ti invfin_local_invfin pip install $(ar)

pdb:
	docker-compose -f local.yml stop invfin
	docker-compose -f local.yml run --rm --service-ports invfin

pdb_manage:
	docker-compose -f local.yml stop invfin
	docker-compose -f local.yml run --rm --service-ports invfin  ./manage.py $(ar) --settings=config.settings.final

requirements:
	docker-compose -f local.yml run invfin /requirements.sh "temp_venv/bin/pip"
	docker-compose -f local.yml run invfin rm -rf temp_venv/

reset_migrations:
	docker-compose -f local.yml run --rm invfin /reset_migrations.sh

# Postgres
shell_db:
	docker-compose -f local.yml exec postgres /bin/sh

log-db:
	docker-compose -f local.yml logs db

backup:
	docker-compose -f local.yml exec postgres backup

ls_backups:
	docker-compose -f local.yml exec postgres backups

rt_backups:
	@echo ls -Art $PWD/backups/*.sql.gz | tail -n 1

restore:
	docker-compose -f local.yml stop
	docker-compose -f local.yml up -d postgres
	docker-compose -f local.yml exec postgres restore $(ar)

auto_restore:
	auto_backup_import

# Documentation
docs_check:
	docker-compose -f local.yml run --rm invfin ./manage.py generate_swagger --settings=config.settings.final

# Testing
new-test:
	docker-compose -f local.yml run --rm invfin python -u manage.py test $(ar) --noinput --settings=config.settings.test

test:
	docker-compose -f local.yml run --rm invfin python -u manage.py test $(ar) --noinput --keepdb --settings=config.settings.test

pytest:
	docker-compose -f local.yml run --rm invfin pytest

cov:
	docker-compose -f local.yml run --rm invfin coverage run --source='.' manage.py test $(ar) --noinput --settings=config.settings.test
	docker-compose -f local.yml run --rm invfin coverage report

pycov:
	docker-compose -f local.yml run --rm invfin coverage run -m pytest
	docker-compose -f local.yml run --rm invfin coverage report

# Style
format:
	docker-compose -f local.yml run invfin flake8 && isort . && black ${BLACK_FOLDERS}

flake8:
	docker-compose -f local.yml run --rm invfin make local/flake8

isort:
	docker-compose -f local.yml run --rm invfin make local/isort

black:
	docker-compose -f local.yml run --rm invfin local/black

mypy:
	docker-compose -f local.yml run --rm invfin local/mypy

local/flake8:
	flake8

local/isort:
	isort .

local/mypy:
	mypy ${MYPY_FOLDERS}

local/format: local/isort local/black local/flake8 local/djlint local/mypy

format:
	docker-compose -f local.yml run --rm invfin make local/format

isort_check:
	docker-compose -f local.yml run --rm invfin make local/isort_check

local/isort_check:
	isort --df -c .

local/black:
	black ${BLACK_FOLDERS}

black_check:
	docker-compose -f local.yml run --rm invfin black local/black_check

local/black_check:
	black ${BLACK_FOLDERS} --check