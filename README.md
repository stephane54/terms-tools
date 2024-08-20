NLP_tools
===============

Bibliothèque d'outils pour le traitement NLP (construite au dessus de https://spacy.io/) 

Liste des traitements NLP disponibles  :

* Stemming  (stemmer), en francais et en anglais
* Etiquettage en partie du discours  (POStagger), en francais et en anglais
* Reconnaissance de termes contrôlés (termMatcher)
* Reconnaissance d'entités nommées  (ner)
* Chunking nominal  (NPchunker)
* Chunking nominal issu d'une analyse en dépendance (NPchunkerDP)  

Deux types d'OUTPUT sont disponibles pour chaque traitement.  
Le résultat est présenté soit :

* intégré au texte d'origine (option -o doc)  
* sous la forme d'une liste (option -o list)
* sous la forme d'une liste (option -o json)
  

## Installation  

### Mode developpement  
```  
git clone http://vxgit.intra.inist.fr:60000/git/RichText/NLP_tools.git
```
ou pour une cloner une version specifique, exemple v1.0 :
```  
git clone --branch v1.0 http://vxgit.intra.inist.fr:60000/git/RichText/NLP_tools.git
``` 
Pour pointer sur la version de dev dans le PYTHONPATH :   =
  
Dans le repertoire où se trouve nlptools :
```
export PYTHONPATH=$PYTHONPATH:$PWD
```

Installation des dépendances :
```
pip3 install -r requirements.txt
```

##### Tests
Tests unitaires de chaque composants avec nose (mode lib) : 
```
nosetests test/nose/* 
```

Test en ligne de commande (CLI) : 
```
./test/cli/test_nlptoolsCLI.sh
```

### Production, en paquet python (directement depuis git) :
```      
pip3 install --upgrade --no-cache-dir --user git+http://vxgit.intra.inist.fr:60000/git/RichText/NLP_tools.git#egg=nlptools

``` 
ou pour une cloner une version specifique, exemple v1.0 

```
pip3 install --upgrade --no-cache-dir --user git+http://vxgit.intra.inist.fr:60000/git/RichText/NLP_tools.git@v1.0#egg=nlptools
```

##### Tester l'installation
Vérifier quelle est la version active sur votre système :

```
   pip3 show nlptools
```

Test d'execution :

``` 
python3 test/lib/full_txt_exec.py
python3 test/lib/full_tsv_exec.py
```

## Usage
### En ligne de commande
#### Mode production
```  
usage: nlptools [-h] [-file CORPUS] [-lang {fr,en}] [-f {txt,csv,tsv}] [-ini_file INI_FILE] [-param PARAM]
                      [-o {list,doc,json}] [-log LOG]
                      {stemmer,termMatcher,ner,NPchunker,POStagger,gazetteer,NPchunkerDP,lefff_tagger}

positional arguments:
  {stemmer,termMatcher,ner,NPchunker,POStagger,gazetteer,NPchunkerDP,lefff_tagger}
                        Name oh the NLPpipe

optional arguments:
  -h, --help            show this help message and exit
  -file CORPUS, --corpus CORPUS
                        Path to corpus file
  -lang {fr,en}, --language {fr,en}
                        language
  -f {txt,csv,tsv}, --format {txt,csv,tsv}
                        Format of the input corpus
  -ini_file INI_FILE, --ini-file INI_FILE
                        initialisation file [default config.ini]
  -param PARAM, --param PARAM
                        initialisation param in json
  -o {list,doc,json}, --output {list,doc,json}
                        Format result
  -log LOG, --log LOG   log file
```  
Exemple :  
Entrée de type fichier zippé .bz2 (option -file)  
```
nlptools -file test/data/notz.txt.bz2 stemmer -lang en -f txt -o doc -log test.log
```    
Entrée de type .text (ou csv)    
```  
echo "Correcting inner filter effects, a non multilinear tensor decomposition method.Among measurement used in analytical chemistry, fluorescence spectroscopy is widely spread and its applications are numerous" | nlptools stemmer -lang en -f txt -o doc   
```  
#### Mode developpement

Exemple :
```  
echo "Correcting inner filter effects, a non multilinear tensor decomposition method.Among measurement used in
 analytical chemistry, fluorescence spectroscopy is widely spread and its applications are numerous" |  nlptools POStagger -ini_file /home/schneist/app/NLP_tools/test/conf_test_epython3 nlptoolsn.ini -param '{"POStagger": {"POS_whitelist":["ADJ","NOUN","PROPN"]},"stemmer":{"stemmer_algo":"snowball"}}' -lang en -f txt -o json -log  analyze.log   
```  
``` 
nlptools  -file test/data/notz.tsv.bz2  POStagger -ini_file /home/schneist/app/NLP_tools/test
/conf_test_en.ini -param '{"POStagger": {"POS_whitelist":["ADJ","NOUN","PROPN"]},"stemmer":{"stemmer_algo":"snowball"}}' -lang en -f txt -o json -log  analyze.log
```  
### Commme une distribution Python : nlptools

**Code exemple :**  
Le programme suivant réalise un traitement de reconnaisance de termes (pipe="termMatcher") sur un corpus au format txt
 (corpus="not.txt.bz2").
Le programme produit sur le sortie standard. Les parametres dont le nom de la
terminologie à utiliser se trouvent dans un fichier de configuration (ini_file="conf.ini").  
conf_test.ini :  http://vxgit.intra.inist.fr:60000/RichText/NLP_tools/blob/master/test/conf_test.ini    
Un fichier de données text :  http://vxgit.intra.inist.fr:60000/RichText/NLP_tools/blob/master/test/data/notz.txt
.bz2  


```  
# paquet nlptools
from nlptools import *
from nlptools.tools import *
from nlptools.resources import *
    
import os
import time
import logging
    
def main():
    pipe = "termMatcher"  # choix du pipe a executer , parmi {stemmer,termMatcher,ner,NPchunker,POStagger,gazetteer}
    ini_file = "conf_test_en.ini"  # fichier de parametres
    log = "test.log"  # fichier de log
    corpus = "data/not.txt.bz2"  # corpus a traiter
    field = 1  # indique le nombre de champs tsv/csv/txt des fichiers du corpus
    language = "en" #langue

    run = full_run(pipe, ini_file, "doc", language)   # doc = corpus traité sur la sortie standard

    logging.basicConfig(filename=log, level=logging.DEBUG)
    t1 = time.time()

    # boucle de traitement sur le champ "text" de chaque document
    # label et keywords sont extraits, puis replacés
    for text in readTxtBz2(corpus, field):
        text_nlp = run.pipe_analyse(text)
        print(text_nlp)

    # calcul du temps execution
    t2 = time.time()
    logging.info("TRACE::Executing times %.3f " % (t2 - t1))

class full_run:

    def __init__(self,  pipe, ini_file, output):

        self.location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname("doc"))
        )
        self.parsers = [
            exec_spacy_pipe_en(pipe, ini_file, output),
        ]

    def pipe_analyse(self, text):

        # execution du pipe
        for parser in self.parsers:
            text = parser(text)
        return text

    if __name__ == "__main__":
    
        if __name__ == "__main__":
            main()
```  

### Fichier de parametres  
Les liens  vers les ressources et les parametres que définissent le comportement de chaque outil sont renseignés dans
 un fichier  de configuration (*.ini)   
 exemple : http://vxgit.intra.inist.fr:60000/RichText/NLP_tools/blob/master/test/conf_test_en.ini
 
 (A complèter)

### Dépendance (dans cette ordre) 

plac==0.9.6  
thinc==8.0.2  
spacy-lefff  
numpy==1.19.4    
spacy==3.0.4 (Le modèle Spacy utilisé est embarqué)  
nltk  
jinja2   

## (re)construction de la distribution
Pour reconstruire la distribution en developpement (dans le cas d'une nouvelle version) : 
Modifier le contenu du fichier tag.txt qui contient le numero de version
Exécuter :
```
 ./build_push_package.sh
```
Ensuite, pousser la version sur le dépot git (add, commit, push).

Le script suivant prend en charge toute procedure. 
```
 ./build_push_package.sh [--tagged]
``` 
l'option --tagged tague la version avec la valeur de tag.txt  

### TODO (17/10/2021)

* TODO : revoir nosetest 
* TODO : intégrer/tester, fonction NLpre et faire menage pretraitement de nettoyage  
* BUG : gazetteer ne sort que des formes de 2 unites
* AM : ajouter traitement StopList ; parse("stoplist"); alimenter "stop list spacy" => token.is_stop = True  q!
* AM : test : prise en compte de fichiers de data pour les tests pour nose
* AM : ajouter la notion de  ex: writer(termatcher, doc, file)
* AM : faire test sur doc pdf  
* AM : rapidité : mis en parallele des traitements

