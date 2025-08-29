import json
import logging

class Run_tagger(object):
    
    def __init__(self, nlp, Matcher, ezs):

        self.nlp = nlp
        self.matcher = Matcher
        self.ezs = ezs

    def run_tagger (self, text):
        
        if self.ezs:
            try:
                data = json.loads(text)
                data["value"] = self._execute_(data["value"])
                return (json.dumps(data, ensure_ascii=False).replace('\\"', '"'))
            except json.decoder.JSONDecodeError:
                logging.error("Input format problem line : String could not be converted to JSON" )
                exit(1) 
        else:
            return (self._execute_(text))
          
    
    def _execute_(self,text): 
        
        # pretraitement
        doc = self.nlp(text)
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
        
            
