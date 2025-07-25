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
    getEnts,
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

        self.tag = termMatcher_tag

        # definition du module de matching
        if len(termMatcher_vocabulary) == 0:
            self.ruler = EntityRuler(
                nlp, overwrite_ents=True, phrase_matcher_attr="lemma"
            )
        else:
            self.ruler = EntityRuler(
                nlp, overwrite_ents=True, phrase_matcher_attr="LEMMA"
            )
            self.ruler = EntityRuler(
                nlp)
            # load le dictionnaire au format jsonl 
            #TRACE  print('DEBUT LOAD DICO')
            self.ruler.from_disk(termMatcher_vocabulary)
            #TRACE print('FIN LOAD DICO')

    def __call__(self, doc):
        # execution du matcher
        self.rules = self.ruler(doc)
        self.rules_len = len(self.rules)
        return (doc)
 
    # attention renvoie tous les ents
 

    # renvoi la liste ds termes trouves
def display_matches(doc, show):
    
    def scan_termMatch(doc):

        for ent in  doc.ents:

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
        ):  # trie marche pas !
            # text = segment textuel du matche
            # lemma = forme du texte qui a servi pour le matching
            # label = ici, label du gaz
            # id = identifiant dans le gaz
            en={}
            en["idx"]=dict(zip(["start","end"],[str(start),str(end)]))
            en["match"]=dict(zip(["id", "ul", "term"],[idt, oneMcMark(text, space), oneMcMark(lemma, space)]))
            list_terms.append(en)
            
        # ajout du texte annotaté
        #result=[]
        #OneResult={} 
        #OneResult["terms"]=list_terms            
        #OneResult["doc"]=getEnts(doc, self.tag)
        #return([OneResult])
        return(list_terms)
                

    list_terms = []

    # liste des termes tsv avec idx
    if show == "list":
        for label, text, lemma, idt, start, end in self.scan_termMatch(
            doc
        ):  # trie marche pas !
            # label = ici, label du gaz
            # start-end
            # text = segment textuel du matche
            # lemma = forme lemmatique de text qui a servi pour le matching
            # id = identifiant dans le gaz
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

        return getEnts(doc, self.tag)

# Affiche le resultat du matching
def getMatcherRules(matcher):

    print("matcher rules")

    for item in matcher:
        print(item)
