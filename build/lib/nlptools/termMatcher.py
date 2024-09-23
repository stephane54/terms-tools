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
        "termMatcher_tag": "VOC",  # tag prefix qui marque le terme trouvé
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
            self.show = show
        else:
            self.show = "doc"

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
            self.ruler.from_disk(termMatcher_vocabulary)

    def __call__(self, doc):
        # execution du matcher

        self.rules = self.ruler(doc)
        self.rules_len = len(self.rules)
        self.entities = doc.ents

        return self.getTermMatch(doc)

    def getLenGaz(self):

        return len(self.ruler)

    def showGaz(self):

        for a in enumerate(self.ruler.patterns):
            print(a)

    def add_patterns(self, patterns):

        self.ruler.add_patterns(patterns)

    def getLenMatches(self):

        # ca correspond a quoi ???
        return self.rules_len

    # attention renvoie tous les ents
    def scan_termMatch(self, doc):

        for ent in self.entities:

            yield (ent.label_, ent.text, ent.lemma_, ent.ent_id_, ent.start, ent.end)

    # renvoi la liste ds termes trouves
    def getTermMatch(self, doc):

        list_terms = []
        if self.show == "doc":
            sep = tiretb
        else:
            sep = space

        if self.show == "json":
            for label, text, lemma, idt, start, end in self.scan_termMatch(
                doc
            ):  # trie marche pas !
                # text = segment textuel du matche
                # lemma = forme du texte qui a servi pour le matching
                # label = ici, label du gaz
                # id = identifiant dans le gaz
                
                    en={ }
                    en["idx"]=str(start)+ tireth+ str(end)
                    en["text"]=oneMcMark(text, space)
                    en["lemma"]=oneMcMark(lemma, space)
                    en["idt"]=idt
                    list_terms.append(en)

            return(json.dumps(list_terms))

        list_terms = []

        if self.show == "list":
            for label, text, lemma, idt, start, end in self.scan_termMatch(
                doc
            ):  # trie marche pas !
                # text = segment textuel du matche
                # lemma = forme du texte qui a servi pour le matching
                # label = ici, label du gaz
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
                    + space
                    + idt
                )
            # liste dedoublonnée
            return cr.join(list(set(cleanWList(list_terms))))

        else:

            return getEnts(doc, self.tag)


# Affiche le resultat du matching
def getMatcherRules(gaz):

    print("matcher rules")

    for item in gaz:
        print(item)
