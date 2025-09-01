#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
# exemple : python3 nlptools  test/data/med10.csv.bz2 -p "lemme" -log test
#
from nlptools.tools import readCsvBz2, readTxtBz2, tab, space, readCsv, tab
import time
import plac
import logging
import sys
import os
import json
from pathlib import Path
from nlptools.run import Pipe
from nlptools.tools import  dive_term
@plac.annotations(
    pipe=(
        "Name of the NLPpipe ",
        "positional",
        None,
        str,
        ["NPchunker","POStagger", "NPchunkerDP", "termMatcher"]
    ),
    matcher_dico=(
        "termMatcher dico path in jsonld format ",
        "option",
        "d",
        str,
    ),
    corpus=("Path to corpus file", "option", "file", str),
    language=("language", "option", "lang", str, ["fr", "en"]),
    ini_file=("initialisation file [default config.ini]", "option", "ini_file", str),
    param=("initialisation param in json", "option", "param", str),  
    format=("Format of the input corpus ", "option", "f", str, ["text", "terms"]),
    output=("Format result; 'dico_pos' illegal 'with text' ", "option", "o", str, ["list", "doc", "json", "dico_pos", "dico_annot"]),
    log=("log file", "option", "log", str),
    ezs=("ezs way, output jsonld {id=,value=}", "flag", "ezs"),
)

def main (pipe, corpus, matcher_dico, language, format, ini_file, param, output, log, ezs):
     
    # test parameter combinaison legality
    if (format != "terms" and output in ["dico_pos","dico_annot"] ):
        raise ValueError(u'ERROR : terms_tools.py : illegal parameters combinaison')       
            
    if (format == "terms" and pipe !=  "POStagger"  ):
        raise ValueError(u"ERROR : terms_tools.py : This NLP component doesn't work with this input !")       
    
    if (matcher_dico  and pipe !=  "termMatcher"  ):
        raise ValueError(u"ERROR : terms_tools.py : This NLP component doesn't work with this input !")       
    
    # check dictionnary exist 
    if matcher_dico: 
        if not (os.path.isfile(matcher_dico)):
            raise ValueError(matcher_dico)
    
    # creation d1 instance de pipe
    pipe = Pipe(pipe, matcher_dico, language, ini_file, param, output, format)
    field = 2  # nombre de champs tsv des fichiers du corpus , format : label TAB text

    logging.basicConfig(filename=log, level=logging.DEBUG)
    t1 = time.time()
    
    if corpus:  # test la presence d'un fichier corpus
        # entrée type fichier zippé
        my_file = Path(corpus)
        if not (my_file.is_file()):
            logging.error("corpus file not found !")
            exit(0)
        else:
            # TODO : ameliorer le controle du format   
            # csv, tsv
            for [label, value] in readCsvBz2(corpus, field):
                if format == "terms":
                    text_nlp = pipe.pipe_analyse(dive_term(value, language))
                else:
                    text_nlp = pipe.pipe_analyse(value)
                
                if output == "dico_annot":
                    text_nlp["id"]=label
                    print(json.dumps(text_nlp, ensure_ascii=False))
                else :
                    print(label, tab, text_nlp, space)       
        
    else:
        # ezs format : jsonld, {id,value}
        if ezs:
            compteur = 0
            for json_line in sys.stdin:
                compteur += 1
                try:
                    data = json.loads(json_line)
                except json.decoder.JSONDecodeError:
                    logging.error("Input format problem line :{s1}{s2} : String could not be converted to JSON".format(s1 = compteur,s2 = json_line) )
                    exit(1)

                # NB : sortie avec \" car dump json protege", evité si ' replace("""", "\'")
                if format == "terms":
                    data["value"] = pipe.pipe_analyse(dive_term(data["value"], language))  # "value" car flux ezs jsonld au format id=,value=
                else:
                    data["value"] = pipe.pipe_analyse(data["value"])  # "value" car flux ezs jsonld au format {id:,value:}
                
                #print("ou".format(compteur))
                sys.stdout.write(json.dumps(data))
                sys.stdout.write('\n')  
        
        else:
            # entrée type stdin csv, tsv
            for row in readCsv(sys.stdin.readline, field):
                #TRACE print("DEBUT ANALYSE 1")
                if format == "terms":
                    text_nlp = pipe.pipe_analyse(dive_term(row[1], language))
                else:
                    text_nlp = pipe.pipe_analyse(row[1])
                    
                if output in ["dico_annot"]:
                    text_nlp["id"]=row[0]
                    print(json.dumps(text_nlp, ensure_ascii=False))
                else:
                    print(row[0],tab,(text_nlp))
                #TRACE print("FIN ANALYSE 2")
                         
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
        
