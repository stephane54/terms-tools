#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.py

"""
#
#     Annotation d un corpus avec une ressource termino
#
#     NB : la termino est fixe par le param  keywords_dict de dictionary/__init__.py/
#
#     USAGE: 
#       usage: usage: term-tagger.py [-h] [-file FILE_TEXT] [-d MATCHER_DICO] [-output {list,doc,json}] [-add_stp] [-format ul] [-norm lower] [-p]
#
#      python3 nlptools/term-tagger.py -file $HOME/app/terms_tools/data/corpus_test_memoire_en.tsv -output doc -norm lower -add_stp -format pref -d memoire-lower-pref.tsv
#
#     INPUT :
#        Sortie standard
#        error :  term-tagger.log
#
#     PARAM :
#        -file          file
#        -output        {list, doc, json} mode d'affichage des annotations 
#                            list = standoff , doc = insertion dans le texte, json = format flash des annotations
#        -d MATCHER_DICO, --matcher-dico MATCHER_DICO
#                        flash matcher dico in tsv format
#        -format        {pref, id ,ul} nature des annotations : affiche la forme preferentiel, la forme initiale ou L ID du concept
#        -norm          {lemma,lower, raw}  # forme des elements qui sont matchés, texte et termino. Egalement forme de la sortie textuelle
#                       ATTENTION : flashtext param => "case_sensitive": True r false (fixe si algo sensitive a la case ou pas)
#        -add_stp       flag : add stop word liste , dictionary/my_stopwords.tsv
#        -p             str : prefixe qui marque les formes identifiées
#        -num           flag : numerotation des id (cas id non unique tel que ARK concept)
#
#     DICTIONNARY FORM EX :
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6.0      brain lobe      		  brain lobe   			brain lobe      brain_lobe
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6.1      lobe of the brain       lobe of the brain     brain lobe      brain_lobe
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6.2      brain lobes     		  brain lobe     	    brain lobe      brain_lobe
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6.3      lobes of the brain      lobe of the brain     brain lobe      brain_lobe
#

import spacy
from nlptools.models import modele_init_en
import spacy_stanza
import sys
from time import time
import os.path
import fileinput
from multiprocessing import set_start_method, Pool
import logging
import plac
from nlptools.run_tagger import Run_tagger
from nlptools.matcherFlash import MatcherFlash
from resources import ressource_dir 
import warnings

# desactive les logs
warnings.filterwarnings("ignore")

__authors__ = "Stephane Schneider"
__contact__ = "stephane.schneider@inist.fr"

# --------------------
log = "term-tagger.log"
core = 4
silent = True  # niveau de description dans les log

# BCP PLUS LENT AVEC STANZA !# est ce utile plutot que spacy?

@plac.annotations(    
    file_text=("Path to corpus file", "option", "file", str),
    matcher_dico=(
        "flash matcher dico in tsv format",
        "option",
        "d",
        str,
    ),
    output=(
        "format of the annotation ",
        "option",
        "output",
        str,
        ["list", "doc", "json"],
    ),
    prefix=("tag for mark the entry found", "option", "p", str),
    norm=(
        "execute lower or lemma pretraitment [default lower]",
        "option",
        "norm",
        str,
        ["lemma", "lower", "raw"],
    ),
    format=("tag text with [pref,id,ul], pref or id_pref or text ul", "option","format",str, ["pref","id","ul"]),
    add_stop=("add stop word list [default no]", "flag", "add_stp"),
)
def main(file_text,matcher_dico, output, add_stop, format="ul", norm="lower", prefix=""):

    # execution
    start_time = time()
    if file_text:
        iterator = fileinput.input(file_text)
    else:
        iterator = sys.stdin
        
    #set_start_method("forkserver")

    if add_stop:
        from resources import my_stopword_file as stopword_file
    else:
        stopword_file = ""

    # tune logger
    if silent:
        logging.basicConfig(filename=log, level=logging.INFO)
        logging.info("log mode silent")
    else:
        logging.basicConfig(filename=log, level=logging.DEBUG)
        logging.debug("log mode bavard")

    # check dictionnary exist 
    keywords_dict = os.path.join(ressource_dir, matcher_dico)
    if matcher_dico: 
        #check name file
        norm_list=[norm]         
        if not (os.path.isfile(keywords_dict)):
            raise ValueError(keywords_dict)
        if not(any(map(keywords_dict.__contains__, norm_list))):
            msg = "Bad file name {} with this -norm ={} parameter ".format(keywords_dict, norm)
            logging.error(msg)
            raise IOError()
    
    # loading du modele
    modele = modele_init_en
    
    # prepare config Spacy pipeline
    # config Spacy pipeline must be compatible with the resource format (lemma,lower,raw)
    if norm == "lemma":

        nlp = spacy.load(modele, disable=["ner", "parser", "textcat"])
        #nlp = spacy_stanza.load_pipeline('en', processors='tokenize,mwt,pos,lemma', verbose = False,  logging_level = 'FATAL')
        nlp.max_length = 2000000  # or higher

    elif norm == "lower" or norm == "raw":

        nlp = spacy.load(modele, disable=["ner", "lemmatizer", "parser", "textcat"])
        #nlp = spacy_stanza.load_pipeline('en', processors='tokenize,mwt,pos', verbose = False,  logging_level = 'FATAL')
        nlp.max_length = 2000000  # or higher
        
    else:
        msg = "Can't Find parameter {}".format(norm)
        logging.error(msg)
        raise IOError()

    logging.info(f"LOAD DICO ......")
    logging.info(f" {keywords_dict}")
    logging.info(f" PARM [norm:{norm}][format:{format}]")

    # Configure the flash matcher
    # add Matcher_flash at the end of spacy pipe
    nlp.add_pipe(
        "Matcher_flash",
        name="Matcher_flash",
        config={
            "output": output,
            "prefix": prefix,
            "keywords_dict": keywords_dict,
            "case_sensitive": False,
            "stopword_file": stopword_file,
            "format": format,
            "text_format": norm,
        },
        last=True,
    )
    one_run = Run_tagger(nlp)
    logging.info(f" len(DICO) charged : {MatcherFlash.size_voc}")
    i = 0
    logging.info(f"PROCESS CORPUS ...")

    with Pool(core) as pool:
        #for text in pool.map(one_run.run_tagger, iterator):

        for text in map(one_run.run_tagger, iterator):
            # output
            sys.stdout.write(text)
            sys.stdout.write("\n")
            i += 1

    logging.info(
        f"  Number of traited documents : {i} in times { (time() - start_time)/60} secondes \n"
    )   
        
        #f.close()


if __name__ == "__main__":
    if False:
        import cProfile
        import pstats

        cProfile.runctx("plac.call(main)", globals(), locals(), "Profile.prof")
        s = pstats.Stats("Profile.prof")
        s.strip_dirs().sort_stats("time").print_stats()
    else:
        plac.call(main)
