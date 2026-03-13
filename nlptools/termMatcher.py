#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
from spacy.pipeline import EntityRuler
from nlptools.tools import (
    oneMcMark,
    tireth,
    tab,
    tiretb,
    space,
    cr,
    cleanWList,
    getEntsInDoc,
)
from spacy.language import Language
from spacy.tokens import  Doc, DocBin
import json

# Composant Matcher de termes de type entityRuler, alimenté par une liste de termes
@Language.factory(
    "termMatcher",
    default_config={
        "show": "doc",
        "termMatcher_tag": "TERM",  # tag prefix qui marque le terme trouvé # param ; config.ini [termMatcher] termMatcher_tag=TAG
        "termMatcher_vocabulary": "", #vocabulaire utilisé
    },
)
def create_termMatcher_component(
    nlp: Language,
    name: str,
    show: str,
    termMatcher_tag: str,
    termMatcher_vocabulary: str,
):
    return TermMatcher(nlp, show, termMatcher_tag, termMatcher_vocabulary)


class TermMatcher(object):

    name = "termMatcher"

    rules_len = 0

    def __init__(self, nlp, show, termMatcher_tag, termMatcher_vocabulary):

        if len(show) > 0:
            show = show
        else:
            show = "doc"

        tag = termMatcher_tag

        # definition du module de matching
        if len(termMatcher_vocabulary) == 0:
            self.ruler = EntityRuler(
                nlp, overwrite_ents=True, phrase_matcher_attr="lemma",validate=True
            )
        else:
            self.ruler = EntityRuler(
                nlp, overwrite_ents=True, phrase_matcher_attr="LEMMA",validate=True
            )
            self.ruler = EntityRuler(nlp)
            # load le dictionnaire au format jsonl 
            #TRACE  print('DEBUT LOAD DICO')
            self.ruler.from_disk(termMatcher_vocabulary)
            #TRACE print('FIN LOAD DICO')

    def __call__(self, doc):
        # execution du matcher
        self.rules = self.ruler(doc)
        self.rules_len = len(self.rules)
        return (doc)
    
# renvoi la liste ds termes trouves
# attention renvoie tous les ents

def display_matches(doc, show, tag):
    
    def scan_termMatch(doc):
            # ex: quality | Qualities | quality | http://data.loterre.fr/ark:/67375/P66-B1TWZGXG-D | 16 17
            # effet de l'oubli subséquent | effets de l'oubli subséquent | effet de leoubli subséquent | http://data.loterre.fr/ark:/67375/P66-RN0GL886-1 | 314 319
            # label = champ "label" du dico  = KEY spacy = en general le term
            # text = le texte exact du match
            # lemma = forme lemmatisée du texte qui a servi pour le matching
            # champ "id" du dico = identifiant dans le gaz
            # offset : start-end
        for ent in  doc.ents:
            #TRACE
            #print(ent.start, ent.end,"|",ent.text, "|",ent.label_,"|",  ent.lemma_,"|", ent.ent_id_,"|")
            yield (ent.label_, ent.text, ent.lemma_, ent.ent_id_, ent.start, ent.end)  
             
    list_terms = []

    # format indoc : termes reconnus marques dans le texte
    if show == "doc":
        sep = tiretb
    else:
        sep = space
    
    # format standoff : liste de termes reconnus en json
    if show == "json":
                    
        for label, text, lemma, idt, start, end in scan_termMatch(
            doc
        ):  
            en={}
            en["idx"]=dict(zip(["start","end"],[str(start),str(end)]))
            en["match"]=dict(zip(["id", "text", "term"],[idt, oneMcMark(text, space), oneMcMark(label, space)]))
            list_terms.append(en)
            
        # ajout du texte annotaté
        list_terms.append(dict(zip(["doc"],[getEntsInDoc(doc)])))
        
        return(list_terms)        

    list_terms = []

    # liste des termes tsv avec idx
    if show == "list":
        for label, text, lemma, idt, start, end in scan_termMatch(
            doc
        ):  # trie marche pas !
   
            list_terms.append(
                str(start)
                + tireth
                + str(end)
                + tab
                + oneMcMark(text, sep)
                + tab
                + oneMcMark(lemma, sep)
                + tab
                + oneMcMark(label, sep)
                + tab
                + idt
            )
        # liste dedoublonnée
        return cr.join(list(set(cleanWList(list_terms))))

    else:

        return getEntsInDoc(doc)

# Affiche le resultat du matching
def getMatcherRules(matcher):
    # TRACE
    #print("matcher rules")

    for item in matcher:
        print(item)
