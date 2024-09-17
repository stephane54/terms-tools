#!/bin/bash
# author: stephane
# usage . deploy_package.sh
set +x
#
#  usage : ./build_deploy_package.sh  --deploy 
#
#  construit la distribution nlptools et la pousse sur git
#
#  options :
#			  --deploy :  install le package  en local
#
export TEST="$HOME/test"
export PYTHONPATH=""
#export GIT="http://schneist:merlin@vxgit.intra.inist.fr:60000/git/schneist/terms_tools.git"
export GIT_SSH="git@github.com:stephane54/terms-tools.git"
export GIT_HTTP="https://github.com/stephane54/terms-tools.git"


# cf : https://docs.python.org/fr/3/install/index.html
# setup.py install construit et installe tous les modules en un seul coup.

build () {
# reconstruction de la distribution
echo "build distrib......................................................"
rm -rf dist terms_tools.egg-info build
TT_HOME=/home/schneist/app/terms_tools
    # Construit la distribution binaire (format wheel)
    python3 setup.py bdist_wheel
    # En plus , install in local everything from build directory (en local)
    #python3 setup.py install --user

    # push git
    echo "---- PUSH distrib .........................................................."
    git add .
    git commit -m "maj package"
    tag=$(cat tag.txt)
    echo "tag version with : $tag"
    git tag -d $tag  && git push --delete origin $tag
    git tag $tag 
    git push -u ${GIT_SSH} $tag
}

deploy () 
{
# deploie en local via git
    if [ -n "$1" ]; then

        if [ "$1" = "--deploy" ]; then
                echo "---- DEPLOY ........................................................."
                pip3 uninstall -y terms_tools
                pip3 install --no-cache-dir git+${GIT_HTTP}@${tag}#egg=terms_tools

                # info se mettre en contexte execution avec le paquet installé
                echo "---- CONTROL DEPLOY ........................................................."
                pip3 show -v terms-tools
                unset PYTHONPATH

                echo "---- EXECUTION TEST (lib mode) ........................................................."
                cmd="cat  $TT_HOME/terms_tools/test/data/not-fr.tsv| terms_tools POStagger -f text -o doc -log analyze.log -lang fr"
                echo $cmd
                eval $cmd
                echo "---- EXECUTION TEST in EZS (lib mode) ........................................................."
                cmd="ezs -p input=terms  $TT_HOME/web-service/terms-tools/v1/fr/full_morph/postag.ini   < $TT_HOME/terms_tools/test/data/test_labelFR.tsv"
                echo $cmd
                eval $cmd
                exit 0
        else
                echo "ERROR : $1 mauvaise option"
                exit 1
        fi

    fi
}


build  && deploy

exit 0






