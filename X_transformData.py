"""

INFO: Files starting with X_ are (failed) tests, which didn't work out the way I expected. They are still in this repository for documentary purposes.

What this script does: This script takes a term-document matrix and prepares it for machine learning and returns a tf-idf matrix.

PROBLEM: Without preparing the data with CountVectorizer, it's not possible to use parameters like min_df or max_df for tf-idf, which is quite inconvenient. Furthermore constant data format switching is needed.
Therefore another approach will be used, where the TDM is built by sk-learn and not manually.
"""

import os
import pandas as pd 
from sklearn.feature_extraction.text import TfidfTransformer
import scipy.sparse

tdm = os.path.join(os.getcwd(), "term_document_matrix.csv")
voc = os.path.join(os.getcwd(), "vocabulary.txt")
meta = os.path.join(os.getcwd(), "metadata.csv")

tdm_df = pd.read_csv(tdm, sep="\t", index_col=0)  #without index_col=0 a ranged index is created in front of the filenames
indexes = tdm_df.index
columns = tdm_df.columns
array = tdm_df.values

#print(columns)
#print(array)

array = scipy.sparse.csr_matrix(array)

tfidf = TfidfTransformer()
sparse_tdm = tfidf.fit_transform(array)

save_it = sparse_tdm.toarray()

df = pd.DataFrame(save_it)
df.to_csv("file_path.csv", header=None, index=None)
