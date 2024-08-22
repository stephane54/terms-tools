#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
# exemple : python3 nlptools  test/data/med10.csv.bz2 -p "lemme" -log test
#
from nlptools.tools import readCsvBz2, readTxtBz2, tab, space, readCsv, tab
import os
import time
import plac
import logging
import sys
from pathlib import Path
from nlptools.run import full_run
from nlptools.tools import  dive_term
@plac.annotations(
    pipe=(
        "Name oh the NLPpipe ",
        "positional",
        None,
        str,
        ["termMatcher", "NPchunker", "POStagger", "NPchunkerDP"]
    ),
    corpus=("Path to corpus file", "option", "file", str),
    language=("language", "option", "lang", str, ["fr", "en"]),
    ini_file=("initialisation file [default config.ini]", "option", "ini_file", str),
    param=("initialisation param in json", "option", "param", str),  
    format=("Format of the input corpus ", "option", "f", str, ["text", "terms"]),
    output=("Format result; 'dico_pos' illegal 'with text' ", "option", "o", str, ["list", "doc", "json", "dico_pos"]),
    log=("log file", "option", "log", str),
)

def main (pipe, corpus, language, format, ini_file, param, output, log):
     
    # test parameter combinaison legality
    if (format != "terms" and output == "dico_pos" ):
            sys.exit(u'ERROR : terms_tools.py : illegal parameters combinaison')       
    if (format == "terms" and pipe != "POStagger"  ):
        sys.exit(u"ERROR : terms_tools.py : This NLP component doesn't work with this input !")       

    # creation d1 instance de pipe
    pipe = full_run(pipe, language, ini_file, param, output, format)
    field = 2  # nombre de champs tsv des fichiers du corpus , format : label TAB text

    logging.basicConfig(filename=log, level=logging.DEBUG)
    t1 = time.time()

    # test la presence d un corpus
    if corpus:
        # entrée type fichier
        my_file = Path(corpus)
        if not (my_file.is_file()):
            logging.error("corpus file not found !")
            exit(0)
        else:
            # TODO : ameliorer le controle du format
            if format == "terms":    
                # csv, tsv
                for [label, text] in readCsvBz2(corpus, field):
                    text_nlp = pipe.pipe_analyse(dive_term(text, language))
                    # kw=list(set( ([w for w in span.split(space) if w.startswith(pref)])))
                    print(label, tab, text_nlp, space)
                        
            else:
                # text
                for text in readTxtBz2(corpus, field):
                    # exec du pipe sur une ligne du corpus txt
                    text_nlp = pipe.pipe_analyse(text)
                    print(text_nlp)
    else:
        # entrée type stdin
        if format == "terms": 
            # csv, tsv
            for row in readCsv(sys.stdin.readline, field):
                text_nlp = pipe.pipe_analyse(dive_term(row[1], language))
                print(row[0],tab,(text_nlp))
                         
        else:
            # text
            for line in sys.stdin:
                text_nlp = pipe.pipe_analyse(line)
                print(text_nlp)

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
        
