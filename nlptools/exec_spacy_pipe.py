#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:46:45 2020
@author: stephane schneider

""" 
import logging
import spacy
import lemminflect
import json
import os
import re
import stanza
import spacy_stanza
from configparser import ConfigParser
from lefff import getLefff
from nlptools.tools import to_list
import warnings

# desactive les logs
warnings.filterwarnings("ignore")

class exec_spacy_pipe_en(object):

    show = "doc"

    def __init__(self, pipe=None, ini_file=None, ini_param=None,  show=None, format=None):
   
        pipe_list_en = [
            "termMatcher",
            "NPchunker",
            "POStagger",
            "POStaggerStanza",
            "NPchunkerDP",
        ]

        if pipe not in pipe_list_en:
            raise ValueError("invalid pipe name or language setting")
        if show is None:
            self.show = exec_spacy_pipe_en.show
        else:
            self.show = show

        from nlptools.models import modele_init_en
        
        self.format = format

        # initialisation des parsers selon un fichier de configuration config.ini
        configINI = ConfigParser()

        if ini_file:
            f = ini_file
        else:
            _local_path = os.path.dirname(os.path.abspath(__file__))
            f = os.path.join(_local_path, "config_en.ini")

        if os.path.isfile(f):
            configINI.read(f)
        else:
            raise ValueError("config file *.ini not found")

        # parcourir les valeurs et surcharger les valeurs de configINI par des valeurs
        #  passées dans ini_parm
        configPARAM = ConfigParser()
        if ini_param:

            try: 
                configPARAM.read_dict(json.loads(ini_param))
            except Exception as err:

                print("Error lors de la phase d'initialisation : lecture valeur -param impossible")
                exit(err)
            
            configINI.update(configPARAM) 

        # Association et verification des fichiers de ressources
        if configINI.get("termMatcher", "termMatcher_vocabulary") == "MX_jsonl_porter":
            from nlptools.resources import MX_jsonl_porter as termMatcher_vocabulary
        else:
            if (
                configINI.get("termMatcher", "termMatcher_vocabulary")
                == "MX_jsonl_snowball"
            ):
                from nlptools.resources import (
                    MX_jsonl_snowball as termMatcher_vocabulary,
                )
            elif (
                    configINI.get("termMatcher", "termMatcher_vocabulary")
                    == "MX_jsonl_lemme"
                ):
                    from nlptools.resources import (
                        MX_jsonl_lemme as termMatcher_vocabulary,
                    )
            elif (
                configINI.get("termMatcher", "termMatcher_vocabulary")
                    == "MX_jsonl_lemme_test"
                ):
                    from nlptools.resources import (
                        MX_jsonl_lemme_test as termMatcher_vocabulary
                )
            else:
                raise ValueError("terminology is ommited !")
        
        # for NPchunker
        if configINI.get("NPchunker", "NPchunker_rules") == "NPchunker_rules_gen":
            from nlptools.resources import NPchunker_rules_gen as NPchunker_rules
        else:
            raise ValueError("NPchunker : rules file is ommited !")

        # traitement des parametres
        self.logger = logging.getLogger(__name__)

        logger1 = logging.getLogger("spacy")
        logger1.setLevel(logging.ERROR)

        self.modele = modele_init_en

        ############   PARAMETRAGE des pipes de traitements
        self.pipe = pipe     
        
        try:
            termMatcher_lemma = configINI.get("termMatcher", "termMatcher_lemma")
            termMatcher_tag = configINI.get("termMatcher", "termMatcher_tag")
            termMatcher_POS_whitelist = to_list(configINI.get("termMatcher", "termMatcher_POS_whitelist"))
            whitelist_tag_lemme =  to_list(configINI.get("POStagger", "POS_whitelist"))
            #blacklist_tag_lemme = in_list(configINI.get("POStagger", "POS_blacklist")) ! pas effectif
            blacklist_NPDP_tag_lemme = configINI.get("NPchunkerDP", "blacklist_NPDP")

        except Exception as err:

            print("Error lors de la phase d'initialisation [lecture fichier .ini]")
            exit(err)

        # TRACE print("1 {} {}".format( whitelist_tag_lemme , type(whitelist_tag_lemme)))
        # POSTAGGING LEMMINFLECT
        if pipe == "POStagger":
            # init dun pipe avec chargement du modele sans parser et ner
            self.nlp = spacy.load(self.modele, disable=["ner"])
            # ajout du tagger au pipe courant
            self.nlp.add_pipe(
                "POStagger",
                name="POStagger",
                config={"whitelist_tag_lemme": whitelist_tag_lemme, "show": self.show, "format":self.format},
                last=True,
            )
            
        # TERMMATCHING SPACY
        if pipe == "termMatcher":
            # init dun pipe avec chargement du "modele"
            if configINI.get("termMatcher", "termMatcher_lemma") == "lemme":
                # cas ou on POStag le texte avant (depend des formes de la ressource a appliquer)
                # init dun modele avec chargement d1 pipe sans parser et ner
                self.nlp = spacy.load(self.modele, disable=["parser", "ner"])
                # ajout du tagger au pipe courant
                self.nlp.add_pipe(
                    "POStagger",
                    name="POStagger",
                    config={
                        "whitelist_tag_lemme": termMatcher_POS_whitelist,
                        "show": "pipe",
                        "format":self.format
                    },
                    last=True,
                )

            # ajout du termMatcher au pipe courant
            self.nlp.add_pipe(
                "termMatcher",
                name="termMatcher",
                config={
                    "show": self.show,
                    "termMatcher_tag": termMatcher_tag,
                    "termMatcher_vocabulary": termMatcher_vocabulary,
                },
                last=True,
            )
      
        # POSTAGGING STANZA
        if pipe == "POStaggerStanza":
        
            self.nlp = spacy_stanza.load_pipeline('en', processors='tokenize,mwt,pos,lemma', verbose = False,  logging_level = 'FATAL')
            
            self.nlp.add_pipe(
                "POStagger",
                name="POStagger",
                config={"whitelist_tag_lemme": whitelist_tag_lemme, "show": self.show,"format":self.format},
                last=True,
            )

        # CHUNKING SPACY
        if pipe == "NPchunker" or pipe == "NPchunkerDP":

            self.nlp = spacy.load(self.modele, disable="[ner]")

            # version regroupement sur POStag
            if pipe == "NPchunker":
                # ajout du chunker au pipe courant
                self.nlp.add_pipe(
                    "NPchunker",
                    name="NPchunker",
                    config={
                        "lang": "en",
                        "NPchunker_rules": NPchunker_rules,
                        "show": self.show,
                        "label": "",
                    },
                    last=True,
                )

        # vesion dependance parcing
        if pipe == "NPchunkerDP":
            # ajout du chunker au pipe courant
            self.nlp.add_pipe(
                "NPchunkerDP",
                name="NPchunkerDP",
                config={
                    "blacklist_NPDP_tag_lemme": blacklist_NPDP_tag_lemme,
                    "show": self.show,
                },
                last=True,
            )

    def __call__(self, text):

        # PATCH text=" ".join(text.strip().split())
        # execution du pipe
        return self.nlp(text)

class exec_spacy_pipe_fr (object):

    show = "doc"

    def __init__(self, pipe=None, ini_file=None, ini_param=None,  show=None, format=None):
        
        pipe_list_fr = [
                "POStagger",
                "POStaggerStanza",
                ]

        if pipe not in pipe_list_fr:
            raise ValueError("invalid pipe name or language setting")

        if show is None:
            self.show = exec_spacy_pipe_fr.show
        else:
            self.show = show

        from nlptools.models import modele_init_fr
        
        self.format = format

        # configuration du componsant
        configINI = ConfigParser()
        if ini_file:
            f = ini_file
        else:
            _local_path = os.path.dirname(os.path.abspath(__file__))
            f = os.path.join(_local_path, "config_fr.ini")

        if os.path.isfile(f):
            configINI.read(f)
        else:
            raise ValueError("config_fr.ini not found")

        # parcourir les valeurs et surcharger les valeurs de configINI par des valeurs
        #  passées dans ini_parm
        configPARAM = ConfigParser()
        if ini_param:
            configPARAM.read_dict(json.loads(ini_param))
            configINI.update(configPARAM)  

        # loading du modele
        self.modele = modele_init_fr

        ############   PARAMETRAGE des pipes de traitements
        self.pipe = pipe
  
        try:
            self.whitelist_tag_lemme =  to_list(configINI.get("POStagger", "POS_whitelist"))
            #blacklist_tag_lemme = in_list(configINI.get("POStagger", "POS_blacklist")) ! pas effectif
        except Exception as err:
            print("Error lors de la phase d'initialisation [lecture fichier .ini]")
            exit(err)

        if pipe == "POStaggerStanza":
            
                self.nlp = spacy_stanza.load_pipeline('fr', processors='tokenize,mwt,pos,lemma', verbose = False,  logging_level = 'FATAL')
                
                self.nlp.add_pipe(
                    "POStagger",
                    name="POStagger",
                    config={"whitelist_tag_lemme": self.whitelist_tag_lemme, "show": self.show,"format":self.format},
                    last=True,
                )

        if pipe == "POStagger":
            
            # init dun pipe avec chargement du modele sans parser et ner
            self.nlp = spacy.load(self.modele, disable=[ "ner"])
            
            # ajout du tagger au pipe courant
            self.nlp.add_pipe(
                "lefff_french_tagger",
                last=True,
            )
            self.nlp.add_pipe(
                "lefff_french_lemmatizer",
                after="lefff_french_tagger"
            )
            

    def __call__(self, text):
        # PATCH text=" ".join(text.strip().split())
        # execution du pipe
    
        if self.pipe == "POStagger":
            return getLefff (self.nlp(text), self.show, self.whitelist_tag_lemme, self.format)
        
        if self.pipe == "POStaggerStanza":
            return self.nlp(text)
        


        

        


