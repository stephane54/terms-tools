#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
# paquet nlptools
from nlptools import *
from nlptools.tools import *
from nlptools.resources import *
from nlptools.run import full_run

import os
import time
import logging
from pathlib import Path

def main():

    _local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pipe = "termMatcher"  # choix du pipe a executer , parmi {stemmer,termMatcher,ner,NPchunker,POStagger,gazetteer}
    ini_file = os.path.join(_local_path, "conf_test_en.ini")
    #print(ini_file)
    log = "test.log"  # fichier de log
    corpus = os.path.join(_local_path, "data/notz.txt.bz2");  # corpus a traiter
    field = 1  # indique le nombre de champs tsv/csv/txt des fichiers du corpus
    language = "en" #langue
    param=""

    run = full_run(pipe, language, ini_file, param, "doc")   # doc = corpus traité sur la sortie standard
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


if __name__ == "__main__":

    if __name__ == "__main__":
        main()
