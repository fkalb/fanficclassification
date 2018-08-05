"""
6_performClassification.py
This script performs the actual classification using three different classifiers: NaiveBayes, Support Vector Machine, k-Nearest Neighbor.
The first classification is performed on novel level, the second on genre level.

Every classification generates a timestamped logfile, that contains the used parameters and the accuracy of all classifiers.
Additionally, the results are visualized with confusion matrices that were plotted with matplotlib. 
Results and logfiles can be found in the /results directory.
"""

#Imports
import itertools
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn import svm
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

#Folders
result_dir = os.path.join(os.getcwd(), "results")

#Parameters
timestamp = '{:%Y%m%d-%H%M%S}'.format(datetime.now())
test_size = 0.75         #test_size regulates the proportion of the dataset to be included in the testset
nearest_neighbors = 3


def create_folder(result_dir):

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

def create_logfile(result_dir, timestamp):

    #Logfile gets created and named with timestamp. Every output from print statements is redirected to this file! 
    logfile = open(result_dir + "\\" + timestamp + '_logfile.txt', 'a', encoding="utf-8")
    logfile.write("Task successfully performed at " + timestamp + "\n\n")

    return logfile

def load_files():

    #Load matrix with tf-idf values and metadata table
    sparse_matrix = sparse.load_npz('sparsematrix_tfidf.npz')
    meta_dataframe = pd.read_csv("metadata.csv", sep="\t")

    #Get label columns from metadata.csv as pandas.series. For further use Series are converted to lists
    labels_novel_Series = meta_dataframe["Novel"]
    labels_novel = labels_novel_Series.tolist()

    labels_genre_Series = meta_dataframe["Genre"]
    labels_genre = labels_genre_Series.tolist()

    return sparse_matrix, labels_novel, labels_genre

def split_dataset(sparse_matrix, labels):

    X_train, X_test, y_train, y_test = train_test_split(sparse_matrix, labels, test_size=test_size)

    return X_train, X_test, y_train, y_test

def perform_naive_bayes(matrix_train, matrix_test, labels_train, labels_test, logfile):
   
    naive_bayes = MultinomialNB()
    naive_bayes_classifier = naive_bayes.fit(matrix_train, labels_train)
    predicted_nb = naive_bayes_classifier.predict(matrix_test)

    print("Accuracy Naive Bayes:", np.mean(predicted_nb == labels_test), file=logfile)

    """
    zip needs to be used to iterate over two lists simultaneously. Without zip a ValueError is raised! Applies to the other two classifiers aswell
    """

    #for pred, real in zip(predicted_nb, labels_test):
    #   print(pred, real)

    return predicted_nb

def perform_support_vector_machine(matrix_train, matrix_test, labels_train, labels_test, logfile):
    
    support_vector_machine = svm.LinearSVC()
    support_vector_machine_classifier = support_vector_machine.fit(matrix_train, labels_train)
    predicted_svm = support_vector_machine_classifier.predict(matrix_test)

    print("Accuracy LinearSVM:", np.mean(predicted_svm == labels_test), file=logfile)

    #for pred, real in zip(predicted_svm, labels_test):
    #    print(pred, real)

    return predicted_svm

def perform_k_nearest_neighbor(matrix_train, matrix_test, labels_train, labels_test, logfile):
    
    k_nearest_neighbor = KNeighborsClassifier(n_neighbors=nearest_neighbors)
    k_nearest_neighbor_classifier = k_nearest_neighbor.fit(matrix_train, labels_train)
    predicted_knn = k_nearest_neighbor_classifier.predict(matrix_test)

    print("Accuracy k-Nearest Neighbors:", np.mean(predicted_knn == labels_test), "\n", file=logfile)

    #for pred, real in zip(predicted_nb, labels_test):
    #   print(pred, real)

    return predicted_knn

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Reds):
    """
    This function was posted on http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html#sphx-glr-auto-examples-model-selection-plot-confusion-matrix-py
    and gratefully borrowed!
    """

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

def main(result_dir, timestamp):
    
    create_folder(result_dir)
    logfile = create_logfile(result_dir, timestamp)

    sparse_matrix, labels_novels, labels_genres = load_files()

    labels = {"Novels" : labels_novels, "Genres" : labels_genres}
    
    for description, labels in labels.items():
        
        #Classes are novels or genres
        classes = list(set(labels))
        print("Classifying by:", description, file=logfile)

        matrix_train, matrix_test, labels_train, labels_test = split_dataset(sparse_matrix, labels)
        print("Splitting dataset with test_size", test_size, "and k =", nearest_neighbors, "for k-NN", file=logfile)

        #Use different classifiers with same data and labels
        predicted_nb = perform_naive_bayes(matrix_train, matrix_test, labels_train, labels_test, logfile)
        predicted_svm = perform_support_vector_machine(matrix_train, matrix_test, labels_train, labels_test, logfile)
        predicted_knn = perform_k_nearest_neighbor(matrix_train, matrix_test, labels_train, labels_test, logfile)

        #Create confusion matrices for all classifiers
        cnf_matrix_nb = confusion_matrix(labels_test, predicted_nb, labels=classes)
        cnf_matrix_svm = confusion_matrix(labels_test, predicted_svm, labels=classes)
        cnf_matrix_knn = confusion_matrix(labels_test, predicted_knn, labels=classes)
        
        #Plot matrices and safe them to disc  
        """
        NB: plt.show() HAS to be called after plt.safefig() or plots will overlap!
        """
        plot_confusion_matrix(cnf_matrix_nb, classes=classes, title="Naive Bayes")
        plt.savefig(result_dir + "\\" + timestamp + "_bayes_" + description + ".png")
        plt.show()

        plot_confusion_matrix(cnf_matrix_svm, classes=classes, title="Support Vector Machine")
        plt.savefig(result_dir + "\\" + timestamp + "_svm_" + description + ".png")
        plt.show()

        plot_confusion_matrix(cnf_matrix_knn, classes=classes, title="k-Nearest Neighbor")
        plt.savefig(result_dir + "\\" + timestamp + "_knn_" + description + ".png")
        plt.show()

    #Close logfile after all loops have finished
    logfile.close()

main(result_dir, timestamp)
