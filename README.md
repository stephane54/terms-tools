# terms_tools
===============

Bibliothèque d'outils pour l'etiquettage POS et la reconnaissance de termes (construite au dessus de spacy)


## Installation  

### Mode developpement  
```  
git clone https://github.com/stephane54/terms-tools.git
```
ou pour une cloner une version specifique, exemple v2.0 :
```  
git clone --branch v2.0 https://github.com/stephane54/terms-tools.git
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

Installer les modèles Spacy : 
```
python -m spacy download  en_core_web_trf
python -m spacy download  fr_dep_news_trf
```

## Usage

### POStag et lemmatisation d'une liste de termes en francais et en anglais

#### En mode Dev
```
 terms_tools | python3 terms_toolsCLI.py 
 [-h] [-file CORPUS] [-d MATCHER_DICO] [-lang {fr,en}] [-f {text,terms}] [-ini_file INI_FILE] [-param PARAM]
                         [-o {list,doc,json,dico_pos,dico_annot}] [-log LOG] [-ezs]
                         {NPchunker,POStagger,NPchunkerDP,termMatcher}

positional arguments:
  {NPchunker,POStagger,NPchunkerDP,termMatcher}
                        Name of the NLPpipe

options:
  -h, --help            show this help message and exit
  -file CORPUS, --corpus CORPUS
                        Path to corpus file
  -d MATCHER_DICO, --matcher-dico MATCHER_DICO
                        termMatcher dico path in jsonld format
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
  -ezs, --ezs           ezs way, output jsonld {id=,value=}
```  
```  
cat ./data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -f terms -o dico_pos -log analyze.log -lang en
cat ./data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -f terms -o dico_annot -log analyze.log -lang en
cat ./data/labelFR.tsv| python3 nlptools/terms_toolsCLI.py POStagger -f terms -o dico_pos -log analyze.log -lang fr 
```

Mais aussi
```  
cat ./data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -f terms -o doc  -log analyze.log -lang en  
cat ./data/labelEN.tsv| python3 nlptools/terms_toolsCLI.py POStagger -f terms -o list  -log analyze.log -lang en
```  

#### En mode paquet python  
```  
 cat ./data/labelFR.tsv| terms_tools POStagger -ini test/conf_test_fr.ini -f terms -o dico_pos  -log analyze.log -lang fr
 cat ./data/labelFR.tsv| terms_tools POStagger -ini test/conf_test_fr.ini -f terms -o dico_annot  -log analyze.log -lang fr
 cat ./data/labelFR.tsv| terms_tools POStagger -ini test/conf_test_fr.ini -f terms -o json  -log analyze.log -lang fr 
 cat ./data/labelEN.tsv| terms_tools POStagger -ini test/conf_test_en.ini -f terms -o dico_annot  -log analyze.log -lang en 
 cat ./data/labelEN.tsv| terms_tools POStagger -ini test/conf_test_en.ini -f terms -o dico_pos -log analyze.log -lang en
 cat ./data/labelEN.tsv| terms_tools POStagger -ini test/conf_test_en.ini -f terms -o json -log analyze.log -lang en
 ```  
 
#### Exemple  

INPUT :
http://data.loterre.fr/ark:/67375/P66#xl_fr_f02a6831    inflation de l'imagination
http://data.loterre.fr/ark:/67375/P66#xl_fr_d33d7377    inflation par imagination
http://data.loterre.fr/ark:/67375/P66#xl_fr_7f695a51    effet d'inflation par imagination
http://data.loterre.fr/ark:/67375/P66#xl_fr_b0c3cc69    effet du tout sur la partie
http://data.loterre.fr/ark:/67375/P66#xl_fr_8bef8ccd    effet McCabe
http://data.loterre.fr/ark:/67375/P66#xl_fr_2399392f    effet de dépendance au contexte
http://data.loterre.fr/ark:/67375/P66#xl_fr_26ecc45b    effet du souvenir dépendant du contexte
http://data.loterre.fr/ark:/67375/P66#xl_fr_75d73261    mémoire dépendante du contexte environnemental

RESULTAT :
http://data.loterre.fr/ark:/67375/P66#xl_fr_f02a6831     inflation de l' imagination    NOUN ADP DET NOUN       inflation de le imagination
http://data.loterre.fr/ark:/67375/P66#xl_fr_d33d7377     inflation par imagination      NOUN ADP NOUN   inflation par imagination
http://data.loterre.fr/ark:/67375/P66#xl_fr_7f695a51     effet d' inflation par imagination     NOUN ADP NOUN ADP NOUN  effet de inflation par imagination
http://data.loterre.fr/ark:/67375/P66#xl_fr_b0c3cc69     effet du tout sur la partie    NOUN ADP NOUN ADP DET NOUN      effet de tout sur le partie
http://data.loterre.fr/ark:/67375/P66#xl_fr_8bef8ccd     effet McCabe   NOUN PROPN      effet mccabe
http://data.loterre.fr/ark:/67375/P66#xl_fr_2399392f     effet de dépendance au contexte        NOUN ADP NOUN ADP NOUN  effet de dépendance au contexte

## Reconnaissance de termes dans des documents en francais et en anglais  
```  
loterre_tag | python3 term_taggerCLI.py
 [-h] [-corpus CORPUS] [-d MATCHER_DICO] [-output {list,doc,json}] [-add_stp] [-p PREFIX]
                         [-f {pref,id,ul,term}] [-i {jsonl,json,txt}] [-lang '']

 -corpus CORPUS, --corpus CORPUS
                        Path to corpus file
  -d MATCHER_DICO, --matcher-dico MATCHER_DICO
                        flash matcher dico in tsv format
  -output {list,doc,json}, --output {list,doc,json}
                        format of the annotation
  -add_stp, --add-stop  add stop word list [default no]
  -p PREFIX, --prefix PREFIX
                        tag for mark the entry found in , only for doc output, defaut none
  -f {pref,id,ul,term}, --format {pref,id,ul,term}
                        form to display in the doc [id, ul, term,pref,], only for doc output, default term
  -i {jsonl,json,txt}, --input {jsonl,json,txt}
                        input format
  -lang '', --language ''
                        language
```  
Positionner la variable DICO_PATH avec le chemin où se trouve les dictionnaires :  
ex: DICO_PATH=/<moncompte>/terms_tools/dictionnary

#### En mode Dev
```  
python3 nlptools/term_taggerCLI.py -corpus ./data/P66_fr.jsonl -output json -lang fr -add_stp -d  fr_annotflash_P66.tsv -i jsonl
python3 nlptools/term_taggerCLI.py -corpus ./data/P66_en.jsonl -output json -lang en -add_stp -d  en_annotflash_P66.tsv -i jsonl
```  
#### En mode paquet python 
```  
loterre_tag -corpus ./data/P66_fr.json -output json -lang fr -add_stp -d  fr_annotflash_P66.tsv -i json
loterre_tag -corpus ./data/9SD_en_ezs.jsonl -output json -lang en -add_stp -d  /home/schneist/app/terms_tools/terms_tools/dictionary/en_annotflash_9SD.tsv -i jsonl
```  

#### Exemple
INPUT : 
{"id":"1","value":"courbe d'apprentissage à accélération positive est un type de courbe d'apprentissage indiquant que l'apprentissage débute lentement puis s'accélère."}
{"id":"2","value":"La maladie d'Alzheimer se traduit par des probleme de la vessie, de l'exécution de gestes simples "}

RESULTAT :
{"id": "1", "value": [{"idx": {"start": "10", "end": "23"}, "match": {"id": "http://data.loterre.fr/ark:/67375/p66-r9dc7tzn-9", "ul": "apprentissage", "term": "apprentissage", "pref": "apprentissage"}}, {"idx": {"start": "26", "end": "46"}, "match": {"id": "http://data.loterre.fr/ark:/67375/p66-tpdktcb1-n", "ul": "accélération positif", "term": "accélération positive", "pref": "courbe d'apprentissage à accélération positive"}}, {"idx": {"start": "73", "end": "86"}, "match": {"id": "http://data.loterre.fr/ark:/67375/p66-r9dc7tzn-9", "ul": "apprentissage", "term": "apprentissage", "pref": "apprentissage"}}, {"idx": {"start": "103", "end": "116"}, "match": {"id": "http://data.loterre.fr/ark:/67375/p66-r9dc7tzn-9", "ul": "apprentissage", "term": "apprentissage", "pref": "apprentissage"}}]}