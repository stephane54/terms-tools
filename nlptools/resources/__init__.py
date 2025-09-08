#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

_local_path = os.path.dirname(os.path.abspath(__file__))

NPchunker_rules_gen_en = os.path.join(_local_path, "NPchunker_rules_en.txt")

resource_dir = os.path.join(_local_path)
if os.getenv('DICO_PATH'):
    dico_path = os.getenv('DICO_PATH')

# stop word list
my_stopword_file = os.path.join(_local_path,"my_stopwords.tsv")
stop_words_english = os.path.join(_local_path,"stop_words_english.tsv")