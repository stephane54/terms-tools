#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.py

"""
from __future__ import unicode_literals
import re
from flashtext import KeywordProcessor
import csv
import json 
import os
import logging
import collections
from spacy.language import Language
__authors__ = "Stephane Schneider"
__contact__ = "stephane.schneider@inis.fr"

allowed_postags=["NOUN", "ADJ", "VERB", "PROPN"]
DET={"fr":"le ","en":"the "}

# Composant Gazetteer de type PhraseMatcher, alimenté par une liste de termes
@Language.factory(
    "Matcher_flash",
    default_config={
        "output":"",
        "prefix": "",
        "keywords_dict": "",
        "stopword_file": "",
        "case_sensitive": False,
        "format": "",
        "text_format": "lower"
    },
)
def create_Matcher_component(
    nlp: Language,
    name: str,
    output: str,
    prefix: str,
    keywords_dict: str,
    stopword_file: str,
    case_sensitive: bool,
    format: str,
    text_format : str,
):
    return MatcherFlash(nlp, prefix, output, keywords_dict, case_sensitive, stopword_file, format, text_format )


class MatcherFlash:

    name = "entity"
    logger = logging.getLogger(__name__)
    size_voc = 0

    def __init__(self, nlp, prefix, output, keywords_dict, case_sensitive, stopword_file, format, text_format ):

        # Set up the KeywordProcessor
        self.keyword_processor = KeywordProcessor(case_sensitive=case_sensitive)
        self.prefix=prefix
        self.output=output
        self.nlp = nlp
        self.text_format = text_format  #lemma | lower
        self.format = format
        self.load_Voc(stopword_file, keywords_dict)
        MatcherFlash.size_voc = len(self.keyword_processor)
        self.allowed_postags=allowed_postags
        # trace : see dico
        # print( f"{self.keyword_processor.get_all_keywords()}")


    def __call__(self, doc):
        """Apply the pipeline component on a Doc

        """
        if self.output == "doc":
            return self.keyword_processor.replace_keywords(self._prepare_text(doc))
        elif self.output == "list":
            return self._format_standoff(self.keyword_processor.extract_keywords(self._prepare_text(doc), span_info=True))            
        elif  self.output == "json":
            return (json.dumps(self.keyword_processor.get_all_keywords(), ensure_ascii=False)) 
            
        # TRACE text lemmatisé sans match
        #return (self._lemmatize(doc))

        
    # Transformation des resultats en liste sous forme de texte
    def _format_standoff (self, tuples_list):
                 
        return ("".join("%s %s %s" % tup+"\n" for tup in tuples_list))
        
        
    def load_Voc(self, stopword_file, dico=None):

        """
        Initialize the parser with the vocabulary.

        Args:
            dico: filename, location of the replacement dictionary.
            prefix: string, text to prefix each replacement.
        """
        if dico is None:
            local_path = os.path.dirname(__file__)
            dico = os.path.join(local_path, dico)
            self.logger.debug("Using default dictionary: %s" % dico)
        
        if not os.path.exists(dico) or os.path.getsize(dico) == 0:
            msg = "Can't Find dictionary {}".format(dico)
            self.logger.error(msg)
            raise IOError()
        
        with open(dico) as F:

            csvfile = csv.DictReader(
                F,
                delimiter="\t",
                fieldnames=("id", "ul","term",  "pref","replacement"),
                quotechar='"',
                quoting=csv.QUOTE_NONE,
                skipinitialspace=True,
            )

            # Create dico
            dico = self._create_dico(csvfile, self.format )            
            '''
            # TRACE
            for keys,values in dico.items():
                print(keys)
                print(values)
            
            brain_lobe
            ['brain lobe', 'lobe of the brain', 'brain lobes', 'lobes of the brain']
            '''
        
        # add dico to processor
        self.keyword_processor.add_keywords_from_dict(dico)
        if not(stopword_file):

            self.logger.info("No stopword dictionary: %s" % stopword_file)

        elif  not os.path.exists(stopword_file) or os.path.getsize(stopword_file) == 0:
            msg = "Can't Find stopword dictionary [{}]".format(stopword_file)
            self.logger.error(msg)
            raise IOError()
        else:
            self.logger.info("Stopword dictionary activate: %s" % stopword_file)

            with open(stopword_file) as Fstp:

                csvfile_stp = csv.DictReader(
                    Fstp,
                    delimiter="\t",
                    fieldnames=("id", "ul"),
                    quotechar='"',
                    quoting=csv.QUOTE_NONE,
                    skipinitialspace=True,
                )

                dico_stp = self._create_dico_stpw(csvfile_stp)
                # add dico to processor
                self.keyword_processor.add_keywords_from_dict(dico_stp)

        
    def _create_dico(self, csvfile, field ):
        
        dico = collections.defaultdict(list)
        for row in csvfile:
            key = row[field].replace(" ", "_") 
            dico[self.prefix+key].append(row["ul"])
      
            if re.search("-",row["ul"]): 
                dico[self.prefix+key].append(re.sub(r"-"," ",row["ul"]) )
            
        return dico 
    def _create_dico_stpw(self, csvfile):

        dic = {}
        lst_ = []
        for row in csvfile:
            
            dict.fromkeys([" "] )
            lst_.append(row["ul"])
            #dic[" "].append(re.sub(r"-"," ",row["ul"]) )
        dic[" "] = lst_
        
        return dic


    def _id_reduce(self, id):

        return ".".join(id.split(".")[:-1])


    def _prepare_text(self, doc):

        lst_word = [
            
            ( token.lemma_.lower()+token.whitespace_ if self.text_format == 'lemma' else (token.lower_+token.whitespace_) )
            
            for token in doc
                #if not token.is_punct
                #    and not token.is_digit
                #    and not token.is_space
                #    and not token.is_stop
                #    and not token.like_num
                #    and not token.is_currency
                #    and token.pos_ in self.allowed_postags
            ]
        
        return("".join(lst_word))