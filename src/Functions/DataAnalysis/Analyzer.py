# NUMBER DESCRIPTIVE INFORMATION
# ====================================================================================
# Count : int
# Sum   : float 
# Mean  : float
# Median: float
# Mode  : []
# Std   : float  
# Min   : float  
# Max   : float  
# Q25   : float  
# Q50   : float  
# Q75   : float  
# skew  : float  
# kurt  : float  

# TEXT DESCRIPTIVE INFORMATION
# ====================================================================================
# Word Count | Word Length | Word Feature 1 | Word Feature 2 | Word Feature 3 | ...
# Sent Count | Sent Length | Sent Feature 1 | Sent Feature 2 | Sent Feature 3 | ... 
# Para Count | Para Length | Para Feature 1 | Para Feature 2 | Para Feature 3 | ... 
#
# Phonetic Features         : sound                 : articulatory, acoustic, auditive
# Phonological Features     : sound system          : distinctive features
# Morphological Features    : word formation        : phrase structures 
# Syntactic features        : words formation       : clause structures
# Semantic features         : meaning               : meanings in knowledge graphs
# Pragmatic Features        : meaning in context    : contexts in knowledge graphs
#
# word level        : count, length, feature1, feature2, feature3, ...
# phrase level      : count, length, feature1, feature2, feature3, ...
# sentence level    : count, length, feature1, feature2, feature3, ...
# paragraph level   : count, length, feature1, feature2, feature3, ...
#
# Note: each text field requires different levels and techniques for analysis 
#
# Word Description:
# Text  : string    # full text from data value in column
# Token : string    # individual word from full text
# Freq  : int       # number of occurences of token
# Count : int       # number of tokens or words in text
# Length: int       # number of characters in token
# ...

from typing import List, Tuple

import numpy as np
import pandas as pd

import spacy 
from spacy.matcher import Matcher

from Functions.DataAnalysis import Validator

nlp = spacy.load("en_core_web_sm")

def describe_numbers(series: pd.Series) -> pd.DataFrame:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if Validator.is_number(series) == False:
        raise Exception("incorrect data type")

    df = pd.DataFrame(columns=["Count", "Sum", "Mean", "Median", "Mode", \
        "Std", "Min", "Max", "25%", "50%", "75%", "Skewness", "Kurtosis"])
    
    count = series.count()
    sum = series.sum()
    mean = series.mean()
    median = series.median()
    mode = [m for _, m in series.mode().iteritems()]
    std = series.std()
    min = series.min()
    max = series.max()
    q25 = series.quantile(0.25)
    q50 = series.quantile(0.50)
    q75 = series.quantile(0.75)
    skew = series.skew()
    kurt = series.kurtosis()

    df.loc[len(df.index)] = \
        [count, sum, mean, median, mode, std, min, max, q25, q50, q75, skew, kurt]

    return df 

def describe_text(series: pd.Series) -> pd.DataFrame: 
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    if Validator.is_text(series) == False:
        raise Exception("incorrect data type")

    avg_words = np.average([len(str(value).split(" ")) for _, value in series.dropna().iteritems()])
    avg_sents = np.average([len(list(nlp(value).sents)) for _, value in series.dropna().iteritems()])

    if avg_words <= 3: 
        return describe_words(series)

    if avg_sents == 1: 
        return describe_sents(series)

    if avg_sents > 1: 
        return describe_paras(series)
        
def describe_words(series: pd.Series) -> pd.DataFrame:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    
    counts = series.value_counts()

    lang_df = pd.DataFrame(columns=["Text", "Token", "Count", "Freq", "Length", "Lemma", "PoS", "Tag", "Dep", "Shape", "Sentiment"])
    
    for _, value in series.iteritems():
        if type(value) != str: continue  

        tokens = nlp(value)
        for token in tokens:
            count = len(str(value).split(" "))
            freq = counts[value]
            length = len(token.text)
            lang_df.loc[len(lang_df.index)] = \
                [value, token.text, count, freq, length, token.lemma_, \
                token.pos_, token.tag_, token.dep_, token.shape_, token.sentiment]

    return lang_df.drop_duplicates()

def describe_sents(series: pd.Series) -> pd.DataFrame:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    lang_df = pd.DataFrame(columns=["Text", "Noun", "Number of Nouns", \
        "Verb", "Number of Verbs", "Adjective", "Number of Adjectives"])

    for _, value in series.iteritems():
        if type(value) != str: continue  

        nouns = []
        verbs = []
        adjectives = []
        
        tokens = nlp(value)
        for token in tokens:
            if token.pos_ == "NOUN":
                nouns.append(token)
            if token.pos_ == "VERB":
                verbs.append(token)
            if token.pos_ == "ADJ":
                adjectives.append(token)

        lang_df.loc[len(lang_df.index)] = \
            [value, nouns, len(nouns), verbs, len(verbs), adjectives, len(adjectives)]

    return lang_df

def describe_paras(series: pd.Series) -> pd.DataFrame:
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    lang_df = pd.DataFrame(columns=["Text", "Token", "Start Index", "End Index", "Entity Label", "Knowledge Base ID"])

    for _, value in series.iteritems():
        if type(value) != str: continue  
        tokens = nlp(value)

        for ent in tokens.ents:
            lang_df.loc[len(lang_df.index)] = \
                [value, ent.text, ent.start_char, ent.end_char, ent.label_, ent.kb_id_]

    return lang_df

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

def extract_phone_numbers(text: str) -> str:
    nlp_doc = nlp(text)
    pattern = [{"ORTH": "("}, {"SHAPE": "ddd"},
               {"ORTH": ")"}, {"SHAPE": "ddd"},
               {"ORTH": "-", "OP": "?"},
               {"SHAPE": "ddd"}]
    matcher = Matcher(nlp.vocab)
    matcher.add("PHONE_NUMBER", None, pattern)
    matches = matcher(nlp_doc)
    for match_id, start, end in matches:
        span = nlp_doc[start:end]
        return span.text

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
