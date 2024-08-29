#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
#
# exemple : 
# cat ../../../terms_tools/test/data/not-en.txt| python3 analyze.py POStagger -f text -o doc -log analyze.log -lang en 
#
from nlptools.tools import readCsvBz2, readTxtBz2, tab, space, readCsv, tab
import time
import plac
import csv
import logging
import sys
import json
from pathlib import Path
from nlptools.run import full_run
from nlptools.tools import  dive_term
@plac.annotations(
    pipe=(
        "Name oh the NLPpipe ",
        "positional",
        None,
        str,
        ["NPchunker","POStagger", "NPchunkerDP", "termMatcher"]
    ),
    language=("language", "option", "lang", str, ["fr", "en"]),
    ini_file=("initialisation file [default config.ini]", "option", "ini_file", str),
    param=("initialisation param in json", "option", "param", str),  
    format=("Format of the input corpus ", "option", "f", str, ["text", "terms"]),
    output=("Format result; 'dico_pos' illegal 'with text' ", "option", "o", str, ["list", "doc", "json", "dico_pos", "dico_annot"]),
    log=("log file", "option", "log", str),
)

def main (pipe, language, format, ini_file, param, output, log):
    
    compteur = 0
     
    # test parameter combinaison legality
    if (format != "terms" and output in ["dico_pos","dico_annot"] ):
        raise ValueError(u'ERROR : terms_tools.py : illegal parameters combinaison')       
            
    if (format == "terms" and pipe !=  "POStagger"  ):
        raise ValueError(u"ERROR : terms_tools.py : This NLP component doesn't work with this input !")       
    
    # Forcer Utilisation de Stanza ou Spacy
    if pipe == "POStagger":  
        pipe =  "POStaggerStanza" #"POStaggerSpacy"
    if pipe == "termMatcher":  
        pipe =  "termMatcherStanza" #"termMatcherSpacy"
    
    # creation d1 instance de pipe
    pipe = full_run(pipe, language, ini_file, param, output, format)
    field = 2  # nombre de champs tsv des fichiers du corpus , format : label TAB text

    logging.basicConfig(filename=log, level=logging.DEBUG)
    t1 = time.time()
    # boucle de traitement sur le champ "text" de chaque document
    # label et keywords sont extraits, puis replacés
    #j
    #  son
    for json_line in sys.stdin:
        compteur += 1
        try:
            data = json.loads(json_line )
        except json.decoder.JSONDecodeError:
            logging.error("Input format problem line :{} : String could not be converted to JSON".format(compteur))
            exit(1)

        # print("in".format(compteur))
        # NB : sortie avec \" car dump json protege", evité si ' replace("""", "\'")
        data["value"] = pipe.pipe_analyse(dive_term(data["value"], language))
        #print("ou".format(compteur))
        sys.stdout.write(json.dumps(data))
        sys.stdout.write('\n')    
        

    # calcul du temps execution
    t2 = time.time()
    logging.info("TRACE::Executing times %.3f " % (t2 - t1))

def console_scripts_main():

    plac.call(main)


if __name__ == "__main__":

    if False:
        import cProfile
        import pstats

        cProfile.runctx("plac.call(main)", globals(), locals(), "Profile.prof")
        s = pstats.Stats("Profile.prof")
        s.strip_dirs().sort_stats("time").print_stats()
    else:
        plac.call(main)

