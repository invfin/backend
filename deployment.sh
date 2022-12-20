#!/bin/bash
function git_save_everywhere(){
	git add .
	git commit -m "$1"
	for remote in $(git remote)
	do
		git push "$remote" "master"
	done
}

function run_ssh_command(){
    ssh webserver bash -s $1 <<'EOF'
	cd $HOME/invfin/invfin
	source ../bin/activate
	git pull
	python3 manage.py migrate
	sudo supervisorctl restart $1
	exit
EOF
}

find_in_conda_env(){
    conda env list | grep "${@}" >/dev/null 2>/dev/null
}


COMMIT_MESSAGE="${1:-.}"
SERVICES_TO_RESTART="${2:-all}"
TEST_FOLDER="$PWD"/tests
CODE_FOLDER="$PWD"/src

if find_in_conda_env ".*RUN_ENV.*" ; then
   conda init invfin
fi


isort $CODE_FOLDER
black $CODE_FOLDER

pytest $TEST_FOLDER -x --disable-pytest-warnings -n auto -vv
pytest_result=$?

if [ "$pytest_result" == "0" ]; then
    echo "Ha pasado pytest"
    echo "****************************************************"
    mypy $CODE_FOLDER
    mypy_result=$?
    mypy_result="0"
    if [ "$mypy_result" == "0" ]; then
        echo "Ha pasado mypy"
        echo "****************************************************"
        flake8 $CODE_FOLDER
        flake8_result=$?
        flake8_result="0"
        if [ "$flake8_result" == "0" ]; then
            echo "Ha pasado flake8"
            echo "****************************************************"
            git_save_everywhere "$COMMIT_MESSAGE";
			run_ssh_command "$SERVICES_TO_RESTART";
        elif [ "$flake8_result" == "1" ]; then
            echo "Ha fallado flake8"
        fi
    elif [ "$mypy_result" == "1" ]; then
        echo "Ha fallado mypy"
    fi
elif [ "$pytest_result" == "1" ]; then
    echo "Ha fallado pytest"
fi