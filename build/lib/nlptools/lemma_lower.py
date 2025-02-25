# Create a pipe that converts lemmas to lower case:
from spacy.language import Language
from spacy.tokens import Doc

__authors__ = "Stephane Schneider"
__contact__ = "stephane.schneider@inis.fr"

'''
@Language.component("lower_case_lemmas")

def lower_case_lemmas(doc) :
    for token in doc :
        token.lemma_ = token.lemma_.lower()
    return doc
'''

@Language.factory("lower_case_lemmas"
)
def lower_case_lemmas(nlp: Language, name:str ):
    
    return LowerCaseLemmas(nlp)

class LowerCaseLemmas (object):
    
    def __init__(self, nlp):

        self.nlp = nlp
    
    
    def __call__(self, doc):
        
        for token in doc :
            token.lemma_ = token.lemma_.lower()
        return doc