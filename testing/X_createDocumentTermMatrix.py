"""
INFO: Files starting with X_ are (failed) tests, which didn't work out the way I expected. They are still in this repository for documentary purposes.

What this script does: This script takes the previously saved texts and converts them into a Document-Term-Matrix to prepare it for machine learning purposes.

PROBLEM: See X_transformData.py for further information on why this script is not used.
"""

from collections import Counter 
import os
import glob 
from nltk import RegexpTokenizer
import pandas as pd 

text_dir = os.path.join(os.getcwd(), "texts")

def getTokens(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    #print(tokens)
    return tokens

def getTypes(tokens):
    types = dict(Counter(tokens))
    return types

def saveVocabulary(vocabulary):
    with open("vocabulary.txt", "w", encoding="utf-8") as outfile:
        for word in vocabulary:
            outfile.write(word + "\n")

def saveDataframe(dataframe):
    dataframe.fillna(0, inplace=True)
    with open('term_document_matrix.csv', 'w', encoding='utf-8') as outfile:
        dataframe.to_csv(outfile, sep="\t")

def main(text_dir):
    data = {}
    
    for text in glob.glob(text_dir+ '\\*.txt'):
        
        file_name = os.path.basename(text)
        data[file_name] = {}  #create nested dictionary: {text: {word : count}}

        with open(text, 'r', encoding='utf-8') as infile:
            
            text_content = infile.read().lower()
           
            tokens = getTokens(text_content)
            types = getTypes(tokens)
        data[file_name].update(types.items())
        #print("Found", len(tokens), "tokens and", len(types), "types for text:", file_name)
        #print(data)

    #This dataframe contains the actual term-document frequencies
    df = pd.DataFrame.from_dict(data, orient='index')
    vocabulary = df.columns.values.tolist()
    saveVocabulary(vocabulary)
    saveDataframe(df)
main(text_dir)