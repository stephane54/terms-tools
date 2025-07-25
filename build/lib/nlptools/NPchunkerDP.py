#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
# -*- coding: utf-8 -*-
#
# from . import nlp
import logging
from spacy.language import Language
from nlptools.tools import tiretb, cr, space, tireth, tab
import json

# chunker a base de regles
@Language.factory(
    "NPchunkerDP",
    default_config={"blacklist_NPDP_tag_lemme":"", "show": "doc"},
)
def create_NPchunkerDP_component(
    nlp: Language, name: str, blacklist_NPDP_tag_lemme: str, show: str
):
    return NPchunkerDP(nlp, blacklist_NPDP_tag_lemme, show)

class NPchunkerDP(object):

    name = "NPchunkerDP"

    def __init__(self, nlp, blacklist_NPDP_tag_lemme, show):

        self.nlp = nlp
        self.show = show
        self.listTAG = blacklist_NPDP_tag_lemme

    def __call__(self, doc):

        list_chunkDP = []
        sep=""
        if self.show == "doc":
            sep = tiretb
        else:
            sep = space

        # on boucle sur tous les noun chunk
        # les mot donc la POS appartient à list5TAG sont exclus
        for chunk in doc.noun_chunks:
            list_chunkDP.append(
                    (
                    sep.join(
                        [
                            token.text
                            for token in doc[chunk.start : chunk.end]
                            if (token.pos_ not in self.listTAG) and token
                        ]
                    )
                    ,
                    sep.join(
                        [
                            token.lemma_
                            for token in doc[chunk.start : chunk.end]
                            if (token.pos_ not in self.listTAG) and token
                        ]
                    )
                    ,str(chunk.start )+tireth+str(chunk.end)
                    )
            )

        #print([x for x in list_chunkDP])
        #exit (1)
        # TRACE
        # print(chunk.text, chunk.root.text, chunk.root.dep_,chunk.root.head.text)
        # print("TEXT=",chunk.text,";ROOT=",chunk.root.text,";DEP=",chunk.root.dep_,";HEAD=",chunk.root.head.text, chunk.start, chunk.end)
        # for token in doc[chunk.start:chunk.end]:
        #     print(token.text,":", token.pos_,":", token.is_stop)
        #####
        if self.show == "list":

            return cr.join( [ elt[0]+tab+elt[1]+tab+elt[2] for elt in list_chunkDP ] )

        if self.show =="doc":

            return space.join( [ elt[1] for elt in list_chunkDP ] )

        if self.show =="json":
            
            return(json.dumps( [{"text":elt[0], "lemma":elt[1], "idx":elt[2]} for elt in list_chunkDP]))
