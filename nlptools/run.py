#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 12:46:45 2020
@author: stephane schneider

"""
import os
from nlptools.exec_spacy_pipe import exec_spacy_pipe_en
from nlptools.exec_spacy_pipe import exec_spacy_pipe_fr

class full_run (object):

    def __init__(self, pipe, language, ini_file, param, output ):

        self.location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname("doc"))
        )

        if (language == "en"):
            
            self.parsers = [
                exec_spacy_pipe_en(pipe, ini_file, param, output),
            ]
        else:
            self.parsers = [
                exec_spacy_pipe_fr(pipe, ini_file, param, output),
            ]

    def pipe_analyse(self, text):

        # execution du pipe
        for parser in self.parsers:
            text = parser(text)
        return text
        # return x_blanc.sub(" ",patch.sub(" ", text))
