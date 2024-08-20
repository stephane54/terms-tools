#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import *
from nlptools import NPchunker
from nlptools import exec_spacy_pipe_en


class NPchunkerDP_test:
    @classmethod
    def setup_class(cls):

        cls.parser = exec_spacy_pipe_en("NPchunkDP")

    def lovins_st01(self):
        doc_in = "Mucocutaneous lesions in transplant recipient in a tropical country"
        doc_good = "mucocutaneous_lesion transplant_recipient tropical_country"
        doc_new = self.parser(doc_in)
        assert_equal(doc_good, doc_new)
