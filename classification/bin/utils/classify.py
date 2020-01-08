from typing import Iterator, Iterable, Tuple, Text, Union

import numpy as np
import re

from scipy.sparse import issparse, spmatrix, csr_matrix

import pandas as pd


from sklearn.preprocessing import LabelEncoder, normalize, binarize, LabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.utils import check_array, check_X_y
from sklearn.utils.extmath import safe_sparse_dot


NDArray = Union[np.ndarray, spmatrix]


def read_data(data_path: str) -> Iterator[Tuple[Text, Text]]:
    # open file
    f = open(data_path, "r")
    data = f.readlines()
    f.close()

    # create an array to save the result. 
    result = []


    for line in data:
        # split and store label/text
        label, text = line.rstrip().split("\t")
        
        # create tuple and append it to the result array
        tup = (label, text)
        
        result.append(tup)

    return iter(result)


class TextToFeatures:
    def __init__(self, texts: Iterable[Text], binary = False):
        """Initializes an object for converting texts to features.
        :param texts: The training texts.
        """

        # build word CountVectorizer (ngram = 1, 2)
        self.vectorizer = CountVectorizer(
                                          ngram_range = (1, 2), 
                                          lowercase = False, 
                                          binary = binary
                                          )

        # word vectors
        self.X = self.vectorizer.fit_transform(texts)

    def index(self, feature: Text):
        """Returns the index in the vocabulary of the given feature value.

        :param feature: A feature
        :return: The unique integer index associated with the feature.
        """

        # get the integer index of a given feature
        int_index = self.vectorizer.vocabulary_[feature]

        return int_index

    def __call__(self, texts: Iterable[Text]) -> NDArray:
        """Creates a feature matrix from a sequence of texts.

        Each row of the matrix corresponds to one of the input texts. The value
        at index j of row i is the value in the ith text of the feature
        associated with the unique integer j.

        It is up to the implementer what the value of a feature that is present
        in a text should be, though a common choice is 1. Features that are
        absent from a text will have the value 0.

        :param texts: A sequence of texts.
        :return: A matrix, with one row of feature values for each text.
        """

        # word vectors
        features = self.vectorizer.transform(texts).toarray()

        return features


class TextToLabels:
    def __init__(self, labels: Iterable[Text]):
        """Initializes an object for converting texts to labels.

        During initialization, the provided training labels are analyzed to
        determine the vocabulary, i.e., all labels that the converter will
        support. Each such label will be associated with a unique integer index
        that may later be accessed via the .index() method.

        :param labels: The training labels.
        """

        # create label encoder
        self.le = LabelEncoder()

        # define indices for classes
        self.le.fit(labels)

    def index(self, label: Text) -> int:
        """Returns the index in the vocabulary of the given label.

        :param label: A label
        :return: The unique integer index associated with the label.
        """

        # get index of given label
        int_index = self.le.transform([label])[0]

        return int_index

    def __call__(self, labels: Iterable[Text]) -> NDArray:
        """Creates a label vector from a sequence of labels.

        Each entry in the vector corresponds to one of the input labels. The
        value at index j is the unique integer associated with the jth label.

        :param labels: A sequence of labels.
        :return: A vector, with one entry for each label.
        """

        # convert labels to indices
        int_indice = self.le.transform(labels)

        return int_indice


class Classifier:
    def __init__(self):
        """Initalizes a logistic regression classifier.
        """

        # call a model which uses
        # L2 Penalization with 2.0 strength
        self.classifier = LinearSVC(C = 2.0, penalty = 'l2')

    def train(self, features: NDArray, labels: NDArray) -> None:
        """Trains the classifier using the given training examples.

        :param features: A feature matrix, where each row represents a text.
        Such matrices will typically be generated via TextToFeatures.
        :param labels: A label vector, where each entry represents a label.
        Such vectors will typically be generated via TextToLabels.
        """

        # train the model with given features and labels

        self.classifier.fit(features, labels)

    def predict(self, features: NDArray) -> NDArray:
        """Makes predictions for each of the given examples.

        :param features: A feature matrix, where each row represents a text.
        Such matrices will typically be generated via TextToFeatures.
        :return: A prediction vector, where each entry represents a label.
        """

        # make prediction with given feature matrix and
        # return a prediction vector
        return self.classifier.predict(features)

class NBSVM:
    def __init__(self):
        # create list to save LinearSVM for one vs rest
        self.svms = []
        self.labelbin = LabelBinarizer()

    def compute_ratios(self, X, Y, alpha):
        '''
        label
        0: negative
        1: negative&support
        2: support
        3: unrelated
        '''

        # Get number of classes and features
        n_effective_classes = Y.shape[1]
        total_sent, n_features = X.shape
        
        # Create np.ones for ratio and feature
        f_list = np.full(shape = (n_effective_classes, n_features), fill_value = alpha, dtype = np.float64)

        # Make a feature matrix for each label        
        for i in range(0, total_sent):
            # decide which label the sentence is
            lab = np.argmax(Y[i])
            # add it to the feature matrix
            f_list[lab] += X[i]

        # Calculate the ratio for each class (one vs rest)
        for j in range(0, n_effective_classes):
            # p/||p||
            x = (f_list[j]/abs(f_list[j].sum()))

            n_x = np.delete(f_list, j, 0)
            # q/||q||
            y = (n_x.sum(axis = 0)/abs(n_x.sum()))

            # calculate r
            # r = np.log(x/y)
            r = np.log((f_list[j]/abs(f_list[j].sum()))/(n_x.sum(axis = 0)/abs(n_x.sum())))
            self.ratios[j] = r

    def train(self, features: NDArray, labels: NDArray, alpha: 1.0) -> None:
        X, y = check_X_y(features, labels, 'csr')

        # get number of features
        _, n_features = X.shape
        
        # change label into one-hot
        Y = self.labelbin.fit_transform(y)
        self.classes_ = self.labelbin.classes_
        
        Y = Y.astype(np.float64)

        self.n_effective_classes = Y.shape[1]
        # self.class_count_ = np.zeros(shape = n_effective_classes, dtype=np.float64)
        self.ratios = np.full(shape = (self.n_effective_classes, n_features), fill_value = 1, dtype = np.float64)

        # print("Computing NB ratio...")
        self.compute_ratios(features, Y, alpha = 1)

        for i in range(self.n_effective_classes):
            X_i = np.multiply(X, self.ratios[i])
            svm = LinearSVC(C = 2.0, penalty = 'l2')
            Y_i = Y[:,i]
            svm.fit(X_i, Y_i)
            self.svms.append(svm)
        return self

    def predict(self, features: NDArray) -> NDArray:
        # n_effective_class = self.class_count_.shape[0]
        beta = 0.75
        n_examples = features.shape[0]

        D = np.zeros(shape = (self.n_effective_classes, n_examples))

        for i in range(self.n_effective_classes):
            X_i = np.multiply(features, self.ratios[i])
            w_bar = (abs(self.svms[i].coef_).sum())/features.shape[1]
            w_prime = (1 - beta)*(w_bar) + (beta * self.svms[i].coef_)
            result = np.sign(np.dot(X_i, w_prime.T) + self.svms[i].intercept_)
            D[i] = np.reshape(result, 40)

        return self.classes_[np.argmax(D, axis = 0)]

