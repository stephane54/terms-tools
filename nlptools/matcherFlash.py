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
import sys
import json 
import os
import logging
import collections

__authors__ = "Stephane Schneider"
__contact__ = "stephane.schneider@inist.fr"

allowed_postags=["NOUN", "ADJ", "VERB", "PROPN"]
#DET={"fr":"le ","en":"the "}

class MatcherFlash:

    name = "entity"
    logger = logging.getLogger(__name__)
    size_voc = 0

    def __init__(self, prefix, output, keywords_dict, case_sensitive, stopword_file, format, text_format):

        # Set up the KeywordProcessor
        self.keyword_processor = KeywordProcessor(case_sensitive=case_sensitive)
        self.prefix=prefix
        self.output=output
        self.text_format = text_format  #lemma | lower
        self.format = format
        self.load_Voc(stopword_file, keywords_dict)
        MatcherFlash.size_voc = len(self.keyword_processor)
        self.allowed_postags=allowed_postags
        # trace : see dico
        # print( f"{self.keyword_processor.get_all_keywords()}")


    def __call__(self, text):
        """Apply the pipeline component on a Doc

        """
        if self.output == "doc":
            return self._format_doc(self.keyword_processor.replace_keywords(text))
        elif self.output == "list":
            return self._format_standoff(self.keyword_processor.extract_keywords(text, span_info=True))            
        elif  self.output == "json":
            return self._format_json(self.keyword_processor.extract_keywords(text, span_info=True))
    
    
    def _format_doc(self, st):
        return(st)
    
        
    # Transformation des resultats en liste sous forme de texte
    # format terms_matché + idx
    def _format_json(self, tuples_list):
        ks = ("id", "ul", "term", "pref")
        info_terms=[]
        for tup in tuples_list :
            terms_info , idx0, idx1 = tup 
            en={ }
            en["idx"]=dict(zip(["start","end"],[str(idx0),str(idx1)]))
            en["match"]=dict(zip(ks, terms_info))
            info_terms.append(en) 
                
        return(json.dumps(info_terms, ensure_ascii=False))
        
        
    def _format_standoff (self, tuples_list):
        
        # TRACE
        #print(tuples_list)            
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
            # see dic
            print(dico)
            for keys,values in dico.items():
                print(keys)
                print(values)
            
            #brain_lobe
            #['brain lobe', 'lobe of the brain', 'brain lobes', 'lobes of the brain']
            '''
            
            # add dico to processor
            self.keyword_processor.add_keywords_from_dict(dico)
            '''
            self.keyword_processor.add_keyword('Taj Mahal', ('Monument', 'Taj Mahal'))
            self.keyword_processor.add_keyword('Delhi', ('Location', 'Delhi'))
            print(self.keyword_processor.get_all_keywords())
            exit()
            '''
        
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
            
            # calcule de la cles du dictionnaire flash
            if  self.output in ["list","json"]:
                #key = (row[field],row['id']) #.replace(" ", "_")   resultat avec ou sans _
                key = (row['id'],row['ul'],row['term'],row['pref']) 
                
            # construis la forme in-doc
            if  self.output == "doc":
                #key = self.prefix+row[field].replace(" ", "_") +"_"+row['id']
                #prefix plus utilisé
                #key = "["+row[field]+"]("+row['id']+" \\\""+row['pref']+' ['+row['id'] +"]\\\")"
                # ok
                key = "["+row[field]+"]("+row['id']+")"
                
                
            dico[key].append(row['ul']) 
            if re.search("-",row['ul']): 
                dico[(key)].append(re.sub(r"-"," ",row['ul']) )
                
        # print dico          print(dico)
        # SORTIE A REVOIR CAR JSON MAL FORME !! voir comment c fait dans le termMatcher
        return (dico)
    
    
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


