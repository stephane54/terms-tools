import json
import logging
import re

class Run_tagger(object):
    
    def __init__(self, nlp, Matcher, input):
        
        self.nlp = nlp
        self.matcher = Matcher
        self.input = input

    def run_tagger (self, stream):
        
        if self.input in ["jsonl", "json"]: #jsonl json
            
            try:              
                data = json.loads(stream)  
            except json.decoder.JSONDecodeError:
                logging.error(f"{stream}Input format problem line : LOAD: String could not be converted to JSON - not a valid JSON document." )
                
            if self.input == 'jsonl':
                data["value"] = self._execute_(data["value"])
            elif self.input == 'json':
                data[0]["value"] = self._execute_(data[0]['value'])
    
            return(self._norm_json_(json.dumps(data, ensure_ascii=False) ))
           
        else:
            # stream
            return (self._execute_(stream))
    
    # normalisation du flux json
    def _norm_json_ (self, stream):
        
        remplacements =  [('\\"','"'), (']"', ']'),('"[', '[')]
        for ancien, nouveau in remplacements:
            stream = stream.replace(ancien, nouveau)

        return (stream)
          
    
    def _execute_(self,stream): 
        
        # pretraitement
        doc = self.nlp(stream)
        lst_word = []
        # on extrait le texte pretraité 
        for token in doc :
            #if not token.is_punct
            #    and not token.is_digit
            #    and not token.is_space
            #    and not token.is_stop
            #    and not token.like_num
            #    and not token.is_currency
            #    and token.pos_ in self.allowed_postags
            if self.matcher.text_format == 'lemma':
                lst_word.append(token.lemma_.lower())
            elif  self.matcher.text_format == 'lower':
                lst_word.append(token.lower_+token.whitespace_)
            else:
                lst_word.append(token.text_+token.whitespace_)
                
        # TRACE texte pretraité  print(lst_word)
        # Execution du matcher
        if self.matcher.text_format  == "lemma":
            return( self.matcher(" ".join(lst_word)) )
        else:
            return( self.matcher("".join(lst_word)) )
        
            
