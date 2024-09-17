# terms_tools
===============

Bibliothèque d'outils pour l'etiquettage POS et la reconnaissance de termes (construite au dessus de stanza) 

Liste des traitements   :

1/ POStag et lemmatisation d'une liste de termes en fr en En , en francais et en anglais

IN?PUT : 
id      text
http://data.loterre.fr/ark:/67375/P66#xl_en_9278939f    qualities
http://data.loterre.fr/ark:/67375/P66#xl_en_696ab94f    material entities
http://data.loterre.fr/ark:/67375/P66#xl_en_d9fccd58    process
http://data.loterre.fr/ark:/67375/P66#xl_en_0fa9a1f2    empirical effect
http://data.loterre.fr/ark:/67375/P66#xl_en_ba359dd0    empirical generalization
http://data.loterre.fr/ark:/67375/P66#xl_en_06b45a8a    general empirical observation
http://data.loterre.fr/ark:/67375/P66#xl_en_d9a365b6    empirical generalisations

Trois types d'OUTPUT sont disponibles  

* sous la forme d'un dictionaire jsonld avec l ensemble des informations (option -o json)
* exemple: 
http://data.loterre.fr/ark:/67375/P66#xl_en_53acd26b     [{"id": 0, "start": 0, "end": 7, "tag": "JJ", "pos": "ADJ", "morph": "Degree=Pos", "lemma": "general"}, {"id": 1, "start": 8, "end": 17, "tag": "JJ", "pos": "ADJ", "morph": "Degree=Pos", "lemma": "empirical"}, {"id": 2, "start":
18, "end": 30, "tag": "NNS", "pos": "NOUN", "morph": "Number=Plur", "lemma": "observation"}]

* sous une forme tabulée simplifié de la forme : URI   POSTAG LEMMA      (option -o dico_pos)
exemple: 
http://data.loterre.fr/ark:/67375/P66#xl_en_542d3e8b     cognitive qualities    JJ NNS  cognitive quality
http://data.loterre.fr/ark:/67375/P66#xl_en_9ac2b72c     cognitive quality      JJ NN   cognitive quality
http://data.loterre.fr/ark:/67375/P66#xl_en_ef4050c0     objects        NNS     object

* sous la forme d'un dictionnaire pour termMatcher
exemple: 
http://data.loterre.fr/ark:/67375/P66#xl_en_d2b95b32     {"label": "empirical generalisation ", "pattern": [{"pos": "ADJ", "lemma": "empirical"}, {"pos"
: "NOUN", "lemma": "generalisation"}], "id": "http://data.loterre.fr/ark:/67375/P66#xl_en_d2b95b32"}

  
 2/ Reconnaissance de termes


## Installation  

### Mode developpement  
```  
git clone http://vxgit.intra.inist.fr:60000/git/schneist/terms_tools.git
```
ou pour une cloner une version specifique, exemple v1.0 :
```  
git clone --branch v1.0 http://vxgit.intra.inist.fr:60000/git/schneist/terms_tools.git
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


##### Tester l'installation


## Usage
### En ligne de commande
#### Mode production
```  
usage: terms_tools [-h] [-file CORPUS] [-lang {fr,en}] [-f {text,terms}] [-ini_file INI_FILE] [-param PARAM] [-o {list,doc,json,dico_pos,dico_annot}]
                   [-log LOG] [-ezs]
                   {NPchunker,POStagger,NPchunkerDP,termMatcher}

positional arguments:
  {NPchunker,POStagger,NPchunkerDP,termMatcher}
                        Name oh the NLPpipe

optional arguments:
  -h, --help            show this help message and exit
  -file CORPUS, --corpus CORPUS
                        Path to corpus file
  -lang {fr,en}, --language {fr,en}
                        language
  -f {text,terms}, --format {text,terms}
                        Format of the input corpus
  -ini_file INI_FILE, --ini-file INI_FILE
                        initialisation file [default config.ini]
  -param PARAM, --param PARAM
                        initialisation param in json
  -o {list,doc,json,dico_pos,dico_annot}, --output {list,doc,json,dico_pos,dico_annot}
                        Format result; 'dico_pos' illegal 'with text'
  -log LOG, --log LOG   log file
```  
Exemple :  
Entrée de type fichier zippé .bz2 (option -file)  
```

POSTAG : 
 ---------
 EN :

cat test/data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -ini test/conf_test_en.ini -f terms -o dico_pos  -log analyze.log -lang en -ezs | more
cat test/data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -ini test/conf_test_en.ini -f terms -o dico_annot  -log analyze.log -lang en | more
cat test/data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -ini test/conf_test_en.ini -f terms -o json  -log analyze.log -lang en  

Mais aussi
cat test/data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -ini test/conf_test_en.ini -f terms -o doc  -log analyze.log -lang en  
cat test/data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -ini test/conf_test_en.ini -f terms -o list  -log analyze.log -lang en


#### En mode CLI paquet python 
 cat test/data/labelFR.tsv| terms_tools POStagger -ini test/conf_test_fr.ini -f terms -o dico_pos  -log analyze.log -lang fr
 cat test/data/labelFR.tsv| terms_tools POStagger -ini test/conf_test_fr.ini -f terms -o dico_annot  -log analyze.log -lang fr
 cat test/data/labelFR.tsv| terms_tools POStagger -ini test/conf_test_fr.ini -f terms -o json  -log analyze.log -lang fr
 
 cat test/data/labelEN.tsv| terms_tools POStagger -ini test/conf_test_en.ini -f terms -o dico_annot  -log analyze.log -lang en 
 cat test/data/labelEN.tsv| terms_tools POStagger -ini test/conf_test_en.ini -f terms -o dico_pos  -log analyze.log -lang en
 cat test/data/labelEN.tsv| terms_tools POStagger -ini test/conf_test_en.ini -f terms -o json  -log analyze.log -lang en
 
 
 TERMATCHER  
 ------------
=> Annote un texte avec un dico produit avec l 'option dico_annot

 EN :
cat test/data/not-en.tsv| python3 nlptools/terms_toolsCLI.py termMatcher -ini test/conf_test_en.ini -f text -o doc -log analyze.log -lang en
cat test/data/not-en.tsv| python3 nlptools/terms_toolsCLI.py termMatcher -ini test/conf_test_en.ini -f text -o list -log analyze.log -lang en
cat test/data/not-en.tsv| python3 nlptools/terms_toolsCLI.py termMatcher -ini test/conf_test_en.ini -f text -o json -log analyze.log -lang en

 FR :
cat test/data/not-fr.tsv| python3 nlptools/terms_toolsCLI.py termMatcher -ini test/conf_test_fr.ini -f text -o json -log analyze.log -lang fr
cat test/data/not-fr.tsv| python3 nlptools/terms_toolsCLI.py termMatcher -ini test/conf_test_fr.ini -f text -o doc -log analyze.log -lang fr
cat test/data/not-fr.tsv| python3 nlptools/terms_toolsCLI.py termMatcher -ini test/conf_test_fr.ini -f text -o list -log analyze.log -lang fr 
 