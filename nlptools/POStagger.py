#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
import logging
from nlptools.tools import cleanTokenLenght, blanc, readCsvBz2, getDocPos, doc_remove_pos, getDocPosDico, getDicoInflect
from nlptools.tools import list_attr_spacy
from spacy.language import Language
from spacy.tokens import Doc
from json import dumps

@Language.factory(
    "POStagger", default_config={"whitelist_tag_lemme": "", "show": "doc"}
)
def create_POStagger_component(
    nlp: Language, name: str, whitelist_tag_lemme: list, show: str
):
    return POStagger(nlp, whitelist_tag_lemme, show)


class POStagger(object):

    def __init__(self, nlp, list_cat, show):

        self.nlp = nlp
        self.list_cat = list_cat
        self.show = show

    def __call__(self, doc):

        if len(self.list_cat) != 0:

            doc = doc_remove_pos (doc, self.list_cat, list_attr_spacy, kind="black" )
            

        if self.show == "doc":

            list_lemme = []

            # filtre sur une liste de POS (self.list_cat)
            for token in doc:
                #list_lemme.append(token.lemma_+"/"+token.pos_)
                list_lemme.append(token.lemma_)

            # outpu text avec flow de lemmes
            return blanc.join(list_lemme)

        if self.show == "list":
            
            # outpu list
            return getDocPos(doc)
        
        if self.show == "dico_pos":
            
            # output list
            return getDocPosDico(doc)
        
        if self.show == "dico_inflect":
            
            # output list
            return getDicoInflect(doc)

        if self.show == "json":
            
            # output json
            return (dumps(Doc.to_json(doc)['tokens'], ensure_ascii=False))
  

        if self.show == "pipe":

            return doc
