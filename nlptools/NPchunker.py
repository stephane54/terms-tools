#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane schneider
"""
# -*- coding: utf-8 -*-
#
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from operator import itemgetter
from nlptools.tools import tiretb, blanc, cleanWList, cr, tireth, tab
import json
from spacy.language import Language
from spacy.tokens import  Doc

# chunker a base de regles
@Language.factory(
    "NPchunker",
    default_config={"lang": "en", "NPchunker_rules": "", "show": "doc", "label": ""},
)
def create_NPchunker_component(
    nlp: Language, name: str, lang: str, NPchunker_rules: str, show: str, label: str
):
    return NPchunker(nlp, lang, NPchunker_rules, show, label)


class NPchunker(object):

    name = "NPchunker"

    def __init__(self, nlp, lang, NPchunker_rules, show, label):

        self.nlpPrivate = nlp.vocab
        self.matcher = Matcher(self.nlpPrivate)
        self.langue = lang
        self.show = show
        self.NPchunker_rules = NPchunker_rules

        if label != "":
            self.label = label
        else:
            self.label = NPchunker.name

        self.matcher.add(self.label, self._get_rules_())

    # appel du rules matcher
    def __call__(self, doc):

        self.matches = self.matcher(doc)
        self.NOTinclude(doc)  # segment le plus long

        return self.getNPchunk(doc)

    # Définition des regles de chunking - a modifier
    def _get_rules_(self):

        message = "Langue non prise en compte par le module chunk"
        data = []
        if self.langue == "en":

            for line in open(self.NPchunker_rules, "r"):
                if line[0] not in ["#", "\n"]:  # TODO : ameliorer la souplesse parsing
                    data.append(json.loads(line.rstrip()))
            # trace data)
            return data
            # return [{"POS": {"IN": ["NOUN", "PROPN"]}}],[{"TAG": {"IN": ["JJ", "VBG", "VBN"]}}],[{"TAG": {"IN": ["JJ", "VBG", "VBN"]}},{"POS": {"IN": ["NOUN", "PROPN"]}},],[{"POS": {"IN": ["NOUN", "PROPN"]}},{"POS": {"IN": ["NOUN","PROPN"]}},],[{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["PREP", "ADP"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}],[{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["NOUN","PROPN"]}}],[{"TAG": {"IN": ["JJ" , "VBG", "VBN"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}},{"POS": {"IN": ["NOUN", "PROPN"]}}],[{"TAG": {"IN": ["JJ" , "VBG", "VBN"]}},{"TAG": {"IN": ["JJ" , "VBG", "VBN"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}],[{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["PREP", "ADP"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}],[{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["PREP", "ADP"]}}, {"TAG": {"IN": ["JJ" , "VBG", "VBN"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}],[{"TAG": {"IN": ["JJ" , "VBG", "VBN"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["PREP", "ADP"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}],[{"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["PREP", "ADP"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}, {"POS": {"IN": ["CONJ"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}],[{"TAG": {"IN":["JJ" , "VBG", "VBN"]}}, {"POS": {"IN": ["CONJ"]}}, {"TAG": {"IN": ["JJ" , "VBG", "VBN"]}}, {"POS": {"IN": ["NOUN", "PROPN"]}}]
        else:
            return message

    # fonction qui permet de ne garder que le segment le plus long
    def NOTinclude(self, doc):

        data = []

        # recuperation liste de matches
        for match_id, start, end in self.matches:
            string_id = self.nlpPrivate.strings[match_id]  # Get string representation
            data.append((end - start, match_id, start, end))

        # trie : on met les donnees dans l ordre decroissant
        sorted_data = list(sorted(data, key=itemgetter(0), reverse=True))

        # on construit la liste des elements à ne pas garder , la liste to_del tout element qui appartient a un segment  plus long
        # fonction native  self.matches
        #   NB:  on ne traite pas les  segments se chevauchant
        to_del = []

        for i, el1 in enumerate(sorted_data):

            if el1[0] > 1:
                # TRACE print('CHERCHER=',el1[2], el1[3], "==>" , i)

                for n, el2 in enumerate(sorted_data[i + 1 :]):
                    if ((el2[2] >= el1[2]) and (el2[2] <= el1[3])) and (
                        (el2[3] >= el1[2]) and (el2[3] <= el1[3])
                    ):
                        to_del.append(i + n + 1)

        # on dedoublonnage la liste
        to_del = list(set((to_del)))

        # on suppreme les elements inclus
        self.matches = [
            [x[0], x[1], x[2], x[3]]
            for index, x in enumerate(sorted_data)
            if index not in to_del
        ]

        return doc

    def get_matches(self):

        return self.matches

    # Retourne la listes des chunk sous forme de chaine
    def getNPchunk(self, doc):

        # parcour la listes des chunk     
        list_chunk= []
        sep=""

        if self.show == "doc":
            sep = tiretb
        else:
            sep = blanc

        for taille, match_id, start, end in list(
            sorted(self.get_matches(), key=itemgetter(2), reverse=False)
        ):

            lemma_expr = []
            text_expr = []


            if (taille >= 1) and not (
                doc[start].is_stop
            ):  # on filtre les chunk mono qui sont des stop_word

                for token in doc[start:end]:
                    # on ne garde que les lemma_lemma_expr qui ne contiennent que des alphnum pour l instant
                    if token.is_alpha:
                        lemma_expr.append(token.lemma_)  # compose  lemma_expression
                        text_expr.append(token.text)  # compose text_expression

                    else:
                        lemma_expr = []
                        text_expr = []
                        break

                list_chunk.append(
                    ([sep.join(text_expr), sep.join(lemma_expr),  str(start)+tireth+str(end)])
                )  # ajout a la liste des lemma_expression


        # renvoie les chunks dans l ordre sous la forme d une string

        if self.show == "list":

            return cr.join(cleanWList( [elt[0]+tab+elt[1]+tab+elt[2] for elt in list_chunk] ))

        if self.show == "json":
                
            return(json.dumps( [{"text":elt[0], "lemma":elt[1], "idx":elt[2]} for elt in list_chunk]))

        if self.show == "doc":

            return blanc.join(cleanWList( [elt[1] for elt in list_chunk] ))

        else:

            return doc
