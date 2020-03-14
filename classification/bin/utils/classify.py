from typing import Iterator, Iterable, Tuple, Text, Union

import numpy as np
import re

from scipy.sparse import issparse, spmatrix, csr_matrix

from sklearn.preprocessing import LabelEncoder, normalize, binarize, LabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.utils import check_array, check_X_y
from sklearn.utils.extmath import safe_sparse_dot

import pickle

import sys
import os
import glob
import json

from joblib import dump, load


NDArray = Union[np.ndarray, spmatrix]

def extract_texts(data_path):
    texts = []
    for file in glob.glob(os.path.join(data_path, '*.json')):
        print(file)
        with open(os.path.join(data_path, file), "r") as f:
            data = json.load(f)

        try:
            data = data["metadata"]
            if "title" in data.keys():
                # print("Title exists")
                title = data["title"]
            
            # print(title)
            
            contents = ""
            
            if "abstractText" in data.keys():
                # print("Abstract exists")
                abstract = data["abstractText"]
                contents = contents + "Abstract: " + abstract
                # print(contents)

            else:
                if "sections" in data.keys():
                    # print("Introduction exists")
                    abstract = data["sections"]
                    for items in abstract:
                        if "heading" in items.keys():
                            if re.findall(r"introduction", items["heading"], re.I):
                                text = items["text"]
                                words = text.split()

                                if len(words) > 200:
                                    introduction = " ".join(words[:200])
                                else:
                                    introduction = text 

                                contents = contents + "Introduction: " + introduction
                                # print(contents)

            if "sections" in data.keys():
                sections = data["sections"]
                for sec in sections:
                    if "heading" in sec.keys():
                        if re.findall(r"conclus", str(sec["heading"]), re.I):
                            # print("Conclusion/discussion exists")
                            text = sec["text"]
                            text = text.replace("\n", "")
                            head = sec["heading"]
                            contents = contents + " " + head + ": " + text
                            # print(contents)

            result = title + "\t" + contents
            # print(result)
            texts.append(result)

        except:
            pass 

    return texts


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

def read_test_data(data_path: str) -> Iterator[Tuple[Text]]:
    #open file
    # f = open(data_path, "r")
    # data = f.readlines()
    # f.close()
    data = extract_texts(data_path)
    # iteration
    # result = []
    
    for line in data:    
        text = line.rstrip()
        yield text
        # result.append(text)

    # return result

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

        try: 
            # word vectors
            self.X = self.vectorizer.fit_transform(texts)
        except:
            self.vectorizer = texts

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

    def save(self, feature_path):
        dump(self.vectorizer, open(feature_path, "wb"))



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

        try:
            # define indices for classes
            self.le.fit(labels)
        except:
            self.le = labels

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

    def save(self, label_path):
        dump(self.le, open(label_path, "wb"))        



class Classifier:
    def __init__(self):
        """Initalizes a logistic regression classifier.
        """

        # call a model which uses
        # L2 Penalization with 2.0 strength
        self.classifier = LinearSVC(C = 2.0, penalty = 'l2')

    def load_model(self):
        self.classifier = load("models/linearSVM.joblib")

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

    def confidence(self, features: NDArray) -> NDArray:
        return self.classifier.decision_function(features)

    def save_model(self) -> None:
        # save the model
        # model name should be written without the extension
        model_name = "linearSVM.joblib"
        dump(self.classifier, open(model_name, "wb"))

class NBSVM:
    def __init__(self):
        # create list to save LinearSVM for one vs rest
        self.svms = []
        self.labelbin = LabelBinarizer()

    def load_models(self):
        self.svms = [load("models/nbsvm_n.joblib"), load("models/nbsvm_ns.joblib"), load("models/nbsvm_s.joblib"), load("models/nbsvm_unr.joblib")]
        self.labelbin = load("models/nbsvm_label.pickle")
        self.ratios = np.load("models/nbsvm_ratio.npy")
        self.n_effective_classes = np.shape(self.ratios)[0]
        self.classes_ = self.labelbin.classes_

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
        self.ratios = np.full(shape = (self.n_effective_classes, n_features), fill_value = 1, dtype = np.float64)

        # Computing NB ratio
        self.compute_ratios(features, Y, alpha = 1)

        for i in range(self.n_effective_classes):
            X_i = np.multiply(X, self.ratios[i])
            svm = LinearSVC(C = 2.0, penalty = 'l2') 
            Y_i = Y[:,i]
            svm.fit(X_i, Y_i)
            self.svms.append(svm)
        return self

    def predict(self, features: NDArray) -> NDArray:
        # parameters
        beta = 0.75
        n_examples = features.shape[0]

        D = np.zeros(shape = (self.n_effective_classes, n_examples))

        for i in range(self.n_effective_classes):
            X_i = np.multiply(features, self.ratios[i])
            w_bar = (abs(self.svms[i].coef_).sum())/features.shape[1]
            w_prime = (1 - beta)*(w_bar) + (beta * self.svms[i].coef_)
            result = np.sign(np.dot(X_i, w_prime.T) + self.svms[i].intercept_)
            D[i] = np.reshape(result, n_examples)

        return self.classes_[np.argmax(D, axis = 0)]

    def confidence(self, features: NDArray) -> NDArray:
                # parameters
        beta = 0.75
        n_examples = features.shape[0]

        D = np.zeros(shape = (self.n_effective_classes, n_examples))

        for i in range(self.n_effective_classes):
            X_i = np.multiply(features, self.ratios[i])
            w_bar = (abs(self.svms[i].coef_).sum())/features.shape[1]
            w_prime = (1 - beta)*(w_bar) + (beta * self.svms[i].coef_)
            result = np.sign(np.dot(X_i, w_prime.T) + self.svms[i].intercept_)  
            D[i] = np.reshape(result, n_examples)

    def save_model(self, ratio_name):
        names = ("n", "ns", "s", "unr")
        np.save(ratio_name, self.ratios)
        dump(self.labelbin, open("nbsvm_label.pickle", "wb"))        
        for i in range(self.n_effective_classes):
            model_name = "nbsvm_" + names[i] + ".joblib"
            dump(self.svms[i], open(model_name, "wb"))    

