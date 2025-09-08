#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:46:45 2020 
@author: stephane schneider

""" 
import logging
import spacy
import json
import os
import re
import sys
from configparser import ConfigParser
from nlptools.tools import to_list
from spacy.tokens import Doc
import warnings
from nlptools.POStagger import display_postag
from nlptools.termMatcher import display_matches
from nlptools.resources import dico_path

# desactive les logs
warnings.filterwarnings("ignore")

class exec_spacy_pipe_en(object):

    show = "doc"

    def __init__(self, pipe=None, matcher_dico=None, ini_file=None, ini_param=None,  show=None, format=None):
   
        pipe_list_en = [
            "NPchunker",
            "NPchunkerDP",
            "termMatcher",
            "POStagger"
        ]        

        if pipe not in pipe_list_en:
            print(f"ERROR : invalid pipe ({pipe}) name or language (en) setting ")
            sys.exit(f"exit")
        if show is None:
            self.show = exec_spacy_pipe_en.show
        else:
            self.show = show
        
        self.format = format
        
        # Select MODEL SPACY
        from nlptools.models import modele_init_en
        self.modele = modele_init_en

        ############   PARAMETRAGE des pipes de traitement en
        # initialisation des parsers selon un fichier de configuration config.ini
        configINI = ConfigParser()

        if ini_file:
            f = ini_file
        else: # config par defaut si non definie
            _local_path = os.path.dirname(os.path.abspath(__file__))
            f = os.path.join(_local_path, "config_en.ini")

        if os.path.isfile(f):
            configINI.read(f)
        else:
            raise ValueError("config file *.ini not found")

        # parcourir les valeurs et les surcharge par les valeurs passées dans ini_parm
        configPARAM = ConfigParser()
        if ini_param:

            try: 
                configPARAM.read_dict(json.loads(ini_param))
            except Exception as err:

                print("Error lors de la phase d'initialisation : lecture valeur -param impossible")
                exit(err)
            
            configINI.update(configPARAM) 

        # for NPchunker

        if configINI.get("NPchunker", "NPchunker_rules_en") == "NPchunker_rules_gen_en":
            from nlptools.resources import NPchunker_rules_gen_en as NPchunker_rules_en
        else:
            raise ValueError("NPchunker : rules file is ommited !")

        # traitement des parametres
        self.logger = logging.getLogger(__name__)

        logger1 = logging.getLogger("spacy")
        logger1.setLevel(logging.ERROR)

        self.pipe = pipe     
        
        try:
            #termMatcher_lemma = configINI.get("termMatcher", "termMatcher_lemma")
            termMatcher_tag = configINI.get("termMatcher", "termMatcher_tag")
            termMatcher_POS_list = to_list(configINI.get("termMatcher", "termMatcher_POS_list"))
            list_tag_lemme =  to_list(configINI.get("POStagger", "POS_list"))
            clean_mode_pos=configINI.get("POStagger", "clean_mode")
            clean_mode_term=configINI.get("termMatcher", "clean_mode")
            blacklist_NPDP_tag_lemme = configINI.get("NPchunkerDP", "blacklist_NPDP")

        except Exception as err:

            print("Error lors de la phase d'initialisation [lecture fichier .ini]")
            exit(err)
      
        # POSTAGGING  
        if pipe == "POStagger":
            
            #self.nlp = spacy_stanza.load_pipeline('en', processors='tokenize,pos, lemma', verbose = False,  logging_level = 'FATAL',pos_batch_size=10000)
            self.nlp = spacy.load(self.modele, disable=["ner"])
            
            self.nlp.add_pipe(
                    "lower_case_lemmas",
                    name="lower_case_lemmas",
                )
            
            self.nlp.add_pipe(
                "ViewPOStagger",
                name="ViewPOStagger",
                config={"list_tag_lemme": list_tag_lemme, "clean_mode": clean_mode_pos,"format":self.format},
                last=True,
            )
             
        # TERMMATCHER  
        if pipe == "termMatcher":
            if configINI.get("termMatcher", "termMatcher_lemma") == "lemme":
                
                # LOAD MATCHER
                #TRACE print("BEGIN LOAD MODEL")
                #self.nlp = spacy_stanza.load_pipeline('en', processors='tokenize,pos,lemma,depparse', verbose = False,  logging_level = 'FATAL', pos_batch_size=10000)
                self.nlp = self.nlp = spacy.load(self.modele, disable=["parser", "ner"])
                #TRACE print("FIN LOAD MODEL")
                self.nlp.add_pipe(
                    "lower_case_lemmas",
                    name="lower_case_lemmas",
                )

                self.nlp.add_pipe(
                    "ViewPOStagger",
                    name="ViewPOStagger",
                    config={"list_tag_lemme":termMatcher_POS_list,
                            "clean_mode": clean_mode_term},
                    last=True,
                )
            
                self.nlp.add_pipe(
                "termMatcher",
                name="termMatcher",
                config={
                    "show": self.show,
                    "termMatcher_tag": termMatcher_tag,
                    "termMatcher_vocabulary": matcher_dico,
                },
                last=True,
                )
                
            else:
                raise ValueError("Parameter termMatcher_lemma=stem are requiried for matcher_ stanza")

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
                        "NPchunker_rules": NPchunker_rules_en,
                        "show": self.show,
                        "label": "",
                    },
                    last=True,
                )

        # version dependance parcing
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

        # PATCH  text=" ".join(text.strip().split())
        # Execution du pipe Stanza
        doc = self.nlp(text)
        
        if self.pipe == "POStagger":
            
            return (display_postag (doc, self.show))
        
        if self.pipe == "termMatcher":
            
            return (display_matches(doc, self.show))
        
    

class exec_spacy_pipe_fr (object):

    show = "doc"

    def __init__(self, pipe=None, matcher_dico=None, ini_file=None, ini_param=None,  show=None, format=None):
               
        #  nlp fr component list 
        pipe_list_fr = [
                "termMatcher",
                "POStagger",
                ]

        if pipe not in pipe_list_fr:
            print(f"ERROR : invalid pipe ({pipe}) name or language (fr) setting ")
            sys.exit(f"exit")
            
        if show is None:
            self.show = exec_spacy_pipe_fr.show
        else:
            self.show = show

        self.format = format
        
        # select le modele fr
        from nlptools.models import modele_init_fr
        self.modele = modele_init_fr
        
        ############   PARAMETRAGE des pipes de traitements FR
        # LOAD configuration du composant par le .ini
        configINI = ConfigParser()
        
        
        
        if ini_file:
            f = os.path.join(dico_path ,"config", ini_file)    
        else:
            _local_path = os.path.dirname(os.path.abspath(__file__))
            f = os.path.join(_local_path, "config_fr.ini")

        if os.path.isfile(f):
            configINI.read(f)
        else:
            raise ValueError("config_fr.ini not found")

        # parcourir les valeurs et les surcharger  par des valeurs passées dans ini_parm
        configPARAM = ConfigParser()
        if ini_param:
            configPARAM.read_dict(json.loads(ini_param))
            configINI.update(configPARAM)  

        self.pipe = pipe
  
        try:
            self.list_tag_lemme =  to_list(configINI.get("POStagger", "POS_list"))
            clean_mode_pos=configINI.get("POStagger", "clean_mode")
            clean_mode_term=configINI.get("termMatcher", "clean_mode")
            termMatcher_POS_list = to_list(configINI.get("termMatcher", "termMatcher_POS_list"))
            termMatcher_tag = configINI.get("termMatcher", "termMatcher_tag")
            
        except Exception as err:
            print("Error lors de la phase d'initialisation [lecture fichier .ini]")
            exit(err)
            
            
        # POSTAG
        if pipe == "POStagger":
            
                self.nlp = spacy.load(self.modele, disable=["ner"])
    
                self.nlp.add_pipe(
                    "lower_case_lemmas",
                    name="lower_case_lemmas",
                )
    
                self.nlp.add_pipe(
                    "ViewPOStagger",
                    name="ViewPOStagger",
                    config={"list_tag_lemme": self.list_tag_lemme,  "clean_mode":  clean_mode_pos, "format":self.format},
                    last=True,
                ) 
             
        # TERMMATCHER
        if pipe == "termMatcher":
            
            if configINI.get("termMatcher", "termMatcher_lemma") == "lemme":
            
                #self.nlp = spacy_stanza.load_pipeline('fr', processors='tokenize,pos,lemma,depparse', verbose = False,  logging_level = 'FATAL', pos_batch_size=10000)
                self.nlp = self.nlp = spacy.load(self.modele, disable=["parser", "ner"])
                
                self.nlp.add_pipe(
                    "lower_case_lemmas",
                    name="lower_case_lemmas",
                )
                
                self.nlp.add_pipe(
                    "ViewPOStagger",
                    name="ViewPOStagger",
                    config={"list_tag_lemme":termMatcher_POS_list, "clean_mode":  clean_mode_term},
                    last=True,
                )
                    
                self.nlp.add_pipe(
                "termMatcher",
                name="termMatcher",
                config={
                    "show": self.show,
                    "termMatcher_tag": termMatcher_tag,
                    "termMatcher_vocabulary": matcher_dico,
                },
                last=True,
                )
            else:
                raise ValueError("Parameter termMatcher_lemma=stem are requiried for matcher_ +")
         

    def __call__(self, text):
        
        # Execution du pipe stanza
            
        doc = self.nlp(text)
        
        if self.pipe == "POStagger":
            
            return (display_postag (doc, self.show))
        
        if self.pipe == "termMatcher":
            
            return doc
        