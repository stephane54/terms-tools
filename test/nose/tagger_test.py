#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import *
from nlptools.tools import *
from nlptools import exec_spacy_pipe_en


class POStagger_test:
    @classmethod
    def setup_class(cls):

        list_with_tag = ("ADJ", "NOUN", "PROPN")
        cls.parser = exec_spacy_pipe_en("lemmatize", list_with_tag)

    def POStagger_st01(self):
        doc_in = "Mucocutaneous lesions in transplant recipient in a tropical countries"
        doc_good = (
            "mucocutaneous lesion in transplant recipient in a tropical countries"
        )
        doc_new = self.parser(doc_in)
        assert_equal(doc_good, doc_new)
