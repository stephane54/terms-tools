#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import *
from nlptools.tools import *
from nlptools import exec_spacy_pipe_en


class stemmer_test:
    @classmethod
    def setup_class(cls):

        cls.parser = exec_spacy_pipe_en("stem")

    def stem_st01(self):
        doc_in = "Mucocutaneous lesions in transplant recipient in a tropical country"
        doc_good = "mucocutan lesion in transplant recipi in a tropic countri"
        doc_new = self.parser(doc_in)
        assert_equal(doc_good, doc_new)
