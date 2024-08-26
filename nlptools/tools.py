#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 16:09:28 2019

pretraitement sur les mots et pharses du corpus

@author: stephane schneider

"""
from functools import partial
from bz2 import BZ2File
from bz2 import BZ2Decompressor
import json
import csv
import regex
import re
from spacy.tokens import Doc
import numpy  as np
from spacy.attrs import LOWER, POS, ENT_TYPE, IS_ALPHA, DEP, LEMMA, IS_PUNCT, IS_DIGIT, IS_SPACE, IS_STOP

import sys
tab = "\t"
cr = "\n"
space = " "
slash = "/"
LEFT={"fr":"le","en":"the","lenght":1}
RIGHT={"fr":"est correct.","en":"is correct.","lenght":3}
tiretb = "_"
tireth = "-"
matches = []
point = ". "
vide = ""
limit_notice = 100000000
list_attr_spacy = [LOWER, POS, ENT_TYPE, IS_ALPHA, DEP, LEMMA, LOWER, IS_PUNCT, IS_DIGIT, IS_SPACE, IS_STOP]

csv.field_size_limit(limit_notice)

# TODO : decompresse mais CVS on perd l indentification des champs, TODO = y remedier
# utilisation :
# for row in BZ2_CSV_LineReader(corpus).readlines():
#        print(''.join(row))

class ReaderBZ2(object):
    def __init__(self, filename, buffer_size=4 * 1024):

        self.filename = filename
        self.buffer_size = buffer_size

    def readlines_csv(self):

        with open(self.filename, "rb") as file:
            for row in csv.reader(
                self.line_reader(file),
                delimiter="\t",
                doublequote=False,
                quoting=csv.QUOTE_NONE,
            ):
                yield row

    def readlines_txt(self):

        with open(self.filename, "rb") as file:
            for row in self.line_reader(file):
                yield row

    def line_reader(self, file):

        buffer = ""
        decompressor = BZ2Decompressor()
        reader = partial(file.read, self.buffer_size)

        for bindata in iter(reader, b""):
            block = decompressor.decompress(bindata).decode(
                encoding="utf-8", errors="ignore"
            )
            buffer += block

            if "\n" in buffer:
                lines = buffer.splitlines(True)

                if lines:
                    buffer = "" if lines[-1].endswith("\n") else lines.pop()

                    for line in lines:
                        yield line


# Iterateur de document dun corpus au format csv bz2
# return les n 1er champs
# TODO : controler le format et le n
def readCsvBz2(bz2_loc, n):

    for row in ReaderBZ2(bz2_loc).readlines_csv():
        yield ([val for val in row[0:n]])


# iterateur sur une entree stdin avec doc au format tsv/csv
def readCsv(line, n):

    for row in csv.reader(
        iter(line, ""), delimiter="\t", doublequote=False, quoting=csv.QUOTE_NONE
    ):
        yield ([val for val in row[0:n]])


# Iterateur de document dun corpus au format texte bz2
def readTxtBz2(bz2_loc, n):

    for row in ReaderBZ2(bz2_loc).readlines_txt():
        yield (row)


# normalisation basique d'une ligne de texte
# UNUSED
def norm_sent(line):

    # enleve les suite de chiffre+lettre ex: h1n1 12121 1.12 ω-carboxy-(1',45)-alkynyl
    line = re.sub(
        r"[a-zA-Z,;\-\.\(\'\)\[\]\{\}]*\d+[a-zA-Z,;\-\(\'\)\[\]\.\{\}]*", "", line
    )

    # suppression sup et sub, x space
    # line = re.sub(r'[\n\r\t]|\bsu[p|b]\b|\b\w{1,2}\b|\b\d+\b|[.;,-]',"", line, flags=re.I)

    ##########   traitements des phrase
    # enleve les caracteres non alphanumerque
    # line = re.sub(r'[^\w\-\(\)]+', ' ', line)

    # traitement des parentheses uniquement ex : (PTR) => PTR
    line = re.sub(r"\s(\()([a-zA-Z\s*]*)(\))\s", r" \2 ", line)

    # Reduction a un seul espace
    line = re.sub(r"\s+", " ", line, flags=re.I)

    # Conversion en Lowercase
    line = line.lower()

    return line


# Nettoyage basique d une liste de mot
def cleanWList(w_list):

    # enleve space debut et fin
    w_list = [w.strip() for w in w_list]

    # met en min
    w_list = [w.lower() for w in w_list]

    # enlever les mots dont taille inf 2
    w_list = [word for word in w_list if len(word) > 2]

    return w_list


# Iterateur de document dun corpus au format json bz2
# TODO : a corriger, erreur de format json lors du decode, demande ,
# UNUSED
def readJsonBz2(bz2_loc, tag, n=10000):

    with BZ2File(bz2_loc) as file_:

        for i, line in enumerate(file_):
            data = json.loads(line.strip())
            # print(data[tag])
            yield data[tag]

            if i >= n:
                break


# separe les mots d'un liste de mots cles composes par "separateur", return uen chaine
def mcTag(liste_mc, separateur=" "):

    liste = clean_w_list(liste_mc.split(";"))
    return separateur.join([space.join(re.split(r"\s+", w)) for w in liste])


def mcMark(liste_mc, separateur=" "):

    # for word in liste_mc:if word not in listelist_w.append(word)
    return [separateur.join(re.split(r"\s+", w)) for w in liste_mc]


# entrée : string
# return la chaine avec mots liés par separateur
def oneMcMark(mc, separateur=" "):

    # for word in liste_mc:if word not in listelist_w.append(word)
    return separateur.join(re.split(r"\s+", mc))


# supprime les caracteres spéciaux, les balises <sup> et <sub>
def delCaracSpeciaux(chaine):

    patch = re.compile(r"[\n\r\t]|\<\/?su[b|p]\>", re.IGNORECASE)
    return patch.sub("", chaine)


def cleanTokenLenght(token):

    return len(token.text) > 1


# Flechi un dictionnaire
# doc = 1 terme
def getDicoInflect(doc):
    
    l_term=[]
    norm_form = []
    norm_form = doc.text_with_ws.replace(" ","_")
    
    
    for token in doc :
        #if  token.dep_== 'ROOT' and token.pos_=='VERB':
        # calcul de flexion
        if  token.dep_== 'ROOT' and token.pos_== 'NOUN':
            if token.text_with_ws[-1] == space:
                if token.tag_ != 'NNS':
                    l_term.append( doc[token.i]._.inflect('NNS')+space ) 
                else:
                    l_term.append( doc[token.i]._.inflect('NN')+space ) 
            elif token.text_with_ws[0] == space: 
                if token.tag_ != 'NNS':
                    l_term.append( space+doc[token.i]._.inflect('NNS') ) 
                else:
                    l_term.append( space+doc[token.i]._.inflect('NN') ) 
            else:
                if token.tag_ != 'NNS':
                    l_term.append( doc[token.i]._.inflect('NNS') ) 
                else:
                    l_term.append( doc[token.i]._.inflect('NN') ) 
        else:
            
            if  token.text_with_ws != LEFT:
                l_term.append(token.text_with_ws)     
    
    return(''.join(l_term)+tab+(norm_form[1:], doc.lang_))
                      
                      
def dive_term (word, lang):
    
    return(LEFT[lang]+space+word+space+RIGHT[lang])


def clean_terms(doc):
    
    return(doc[LEFT["lenght"]:-abs((RIGHT["lenght"]))].as_doc())
    

def add_himself (word):   
     
    return(''.join(word)+tab+''.join(word).replace(' ','_'))


def getDicoPos(doc):
    
    list_text = []
    list_pos = []
    list_lemma = []

    for token in doc:
        # if token._.stem:
        #   list_stem.append(token._.stem)
        if token.pos_:
            list_text.append(token.text)
            list_pos.append(token.tag_)
            #list_pos.append(token.tag_+"[POS:"+token.pos_+";FLECT:"+";HEAD:"+token.head.text+";DEP:"+token.dep_+";"+str(token.morph)+"]")
            list_lemma.append(token.lemma_)            

    return (space.join(list_text)+tab+space.join(list_pos)+tab+space.join(list_lemma))
   

#{"label":"Analytical chemistry","pattern":[ {"lemma":"analytical","pos":"ADJ"}, {"lemma":"chemistry","pos":"NOUN"} ],"id":"<http://www.termsciences.fr/vocabs/MX/137906>"}    
def getDicoAnnot(doc):
    
    tab = []
    ld = {}
    for token in doc:
        # if token._.stem:
        #   list_stem.append(token._.stem)
        dic = {}
        if token.pos_:
            dic["pos"]=token.pos_
            dic["lemma"]=token.lemma_
        tab.append(dic)
    ld["label"]=str(doc)
    ld["pattern"]=tab
    return(ld)
           

def getDocPos(doc):

    list_ = []

    for token in doc:
        # if token._.stem:
        #   list_stem.append(token._.stem)
        if token.pos_:
            list_.append("text:[" + token.text + "]")
            list_.append(tab)
            list_.append("pos:[" + token.pos_ + "]")
            list_.append(tab)
            list_.append("lemma:[" + token.lemma_ + "]")
            list_.append(tab)
            list_.append("stop:[" + str(token.is_stop) + "]")
            list_.append("\n")

    return space.join(list_)


def getText(doc):

    list_w = []

    for token in doc:
        # if token._.stem:
        #   list_stem.append(token._.stem)
        list_w.append(token.text_with_ws)

    return "".join(list_w)


# affiche certaine info du document structure "doc"
def getDoc(doc):

    list_w = []

    for token in doc:
        # if token._.stem:
        #   list_stem.append(token._.stem)
        list_w.append(
            "token:text:[" + token.text + "]"
        )  # unicode Verbatim text content.
        list_w.append(".lemma:[" + token.lemma_ + "]")  # unicode Verbatim text content.
        list_w.append(
            ".sent:[" + str(token.sent) + "]"
        )  # #V2.0.12    Span    The sentence span that this token is a part of.
        list_w.append(
            ".POS_:[" + token.pos_ + "]"
        )  #    unicode Text content, with trailing space character if present.
        list_w.append(
            ".ent_iob_:[" + token.ent_iob_ + "]"
        )  # unicode Trailing space character if present.
        # list_w.append("orth:"+token.orth)    #int ID of the verbatim text content.
        list_w.append(cr)

    return space.join(list_w)


# renvoi des ents replacé dans le corpus
def getEnts(doc, tag):

    text = []
    ent = []

    for token in doc:
        if token.ent_iob == 3:
            if len(ent) > 0:  # car term contingus
                text.append(tiretb.join(ent))
                text.append(
                    space
                )  # attention parfois ajoute un space en de trop ex : on (MX_control ): M
                ent = []
            ent.append(tag)
            ent.append(token.text)

        else:

            if token.ent_iob == 1:
                ent.append(token.text)
            else:
                if len(ent) > 0:
                    text.append(tiretb.join(ent))  # scan term contingue
                    text.append(space)
                    ent = []
                text.append(token.text_with_ws)

    return vide.join(text)

# revoie une liste a partir d une string de type ['A','B']
def to_list( s ):

    s1=re.sub(r'[ \'\"\[\]]','',s)
    if s1 == "":
        s2=[]
    else:
        s2 = s1.split(',')
    #print(s2, type(s2),len(s2))
    return(s2)


# supprime les informations des elements appartenant à une liste de tag
# kind = defini si filtre de facon   positive = white
#                                    negative = black
def doc_remove_pos (doc, list_pos, list_attr, kind):

    index_to_del = []
    np_array = doc.to_array(list_attr) # Array representation du Doc

    if kind == "white":
        [index_to_del.append(word.i) for word in doc if word.pos_ in list_pos]    
    else:
        [index_to_del.append(word.i) for word in doc if word.pos_ not in list_pos]    

    # Creation d1 mask: boolean array des indexes a supprimer
    mask_to_del = np.ones(len(np_array), np.bool)
    mask_to_del[index_to_del] = 0
    
    np_array_2 = np_array[mask_to_del]
    doc2 = Doc(doc.vocab, words=[t.text for t in doc if t.i not in index_to_del])
    doc2.from_array(list_attr, np_array_2)

    arr = np.arange(len(doc))
    new_index_to_old = arr[mask_to_del]
    doc_offset_2_token = {tok.idx : tok.i  for tok in doc}  # pour les extensions perso
    doc2_token_2_offset = {tok.i : tok.idx  for tok in doc2}  # pour les extensions perso
    new_user_data = {}

    for ((prefix, ext_name, offset, x), val) in doc.user_data.items():
        old_token_index = doc_offset_2_token[offset]
        new_token_index = np.where(new_index_to_old == old_token_index)[0]
        if new_token_index.size == 0:  # Cas index supprimé
            continue
        new_char_index = doc2_token_2_offset[new_token_index[0]]
        new_user_data[(prefix, ext_name, new_char_index, x)] = val
    doc2.user_data = new_user_data
    
    return (doc2)

def replace_carspe(x):
    
    REGEX = [
        (r"([^0-9]+)'",  r"\g<1>"),   # 2'3'-Cyclic-Nucleotide Phosphodiesterases,2'3'-Cyclic-Nucleotide_Phosphodiesterases
    ]
    # on garde le hash sur le dico pour la rapidité mais on pourrait tout faire avec REGEX, A VOIR
    dico_map = {
            #"&": " and ",
            #"%": " percent ",
            #">": " greater-than ",
            #"<": " less-than ",
            #"=": " equals ",
            "#": " ",
            "~": " ",
            #"/": " ",
            "\\": " ",
            "|": " ",
            "$": "",
            # Remove empty :
            " : ": " ",
            # Remove double dashes
            #"--": " ",
            # Remove possesive splits
            #" 's ": " ",
            # Remove quotes
            '"': "",
            # replace dash
            '-':'_',
            '__':'_',
            ',':'_',
            ' ':'_',
            #normalization
            '’':"'",
        }
    def lookup(s, lookups):
        for pattern, value in lookups:
            s = regex.sub(pattern, value, s) 
        return s

    
    for key, val in dico_map.items():
        x = lookup(x, REGEX).replace(key, val)
        
    return(x.replace("__", "_"))