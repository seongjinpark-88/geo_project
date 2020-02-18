import numpy as np
import os

from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import KFold, train_test_split, cross_val_score
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report, f1_score
from utils import classify
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

from collections import Counter

def sortListWithIndex(list_of_numbers):
    '''
    sort list with number, and keep indices
    input: list of numbers
    output: sorted list of tuple [(index, number)]
    '''
    enum_list = list(enumerate(list_of_numbers))

    return sorted(enum_list, key = lambda x: x[1])

def run_kfold():
    with open("../data/processed_data.txt") as f:
        data = f.readlines()

    data = np.asarray(data)

    kf = KFold(n_splits=10, shuffle = False, random_state = 77)

    kf.get_n_splits(data)

    devel_data = []
    prediction = []
    test_sent = []

    print("==============")
    print("START training")
    print("==============")

    i = 1
    for train_index, test_index in kf.split(data):
        
        train = open("train.txt", "w")
        test = open("test.txt", "w")
        
        TRAIN_DATA = list(data[train_index])
        TEST_DATA = list(data[test_index])

        train.write("".join(TRAIN_DATA))
        test.write("".join(TEST_DATA))

        # get texts and labels from the training data
        train_examples = classify.read_data("train.txt")
        train_labels, train_texts = zip(*train_examples)
        
        # get texts and labels from the development data
        devel_examples = classify.read_data("test.txt")
        devel_labels, devel_texts = zip(*devel_examples)

        test_sent.extend(devel_texts)

        # create the feature extractor and label encoder
        to_features_svm = classify.TextToFeatures(train_texts, binary = False)
        to_features_nbsvm = classify.TextToFeatures(train_texts, binary = True)
        to_labels = classify.TextToLabels(train_labels)

        # train NBSVM on the training data
        clf1 = classify.NBSVM()
        clf1.train(to_features_nbsvm(train_texts), to_labels(train_labels), alpha = 1.0)

        # make predictions on the development data
        pred1 = clf1.predict(to_features_nbsvm(devel_texts))

        # train SVM on the training data
        clf2 = classify.Classifier()
        clf2.train(to_features_svm(train_texts), to_labels(train_labels))

        # make predictions on the development data
        pred2 = clf2.predict(to_features_svm(devel_texts))

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

            devel_indices = to_labels(devel_labels)
            
            devel_data.extend(devel_indices)
            prediction.extend(final_preds)

        else:
            print("The data structures are not of the same size.")
            exit()

        os.remove("train.txt")
        os.remove("test.txt")
        i += 1

    print("\n\n================\n\n")
    print("FINAL REPORT")
    print(classification_report(devel_data, prediction, labels=None, target_names=None, sample_weight=None, digits=3))
    print("Micro F1: ", f1_score(devel_data, prediction, average = 'micro'))
    print("Macro F1: ", f1_score(devel_data, prediction, average = 'macro'))

    with open("../data/prediction_result.txt", "a") as output:
        for i in range(0, len(prediction)):
            res = "%s\t%s\n" % (prediction[i], test_sent[i])
            print(res)
            output.write(res)
run_kfold()

def run_error_anal():

    data = classify.read_data("../data/processed_data.txt")
    label, text = zip(*data)

    train_texts, devel_texts, train_labels, devel_labels = train_test_split(text, label, test_size = 0.1, random_state = 20)
    # create the feature extractor and label encoder
    to_features = classify.TextToFeatures(train_texts)
    to_labels = classify.TextToLabels(train_labels)

    # train the classifier on the training data
    classifier = classify.NBSVM()
    print("START TRAINING....")
    classifier.train(to_features(train_texts), to_labels(train_labels))

    # make predictions on the development data
    predicted_indices = classifier.predict(to_features(devel_texts))

    # measure performance of predictions
    devel_indices = to_labels(devel_labels)
    f1 = f1_score(devel_indices, predicted_indices, average = "micro")
    accuracy = accuracy_score(devel_indices, predicted_indices)

    # print out performance
    msg = "PREDICTION: {:.1%} F1 and {:.1%} accuracy on GEOSCIENCE data"
    print(msg.format(f1, accuracy))
    print(classification_report(devel_indices, predicted_indices, labels=None, target_names=None, sample_weight=None, digits=3))
    print("Micro F1: ", f1_score(devel_indices, predicted_indices, average = 'micro'))
    print("Macro F1: ", f1_score(devel_indices, predicted_indices, average = 'macro'))

    vocab_list = to_features.vectorizer.get_feature_names()
    
    negate_weight = classifier.svms[0].coef_.tolist()[0]
    ns_weight = classifier.svms[1].coef_.tolist()[0]
    support_weight = classifier.svms[2].coef_.tolist()[0]
    unrelated_weight = classifier.svms[3].coef_.tolist()[0]
    
    sorted_negate = sortListWithIndex(negate_weight)[-100:]
    sorted_ns = sortListWithIndex(ns_weight)[-100:]
    sorted_support = sortListWithIndex(support_weight)[-100:]
    sorted_unrelated = sortListWithIndex(unrelated_weight)[-100:]


    outFile = open("../data/top100_weight_NBSVM.txt", "w")

    header = "ranking\tnegate&support\tnegate\tsupport\tunrelated\n"
    outFile.write(header)

    for i in range(0, 100):
        rank = i + 1
        neg = vocab_list[sorted_negate[i][0]]
        ns = vocab_list[sorted_ns[i][0]]
        sup = vocab_list[sorted_support[i][0]]
        unl = vocab_list[sorted_unrelated[i][0]]

        result = str(rank) + "\t" + neg + "\t" + ns + "\t" + sup + "\t" + unl + "\n"
        outFile.write(result)

    outFile.close()

    # np.savetxt("../data/nbsvm_weight_result.txt", result_weight, delimiter="\t", 
    #     fmt='%s',
    #     header="feature\tnegative\tnegative&support\tsupport\tunrelated")

    # print(len(to_features.vectorizer.vocabulary_))
    # print(to_features.vectorizer.get_feature_names())
    # plot_coefficients(classifier.classifier, to_features.vectorizer.get_feature_names())
    


# run_error_anal()
 

