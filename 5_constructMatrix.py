"""
5_constructMatrix.py
This script takes the prepared textfiles and converts them to a term-document matrix using sklearn's CountVectorizer.
For boosting our classification performance tf-idf weighting is applied to the aforementioned matrix using sklearn's TfidfTransformer.

Next script: 6_performClassification.py
"""

#Imports
import glob
import os

import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

#Folders
text_dir = os.path.join(os.getcwd(), "texts")


def prepare_texts(text_dir):
    
    #Organize texts in a list and save their filenames in another list
    text_list = []
    filenames = []

    for text in glob.glob(text_dir + "/*.txt"):
        text_list.append(text)
        filenames.append(os.path.splitext(os.path.basename(text))[0])

    return text_list, filenames

def create_matrix(texts):

    #input='filename': a list with files is appended
    #strip_accents: accents are not used consistently e.g. Éowyn vs Eowyn
    #token_pattern: to get rid of numbers and underscores(!), because some authors used myriads of underscores and they sometimes got recognized as words 
    #min_df=0.01: to ensure that only words are used that appear in at least 1% of the texts (for this dataset: 1% = 12 Texts)
    count_vectorizer = CountVectorizer(input="filename", strip_accents="unicode", token_pattern=r"\b[^\d\W_]+\b", min_df=0.01)
    matrix = count_vectorizer.fit_transform(texts)
    vocabulary = count_vectorizer.get_feature_names()

    return matrix, vocabulary

def apply_tfidf_to_matrix(matrix):

    #Use the term-document matrix and transform word frequencies to weighted tf-idf values
    tfidf_transformer = TfidfTransformer()
    tfidf_matrix = tfidf_transformer.fit_transform(matrix)

    return tfidf_matrix

def save_vocabulary(vocabulary):

    #Save the vocabulary with corresponding indices
    index = 0

    with open("vocabulary.csv", "w", encoding="utf-8") as outfile:
        for word in vocabulary:
            outfile.write(str(index) + "\t" + word + "\n")
            index += 1

def save_DataFrame(matrix, vocabulary, filenames):

    #Write Term-Document Matrix to file with labels and filenames. Just for reviewing that structure is correct.
    matrix_DataFrame = pd.DataFrame(matrix.toarray(), columns=vocabulary, index=filenames)

    with open ("tdm.csv", "w", encoding="utf-8") as outfile:
        matrix_DataFrame.to_csv(outfile, sep="\t")

def save_matrix(sparse_matrix):

    #Save sparse matrix and use it again in classification script
    #Rename file to 'sparsematrix.npz' if you didn't use tf-idf!
    sparse.save_npz("sparsematrix_tfidf.npz", sparse_matrix)

def main(text_dir):

    texts, filenames = prepare_texts(text_dir)
    matrix, vocabulary = create_matrix(texts)

    save_DataFrame(matrix, vocabulary, filenames)

    #Comment line 85 out if you want to continue without tf-idf (not recommended). 
    matrix = apply_tfidf_to_matrix(matrix)

    save_vocabulary(vocabulary)           
    save_matrix(matrix)
    
main(text_dir)
