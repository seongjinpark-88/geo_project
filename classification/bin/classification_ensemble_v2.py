import numpy as np
import os
import sys

from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import KFold, train_test_split, cross_val_score
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, f1_score
from utils import classify
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

from collections import Counter

from joblib import load

def sortListWithIndex(list_of_numbers):
    '''
    sort list with number, and keep indices
    input: list of numbers
    output: sorted list of tuple [(index, number)]
    '''
    enum_list = list(enumerate(list_of_numbers))

    return sorted(enum_list, key = lambda x: x[1])

def train():
    
    print("==============")
    print("START training")
    print("==============")

        

    data = classify.read_data("../data/processed_data.txt")
    label, text = zip(*data)

    train_texts, devel_texts, train_labels, devel_labels = train_test_split(text, label, test_size = 0.1, random_state = 20)
    # create the feature extractor and label encoder
    to_features = classify.TextToFeatures(train_texts)
    to_labels = classify.TextToLabels(train_labels)
        
    # create the feature extractor and label encoder
    to_features_svm = classify.TextToFeatures(text, binary = False)
    to_features_svm.save("svm_features.pickle")
    to_features_nbsvm = classify.TextToFeatures(text, binary = True)
    to_features_nbsvm.save("nbsvm_features.pickle")
    to_labels = classify.TextToLabels(label)
    to_labels.save("labels.pickle")

    # train NBSVM on the training data
    clf1 = classify.NBSVM()
    clf1.train(to_features_nbsvm(text), to_labels(label), alpha = 1.0)
    clf1.save_model("nbsvm_ratio")

    # make predictions on the development data
    # pred1 = clf1.predict(to_features_nbsvm(devel_texts))

    # train SVM on the training data
    clf2 = classify.Classifier()
    clf2.train(to_features_svm(text), to_labels(label))
    clf2.save_model()

    print("FINISH TRAINING")

# train()


def test():

    print("==============")
    print("START testing")
    print("==============")

        

    # data = classify.read_data("../data/processed_data.txt")
    # label, text = zip(*data)

    # train_texts, devel_texts, train_labels, devel_labels = train_test_split(text, label, test_size = 0.1, random_state = 20)

    devel_texts = classify.read_test_data(sys.argv[1])

    to_features_svm = classify.TextToFeatures(load("models/svm_features.pickle"))
    to_features_nbsvm = classify.TextToFeatures(load("models/nbsvm_features.pickle"))
    to_labels = classify.TextToLabels(load("models/labels.pickle"))

    clf1 = classify.NBSVM()
    clf1.load_models()
    clf2 = classify.Classifier()
    clf2.load_model()

    output = open(sys.argv[2], "w")

    for text in devel_texts:
        
        # make predictions on the development data
        pred1 = clf1.predict(to_features_nbsvm([text]))
        pred2 = clf2.predict(to_features_svm([text]))

        # conf1 = clf1.decision_function(to_features_nbsvm([text]))
        # conf2 = clf2.confidence(to_features_svm([text]))

        all_preds = []
        if len(pred1) == len(pred2):
            for i in range(0, np.shape(pred2)[0]):
                all_preds.append([pred1[i], pred2[i]])
            all_preds = np.asarray(all_preds)
            final_preds = np.zeros(len(pred1))

            for i in range(len(all_preds)):
                if 0 in all_preds[i]:
                    final_preds[i] = 0
                else:
                    holder = Counter(all_preds[i])
                    held = [(v, k) for k, v in holder.items()]
                    held = sorted(held, reverse = True)
                    if len(held) > 1:
                        if held[0][0] == held[1][0]:
                            if held[0][1] == 3:
                                final_preds[i] = held[1][1] #don't select 0 class
                            elif held[1][1] == 3:
                                final_preds[i] = held[0][1] #don't select 0 class
                        else: #otherwise, select majority voted
                            final_preds[i] = held[0][1]
                    else: #otherwise, select majority voted
                        final_preds[i] = held[0][1]

            # devel_indices = to_labels(devel_labels)

        # else:
        #     print("The data structures are not of the same size.")
        #     exit()

        # print("REPORT")
        # print(classification_report(devel_indices, final_preds, labels=None, target_names=None, sample_weight=None, digits=3))
        # print("Micro F1: ", f1_score(devel_indices, final_preds, average = 'micro'))
        # print("Macro F1: ", f1_score(devel_indices, final_preds, average = 'macro'))

        # with open(sys.argv[2], "w") as output:
            # res = "%s\t%s\n" % (to_labels.le.inverse_transform([int(final_preds[0])])[0], text)
            # # print(res)
            # output.write(res)
        res = "%s\t%s\n" % (to_labels.le.inverse_transform([int(final_preds[0])])[0], text)
        output.write(res)
        # res = "%s\t%s\n" % (to_labels.le.inverse_transform([int(final_preds[0])])[0], text)
        # print(res)
    output.close()
test()