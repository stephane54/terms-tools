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
    "ViewPOStagger", default_config={"list_tag_lemme": "", "clean_mode":"", "show": "doc", "format":""}
)
def create_POStagger_component(
    nlp: Language, name: str, list_tag_lemme: list, clean_mode: str, show: str, format:str
):
    return ViewPOStagger(nlp, list_tag_lemme, clean_mode, show, format)


class ViewPOStagger(object):

    def __init__(self, nlp, list_cat,clean_mode, show, format):

        self.nlp = nlp
        self.clean_mode = clean_mode
        self.list_cat = list_cat
        self.show = show
        self.format = format
        
    def __call__(self, doc):

        if self.format == "terms":    
            
            doc = clean_terms(doc)


        if len(self.list_cat) != 0:
            
            #TRACE print(self.list_cat,self.clean_mode)
            doc = doc_remove_pos (doc, self.list_cat, list_attr_spacy, kind=self.clean_mode )        
        

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

        if self.show == "json":
            
            # output json
            return (Doc.to_json(doc)['tokens'])
  

        if self.show == "pipe":

            return doc
