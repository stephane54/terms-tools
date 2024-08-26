#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

_local_path = os.path.dirname(os.path.abspath(__file__))

MX_jsonl_porter = os.path.join(_local_path, "MX2016-label_porter.jsonl")
MX_jsonl_snowball = os.path.join(_local_path, "MX2016-label_snowball.jsonl")
MX_tsv = os.path.join(_local_path, "MX2016-label.tsv")
MX_jsonl_lemme = os.path.join(_local_path, "MX2016-label_lemme.jsonl")
MX_jsonl_lemme_test_en = os.path.join(_local_path, "MX2016-label_lemme_test_en.jsonl")
MX_jsonl_lemme_test_fr = os.path.join(_local_path, "MX2016-label_lemme_test_fr.jsonl")
NPchunker_rules_gen_en = os.path.join(_local_path, "NPchunker_rules_en.txt")
term_lookup_dico = os.path.join(_local_path, "Memoire_v2.0-nlpre-syno.csv")