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
#     usage: term_taggerCLI.py [-h] [-corpus CORPUS] [-d MATCHER_DICO] [-output {list,doc,json}] [-add_stp] [-p PREFIX]
#                      [-f {pref,id,ul,term}] [-lang '']
#                      file_text
#
#     DICTIONNARY FORM EX :
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6	brain lobe	brain lobe	brain lobe
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6	lobe of the brain	lobe of the brain	brain lobe
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6	brain lobes	brain lobe	brain lobe
# http://data.loterre.fr/ark:/67375/p66-j7p6ztdt-6	lobes of the brain	lobe of the brain	brain lobe
#
#  Exemple : 
# python3 term_taggerCLI.py $HOME/app/terms_tools/data/corpus_test_memoire_en.tsv -output list -lang en -add_stp   -d  $HOME/app/termino_tools/termino_tools/dictionary/out/memoire-lower-en.tsv
#
# python3 term_taggerCLI.py $HOME/app/terms_tools/data/corpus_test_memoire_en.tsv -output doc -lang en -add_stp  -d  $HOME/app/termino_tools/termino_tools/dictionary/out/memoire-lower-en.tsv -p TERM_ -f pref
#
# python3 term_taggerCLI.py $HOME/app/terms_tools/data/corpus_test_memoire_fr.tsv -output json -lang fr -add_stp  -d  $HOME/app/termino_tools/termino_tools/dictionary/out/memoire-lemma-fr.tsv 
# 
#
    # fichiers en entrée
    #   json sur une ligne, format 1d,text 
    #   jsonl, format id,text, 1 texte par ligne 
    #   text, 1 a n text par ligne
    #
    #  PAS DE LIGNE VIDE
    #
#
#  TODO :
#    Doc renvoi un texte lemmatisé ou lower, cad le texte pretraité qui a été passé à flash. Faire plutot un réalignement
#
import spacy        # spacy utilisé car plus rapide que stanza
import sys
from time import time
import os.path
from nlptools.matcherFlash import MatcherFlash
import fileinput
from multiprocessing import set_start_method, Pool
import logging
import plac
from nlptools.run_tagger import Run_tagger
from nlptools.resources import resource_dir 
from nlptools.models import modele_init_fr
from nlptools.models import modele_init_en
import warnings

warnings.filterwarnings("ignore")
__authors__ = "Stephane Schneider"
__contact__ = "stephane.schneider@inist.fr"

# --------------------
log = "term-tagger.log"
core = 8
silent = False  # niveau de description dans les log

@plac.annotations(
    corpus=("Path to corpus file", "option", "corpus", str),
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
    format=("form to display in the doc [id, ul, term,pref,], only for doc output, default term","option","f", str, ["pref","id","ul","term"]),
    prefix=("tag for mark the entry found in , only for doc output, defaut none ", "option", "p", str),
    language=("language", "option", "lang", str, ["fr", "en"]),
    add_stop=("add stop word list [default no]", "flag", "add_stp"),
    input=("input format ", "option", "i", str, ["jsonl", "json", "txt"]),
)
def main(corpus,matcher_dico, output, add_stop, prefix, format, input, language=""):
   
    # test parameter combinaison legalite   
    if (output in ["json","jsonl","list"] and (format or prefix) ):
        raise ValueError(u"ERROR : incompatible option !")  
    
    if (output == "doc"):
        if  (not prefix):
            prefix=""
        if  (not format):
            format="term"  
   
    if language == "fr":
        norm = "lemma"
    elif language == "en":
        norm = "lower"
    else:
        norm ="raw"
         
    # execution
    start_time = time()
    
    iterator = fileinput.input(corpus)

    if corpus:
        iterator = fileinput.input(corpus)
    elif  sys.stdin.isatty():
        logging.error("corpus file not found !")
        exit(0)
    else:
        iterator = sys.stdin

        
    set_start_method("forkserver")

    if add_stop:
        from  nlptools.resources import my_stopword_file as stopword_file
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
    keywords_dict = os.path.join(resource_dir, matcher_dico)
    if matcher_dico: 
        #check name file
        norm_list=[norm]         
        if not (os.path.isfile(keywords_dict)):
            raise ValueError(keywords_dict)
        
    # prepare config Spacy pipeline
    # config Spacy pipeline must be compatible with the resource format (lemma,lower,raw)
    if norm == "lemma": # fr
        nlp = spacy.load(modele_init_fr, disable=["ner", "parser", "textcat"])
        nlp.max_length = 2000000  # or higher

    elif norm == "lower":
        nlp = spacy.blank(language)
        nlp.max_length = 1000000  # or higher
        
    elif norm == "raw":
        nlp = spacy.blank(language)
        nlp.max_length = 1000000  # or higher
        
    else:
        msg = "Can't Find parameter {}".format(norm)
        logging.error(msg)
        raise IOError()

    logging.info(f"LOAD DICO ......")
    logging.info(f" {keywords_dict}")
    logging.info(f" PARM [norm:{norm}][format:{format}]")

    # Configure the flash matcher
    # add Matcher_flash at the end of spacy pipe
    Matcher =  MatcherFlash (
        
        prefix= prefix,
        output= output,
        keywords_dict= keywords_dict,
        case_sensitive= False,
        stopword_file= stopword_file,
        format= format,
        text_format= norm 
    )

    one_run = Run_tagger(nlp, Matcher, input)    
    #logging.info(f" len(DICO) charged : {Matcher_flash.size_voc}")

    i = 0
    logging.info(f"PROCESS CORPUS ...")
    with Pool(core) as pool:

        for result in pool.map(one_run.run_tagger, iterator):
            # output
            if result:
                sys.stdout.write(result)
                sys.stdout.write("\n")
            i += 1

    logging.info(
        f"  Number of traited documents : {i} in times { (time() - start_time)/60} secondes \n"
    )


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
        
