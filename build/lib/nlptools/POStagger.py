#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
import logging
from nlptools.tools import cleanTokenLenght, space, readCsvBz2, getDocPos, doc_remove_pos, getDicoPos, getDicoAnnot, clean_terms
from nlptools.tools import list_attr_spacy
from spacy.language import Language
from spacy.tokens import Doc
from json import dumps

@Language.factory(
    "POStagger", default_config={"whitelist_tag_lemme": "", "show": "doc", "format":""}
)
def create_POStagger_component(
    nlp: Language, name: str, whitelist_tag_lemme: list, show: str, format:str
):
    return POStagger(nlp, whitelist_tag_lemme, show, format)


class POStagger(object):

    def __init__(self, nlp, list_cat, show, format):

        self.nlp = nlp
        self.list_cat = list_cat
        self.show = show
        self.format = format
        
    def __call__(self, doc):

        if len(self.list_cat) != 0:
            
            doc = doc_remove_pos (doc, self.list_cat, list_attr_spacy, kind="black" )
            
            
        if self.format == "terms":    
            
            doc = clean_terms(doc)
        

        if self.show == "doc":

            list_lemme = []

            # filtre sur une liste de POS (self.list_cat)
            for token in doc:
                list_lemme.append(token.lemma_)

            # output text avec flow de lemmes
            return space.join(list_lemme)

        if self.show == "list":
            
            # outpu list
            return getDocPos(doc)
        
        if self.show == "dico_pos":
            
            # output list
            return getDicoPos(doc)
        
        if self.show == "dico_annot":
            
            # output list
            return getDicoAnnot(doc)
       
        """ MUTATE
        if self.show == "dico_inflect":
            
            # output list
            return getDicoInflect(doc)
       """
        if self.show == "json":
            
            # output json
            return (dumps(Doc.to_json(doc)['tokens'], ensure_ascii=False))
  

        if self.show == "pipe":

            return doc
