
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider

Current mapping used spaCy to Lefff is :

{
    "ADJ": "adj",
    "ADP": "det",
    "ADV": "adv",
    "DET": "det",
    "PRON": "cln",
    "PROPN": "np",
    "NOUN": "nc",
    "VERB": "v",
    "PUNCT": "poncts"
}

"""
# ADJ 	   adjective
# ADJWH	   interrogative adjective
# ADV	   adverb
# ADVWH	   interrogative adverb
# CC	   coordination conjunction
# CLO	   object clitic pronoun
# CLR	   reflexive clitic pronoun
# CLS	   subject clitic pronoun
# CS	   subordination conjunction
# DET	   determiner
# DETWH	   interrogative determiner
# ET	   foreign word
# I	   interjection
# NC	   common noun
# NPP	   proper noun
# P	   preposition
# P+D	   preposition+determiner amalgam
# P+PRO	   prepositon+pronoun amalgam
# PONCT	   punctuation mark
# PREF	   prefix
# PRO	   full pronoun
# PROREL	   relative pronoun
# PROWH	   interrogative pronoun
# V	   indicative or conditional verb form
# VIMP	   imperative verb form
# VINF	   infinitive verb form
# VPP	   past participle
# VPR	   present participle
# VS	   subjunctive verb form
from nlptools.tools import blanc, cr, tab
from spacy_lefff import LefffLemmatizer, POSTagger
from spacy.language import Language
from json import dumps
from spacy.tokens import  Doc

@Language.factory('lefff_french_lemmatizer' )
def create_french_lemmatizer(nlp, name):
    return LefffLemmatizer(after_melt=True, default=True)

@Language.factory('lefff_french_tagger')
def create_french_tagger(nlp, name):
    return POSTagger()

def getLefff (doc, show, tagList):

    list_token = []
    list_lemme = []
    tag= ['lemma', 'pos']

    # TRACE print(tagList, type(tagList), len(tagList))
    if not(tagList):
        
        for d in doc:

            list_token.append(dict(zip(tag,(d._.lefff_lemma, d._.melt_tagger,))))
            list_lemme.append(d._.lefff_lemma)
    else:
        for d in doc:
            if d._.melt_tagger in tagList:

                list_token.append(dict(zip(tag,(d.text, d._.melt_tagger, d._.lefff_lemma, d.is_stop))))
                list_lemme.append(d._.lefff_lemma)                
        
    if show == "list":
        list_ = []
        
        for token in list_token:

            if token['pos']:  
                list_.append(tab)
                list_.append("lemma:[" + token['lemma'] + "]")
                list_.append(tab)
                list_.append("pos:[" + token['pos'] + "]")
                list_.append(tab)
                list_.append(cr)

        return blanc.join(list_)
        
    if show == "dico_pos":        
        list_lemma = []
        list_text = []
        list_pos = []

        for token in doc:
            # if token._.stem:
            #   list_stem.append(token._.stem)
            if token.pos_:
                list_lemma.append(token.lemma_)      
                list_text.append(token.text) 
                list_pos.append(token.pos_) 
            
                return (blanc.join(list_text)+                
                        tab+blanc.join(list_lemma)+
                        tab+blanc.join(list_pos)+
                        tab+(dumps(list_token, ensure_ascii=False)))
    
        
    if show == "json":

        #print(doc[0]._.lefff_lemma)
        # output json
        return dumps(list_token, ensure_ascii=False)
    
    if show == "pipe":

        return doc 

    if show == "doc":

        return blanc.join(list_lemme)

    #return(list())


