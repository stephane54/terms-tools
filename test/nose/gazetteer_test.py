#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stephane
"""
# exemple :  nosetests test/termMatcher_test.py
#
# !!!!!!!!!!!!!!!!!!!!!!!!!   OBSOLETE avec spacy 3 A METTRE A JOUR

from nose.tools import *
from nlptools.tools import *
from nlptools import exec_spacy_pipe_en


class gazetteer_test:
    @classmethod
    def setup_class(cls):

        cls.parser = exec_spacy_pipe_en("gazetteer")

    def porter_test01(self):
        # doc_in = "Mucocutaneous lesions in transplant recipient in a tropical climate and Country"
        # doc_good = "Mucocutaneous ; Lesion ; Tropical climate ; Country"
        doc_in = """ The efficiency of utilization of potential donors for organ transplantation in Saudi Arabia
: A pilot study . Organ shortage has been the main obstacle in the progress of organ transplantation in Saudi Arabia. The aim of this pilot study was to determine the percentage of potential donors among all deaths in 
Riyadh hospital intensive care units (ICUs). Mortality data were collected by a medical professional in each ICU and analyzed on weekly basis for 1 year (June 2001 through May 2002): The final analysis at the end of the year showed
 the number of brain death cases in all hospitals to be 114 out of 542 deaths. Fifty-four percent occurred in one hospital. Thirty-eight cases were reported to the Saudi Center for Organ
  Transplantation (33%). Documentation was completed in only 23 cases (60%). Only four cases became actual donors. In conclusion, there is underreporting of brain death cases. Dealing with the reported cases is inefficient since 
only four cases became actual donors out of 38. Improving the efficiency of ICUs in dealing with brain death cases (reporting, documentation, maintenance and consent) will require solving several problems at the medical, 
administrative, religious, and mass media levels."""

        doc_good = """saudi_arabia pilot_study saudi_arabia pilot_study intensive_care brain_death brain_death brain_death mass_media"""
        doc_new = self.parser(doc_in)
        assert_equal(doc_good, doc_new)
