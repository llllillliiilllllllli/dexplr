from typing import List, Dict, Tuple
import numpy as np
import pandas as pd
import spacy 

from Functions.DataAnalysis import Validator

nlp = spacy.load("en_core_web_sm")

# Word Count | Word Length | Word Feature 1 | Word Feature 2 | Word Feature 3 | ...
# Sent Count | Sent Length | Sent Feature 1 | Sent Feature 2 | Sent Feature 3 | ... 
# Para Count | Para Length | Para Feature 1 | Para Feature 2 | Para Feature 3 | ... 

# Phonetic Features         : sound                 : articulatory, acoustic, auditive
# Phonological Features     : sound system          : distinctive features
# Morphological Features    : word formation        : phrase structures 
# Syntactic features        : words formation       : clause structures
# Semantic features         : meaning               : meanings in knowledge graphs
# Pragmatic Features        : meaning in context    : contexts in knowledge graphs

# word level        : count, length, feature1, feature2, feature3, ...
# phrase level      : count, length, feature1, feature2, feature3, ...
# sentence level    : count, length, feature1, feature2, feature3, ...
# paragraph level   : count, length, feature1, feature2, feature3, ...

# Note: each text field requires different levels and techniques for analysis 

def summarize(series: pd.Series) -> pd.DataFrame: 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if Validator.is_text(series) == False:
        raise Exception("incorrect data type")
    
    df = pd.DataFrame(columns=["Text", "Lemma", "PoS", "Tag", "Dep", "Shape", "Sentiment"])
    for _, value in series.iteritems():
        if type(value) != str: continue

        tokens = nlp(value)
        tokens_df = pd.DataFrame(columns=["Text", "Lemma", "PoS", "Tag", "Dep", "Shape", "Sentiment"])

        for token in tokens:
            tokens_df.loc[len(tokens_df.index)] = \
                [token.text, token.lemma_, token.pos_, token.tag_, \
                token.dep_, token.shape_, token.sentiment]
        
        dataline = [value]
        for col in tokens_df.columns[1:]:
            dataline.append(tokens_df[col].count())

        df.loc[len(df.index)] = dataline

    return df
    
### Part-of-Speech (PoS) Tagger

def analyze_pos() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    df = pd.DataFrame(columns=["Text", "Lemma", "PoS", "Tag", "Dep", "Shape", "Alpha", "Stop", "Morph"])
    return NotImplemented

### Morphemes and Morphology

def analyze_morph() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    df = pd.DataFrame(columns=["Text", "Lemma", "PoS", "Tag", "Dep", "Shape", "Alpha", "Stop", "Morph"])
    return NotImplemented

### Lemtimization

def lematimze() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    return NotImplemented 

### Named Entity Recognizer (NER)

def recognize_entity(text: str) -> List[Tuple]:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    tokens = nlp(text)
    for ent in tokens.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_, ent.kb_id_)
    
    return [(ent.text, ent.start_char, ent.end_char, ent.label_, ent.kb_id_) for ent in tokens.ents] 

def customize_entity(text: str) -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    ENT_IOB = spacy.attrs.ENT_IOB
    ENT_TYPE = spacy.attrs.ENT_TYPE

    header = [ENT_IOB, ENT_TYPE]
    doc = nlp.make_doc(text)
    attr_array = np.zeros((len(doc), len(header)), dtype="uint64")

    attr_array[0, 0] = 3  # B
    attr_array[0, 1] = doc.vocab.strings["GPE"]
    doc.from_array(header, attr_array)

    return NotImplemented

def visualize_entity(text: str) -> None: 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    tokens = nlp(text)
    spacy.displacy.serve(tokens, style="ent")

### Dependency Parsing

def extract_nouns() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass 

def extract_verbs(text: str) -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    verbs = set()
    tokens = nlp(text)

    for subject in tokens:
        if subject.dep == spacy.symbols.nsubj \
            and subject.head.pos == spacy.symbols.VERB:
            verbs.add(subject.head)

    return verbs

### Tokenization

def tokenize() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass 

def customize_tokenizer() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass  

def modify_token_patterns() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass 

def merge_tokens() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass 

def split_tokens() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass 

### Sentence Segmentation  

def segment_sents() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass 

def customize_segmenter() -> None:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    pass 
