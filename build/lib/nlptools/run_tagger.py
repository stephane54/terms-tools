    # execution

class Run_tagger(object):
    
    def __init__(self, nlp):

        self.nlp = nlp

    def run_tagger (self, text):
        
        return (self.nlp(text))
