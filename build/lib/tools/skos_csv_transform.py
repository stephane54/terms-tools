#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:57:36 2020

@author: steph

   Genere un vocab a plat idt + label (en tsv ou jsonl) a partir d une vesion csv riche

exemple :

    python3 $HOME/app/NLP_tools/tools/skos_csv_transform.py /applis/commun/data/termino/MX2016.csv -l "en" -e "UTF-8" -f "jsonl" -t "all" -s lemme

"""
from config.config import configINI
import plac
import csv
import json
import sys
from spacy.lang.en import English
from parsers.stemmer import stemmer
from parsers import modele_init_en
from parsers.POStagger import POStagger
from parsers.tools import *


@plac.annotations(
    fcsv=("Path to csv file", "positional", None, str),
    labelpref=("add the pref form of the concept [default no]", "flag", "p"),
    langue=("Language [default en]", "option", "l", str, ["en", "fr"]),
    encoding=("encoding [default UTF-8]", "option", "e", str, ["UTF-8", "ISO-8859-1"]),
    format=(
        "format of the result [default jsonl]",
        "option",
        "f",
        str,
        ["jsonl", "tsv"],
    ),
    labelselect=(
        "type of label to get [default all]",
        "option",
        "t",
        str,
        ["all", "pref"],
    ),
    tokenform=(
        "token form:  stem, lemme, text  [default text]",
        "option",
        "s",
        str,
        ["stem", "lemme", "text"],
    ),
)
# ex: python3 skos_csv_transform.py $HOME/data/skos/geosciences.csv -e MX -l en -f jsonl
# INPUT :categories attendues dans le csv
#   ID,prefLabelFre,prefLabelEng,altLabelFre,altLabelEng,
#   hiddenLabelFre,hiddenLabelEng,broaderFre,broaderEng,semanticCategoryFre,semanticCategoryEng

# OUTPUT en json lite (jsonl):
# {"label":"preventive measures ,"prefLabelEng":"preventive measure"}
# {"label":"activity","prefLabelEng":"activity"}

# OUTPUT en json lite(tsv):
# TODO : controle du code langue d apres liste categories


def main(
    tokenform,
    labelpref,
    fcsv,
    langue="en",
    encoding="UTF-8",
    format="jsonl",
    labelselect="all",
):

    lang = "_" + langue

    NoCat = [
        "semCategory" + lang,
        "ID",
        "hiddenLabel" + lang,
        "notation",
        "subjectField" + lang,
        "scopeNote",
    ]

    if labelselect == "all":

        cat = ["prefLabel" + lang, "hiddenLabel" + lang, "altLabel" + lang]

    else:
        cat = ["prefLabel" + lang]

    delimitateur = "|"

    # definition dun stemmer
    if tokenform == "stem":

        # chargement du modele angalis dans spacy
        nlp = English()
        # choix du stemmer
        stemmer_algo = configINI.get("termMatcher", "termMatcher_stemmer")
        # initialisation du cpst stemmer
        stem = stemmer(nlp, stemmer_algo, "")
        # ajout du stemmer au pipe courant
        nlp.add_pipe(stem, name="stemmer", first=True)
    else:
        # definition dun lemmatiseur
        if tokenform == "lemme":

            # liste POS tag à garder
            POS_whitelist = (
                "ADJ",
                "NOUN",
                "PROPN",
                "ADP",
                "ADV",
                "AUX",
                "CONJ",
                "CCONJ",
                "DET",
                "INTJ",
                "PART",
                "PRON",
                "X",
                "NUM",
                "SYM",
                "PUNCT",
            )
            # chargement du moedele spacy
            nlp = spacy.load(modele_init_en, disable=["parser", "ner"])
            # initialisation du cpst tagger
            tagger = POStagger(nlp, POS_whitelist)
            # ajout du tagger au pipe courant
            nlp.add_pipe(tagger, name="print_lemme", last=True)

    # encoding='ISO-8859-1'
    # encoding='UTF-8'
    with open(fcsv, newline="", encoding=encoding) as csvfile:

        linereader = csv.DictReader(
            csvfile,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
            skipinitialspace=True,
        )

        # get une ligne
        for row in linereader:

            ID = "<" + row["ID"] + ">"
            preflabel = row[cat[0]]

            # get chaque paire key=value
            for (category, libelle) in row.items():

                # if label and category and category not in NoCat and '_en' not in category:
                if libelle and category in cat:
                    # cas champ multivalu
                    multi = libelle.split(delimitateur)

                    for phrase in multi:

                        if tokenform in ["stem", "lemme"]:
                            doc = nlp(phrase)
                            list_word = []
                            list_word.append("[")
                            for token in doc:
                                # if token._.stem:
                                #   list_word.append(token._.stem)
                                if token.lemma_:
                                    list_word.append(
                                        '{"lemma":'
                                        + json.dumps(token.lemma_).strip()
                                        + "},"
                                    )
                            list_word.append("]")
                            lemma_value = blanc.join(list_word)
                            lemma_value = (
                                lemma_value[0:-3] + lemma_value[-2:]
                            )  # on enleve la derniere ","

                        else:  # cas tokenform=text
                            lemma_value = json.dumps(phrase).strip()

                        if format == "jsonl":

                            if labelpref:
                                print(
                                    '{"label:"'
                                    + json.dumps(preflabel)
                                    + ',"pattern":'
                                    + lemma_value
                                    + ',"id":"'
                                    + ID.strip()
                                    + ',"pref":"'
                                    + preflabel.strip()
                                    + '"}'
                                )

                            else:
                                print(
                                    '{"label":'
                                    + json.dumps(preflabel)
                                    + ',"pattern":'
                                    + lemma_value
                                    + ',"id":"'
                                    + ID.strip()
                                    + '"}'
                                )

                        if format == "tsv":

                            if labelpref:
                                print(
                                    ID.strip()
                                    + "\t"
                                    + lemma_value.strip()
                                    + "\t"
                                    + preflabel.strip()
                                )

                            else:
                                print(ID.strip() + "\t" + lemma_value.strip())


if __name__ == "__main__":

    plac.call(main)
