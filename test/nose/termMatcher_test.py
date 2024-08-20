#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane
"""
# exemple :  nosetests test/termMatcher_test.py
#
# !!!!!!!!!!!!!!!!!!!!!!!!!   OBSOLETE avec spacy 3 A METTRE A JOUR
from nose.tools import *
from spacy.lang.en import English
from nlptools.tools import *
from nlptools.termMatcher import TermMatcher
from nlptools.stemmer import *
from nlptools.POStagger import *
from nlptools import modele_init_en
from nlptools.resources import MX_jsonl_porter
from nlptools.resources import MX_jsonl_snowball
from nlptools.resources import MX_jsonl_lemme


class termMatcher_test:
    @classmethod
    def setup_class(cls):

        try:
            # TODO error car plus d init globale, il fut fournir le fichier init puor les tests
            cls.termMatcher_POS_whitelist = configINI.get(
                "termMatcher", "termMatcher_POS_whitelist"
            )

        except Exception as err:

            print("Error lors de la phase d'initialisation [lecture fichier .ini]")
            exit(err)

    def termMatch_test_stem(self):
        # attention NER prend le pas sur le gazetteer donc on le desactive
        nlp = spacy.load(modele_init_en, disable=["parser", "tagger", "ner"])
        param = {
            "show": "doc",
            "termMatcher_tag": "MX_",
            "termMatcher_vocabulary": MX_jsonl_snowball,
        }
        termMatch = termMatcher(nlp, **param)
        print("Nombre de pattern:" + str(termMatch.get_len_matches()))

        # more_term = [ {"label": "MX", "pattern": [{"lemma": "Parkison"}, {"lemma": "disease"}], "id": "st1"},
        #         {"label": "MX", "pattern": [{"lemma": "Guam"}, {"lemma": "Parkinson"}, {"lemma":"dementia"}], "id": "st2"},
        #         {"label": "MX", "pattern": [{"lemma": "country"}], "id": "st3"},
        #          ]
        # gaz.add_patterns(more_term)
        nlp.add_pipe(stemmer(nlp, "snowball", "doc"), name="stemmer", first=True)
        nlp.add_pipe(termMatch, name="gazetteer", last=True)

        # trace print("gaz Nbr de patterns :"+str(self.gaz.get_len_gaz()))
        text_in = """The efficiency of utilization of potential donors for organ transplantation in Saudi Arabia: A pilot study . Organ shortage has been the main obstacle in the progress of organ transplantation in Saudi Arabia. The aim of this pilot study was to determine the percentage of potential donors among all deaths in Riyadh hospital intensive care          units (ICUs). Mortality data were collected by a medical professional in each ICU and analyzed on           weekly basis for 1 year (June 2001 through May 2002): The final analysis at the end of the year           showed the number of brain death cases in all hospitals to be 114 out of 542 deaths. Fifty-four percent           occurred in one hospital. Thirty-eight cases were reported to the Saudi Center for Organ Transplantation (33%).           Documentation was completed in only 23 cases (60%). Only four cases became actual donors.           In conclusion, there is underreporting of brain death cases. Dealing with the reported cases           is inefficient since only four cases became actual donors out of 38. Improving the efficiency of ICUs           in dealing with brain death cases (reporting, documentation, maintenance and consent) will require           solving several problems at the medical, administrative, religious, and mass media levels."""
        text_good = """The MX_efficiency of utilization of MX_potential MX_donors for MX_organ MX_transplantation in MX_Saudi_Arabia : A MX_pilot_study . MX_Organ MX_shortage has been the MX_main MX_obstacle in the MX_progress of MX_organ MX_transplantation in MX_Saudi_Arabia . The aim of this MX_pilot_study was to MX_determine the percentage of MX_potential MX_donors among all MX_deaths in Riyadh MX_hospital MX_intensive_care_units (ICUs). MX_Mortality MX_data were MX_collected by a medical professional in each ICU and MX_analyzed on weekly basis for 1 year (June MX_2001 through May MX_2002 ): The final MX_analysis at the MX_end of the year MX_showed the MX_number of MX_brain_death MX_cases in all MX_hospitals to be 114 out of 542 MX_deaths . Fifty-four percent occurred in one MX_hospital . Thirty-eight MX_cases were MX_reported to the Saudi MX_Center for MX_Organ MX_Transplantation (33%). MX_Documentation was MX_completed in only 23 MX_cases (60%). Only four MX_cases became actual MX_donors . In conclusion, there is underreporting of MX_brain_death MX_cases . Dealing with the MX_reported MX_cases is MX_inefficient since only four MX_cases became actual MX_donors out of 38. MX_Improving the MX_efficiency of ICUs in dealing with MX_brain_death MX_cases (MX_reporting , MX_documentation , MX_maintenance and MX_consent ) will MX_require MX_solving MX_several MX_problems at the medical, administrative, religious, and MX_mass_media MX_levels ."""

        doc = nlp(text_in)
        text_new = termMatch.get_termMatch(doc)

        # trace nbr de matches print("gaz Nbr de matches :"+str(self.gaz.get_len_matches()))
        # trace doc tagge print(get_doc_pos(doc))
        # trace print(text_new)
        assert_equal(text_good, text_new)

    def termMatch_test_lemme(self):

        # INIT du modele
        nlp = spacy.load(modele_init_en, disable=["parser", "ner"])

        # init des composants
        param = {
            "show": "doc",
            "termMatcher_tag": "MX_",
            "termMatcher_vocabulary": MX_jsonl_lemme,
        }
        termMatch = termMatcher(nlp, **param)
        tagger = POStagger(nlp, ())

        print("Nombre de pattern:" + str(termMatch.get_len_matches()))

        # more_term = [ {"label": "MX", "pattern": [{"lemma": "Parkison"}, {"lemma": "disease"}], "id": "st1"},
        #         {"label": "MX", "pattern": [{"lemma": "Guam"}, {"lemma": "Parkinson"}, {"lemma":"dementia"}], "id": "st2"},
        #         {"label": "MX", "pattern": [{"lemma": "country"}], "id": "st3"},
        #          ]
        # cls.gaz.add_patterns(more_term)
        # construction du pipe
        nlp.add_pipe(tagger, name="tagger_print", first=True)
        nlp.add_pipe(termMatch, name="gazetteer", last=True)

        # trace print("gaz Nbr de patterns :"+str(self.gaz.get_len_gaz()))

        text_in = """The efficiency of utilization of potential donors for organ transplantation in Saudi Arabia: A pilot study."""
        text_good = """The efficiency of utilization of potential MX_donors for MX_organ transplantation in Saudi Arabia: A MX_pilot study."""

        doc = nlp(text_in)
        text_new = termMatch.get_termMatch(doc)

        # trace nbr de matches print("gaz Nbr de matches :"+str(self.gaz.get_len_matches()))
        # trace doc tagge print(get_doc_pos(doc))
        # trace print(text_new)

        assert_equal(text_good, text_new)
