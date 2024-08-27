#!/bin/bash
# author: stephane
# usage . deploy_package.sh
set +x
#
#  usage : ./build_deploy_package.sh  --tagged 
#
#  construit la distribution nlptools et la pousse sur git
#
# options :
#
#  --tagged  = tag la version (git et setup avec le numero de version dans le fichier tag.txt
#
export TEST="$HOME/test"
export PYTHONPATH=""

# cf : https://docs.python.org/fr/3/install/index.html
# setup.py install construit et installe tous les modules en un seul coup.

# reconstruction de la distribution
echo "build distrib......................................................"
rm -rf dist terms_tools.egg-info build

# Construit la distribition binaire (fromat wheel)
python3 setup.py bdist_wheel
# En plus , installe en local everything from build directory (en local )
#python3 setup.py install --user

# push git
echo "---- PUSH distrib .........................................................."
git add .
git commit -m "maj package"
tag=$(cat tag.txt)
if [[ -n $1 ]]; then
  if [[ $1 = "--tagged" ]]; then
    echo "tag version with : $tag"
    git tag -d $tag  && git push --delete origin $tag
    git tag $tag &&  git push http://schneist:merlin@vxgit.intra.inist.fr:60000/git/schneist/terms_tools.git  $tag
  else
    echo "ERROR : $1 mauvaise option"
    exit 1
  fi

  if [[ -n $2 ]]; then
    # deploie en local via git
    if [[ $1 = "--deploy" ]]; then
        echo "---- DEPLOY ........................................................."
        pip3 uninstall -y terms_tools
        pip3 install --no-cache-dir git+http://vxgit.intra.inist.fr:60000/git/schneist/terms_tools.git@${tag}#egg=terms_tools

        # info se mettre en contexte execution avec le paquet installé
        echo "---- CONTROL DEPLOY ........................................................."
        pip3 show -v terms-tools
        unset PYTHONPATH

        echo "---- EXECUTION TEST (lib mode) ........................................................."
        cmd="cat test/data/not-fr.tsv| terms_tools POStagger -f text -o doc -log analyze.log -lang fr"
        eval $cmd
    fi

else
  git push http://schneist:merlin@vxgit.intra.inist.fr:60000/git/schneist/terms_tools.git --all
fi





