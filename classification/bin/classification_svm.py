import numpy as np
import os

from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import classification_report, f1_score
from utils import classify
# import matplotlib.pyplot as plt

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

    kf = KFold(n_splits=10, shuffle = True, random_state = 77)

    kf.get_n_splits(data)

    devel_data = []
    prediction = []

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

        # create the feature extractor and label encoder
        to_features = classify.TextToFeatures(train_texts)
        to_labels = classify.TextToLabels(["__label__UNRELATED", "__label__SUPPORT", "__label__NEGATE", "__label__NEGATE,SUPPORT"])

        # train the classifier on the training data
        classifier = classify.Classifier()
        classifier.train(to_features(train_texts), to_labels(train_labels))

        # make predictions on the development data
        predicted_indices = classifier.predict(to_features(devel_texts))

        # measure performance of predictions
        devel_indices = to_labels(devel_labels)
        f1 = f1_score(devel_indices, predicted_indices, average = "micro")
        accuracy = accuracy_score(devel_indices, predicted_indices)

        # calculate baseline performance (predict everything as unrelated)
        bs_indices = np.full((len(predicted_indices)), 2)
        bs_f1 = f1_score(devel_indices, bs_indices, average = "micro")
        bs_accuracy = accuracy_score(devel_indices, bs_indices)

        # print out performance
        devel_data.extend(devel_indices)
        prediction.extend(predicted_indices)

        print("%d FOLD" % i)
        bs_msg = "BASELINE: {:.1%} F1 and {:.1%} accuracy on GEOSCIENCE data"
        print(bs_msg.format(bs_f1, bs_accuracy))

        msg = "PREDICTION: {:.1%} F1 and {:.1%} accuracy on GEOSCIENCE data"
        print(msg.format(f1, accuracy))
        print(classification_report(devel_indices, predicted_indices, labels=None, target_names=None, sample_weight=None, digits=3))
        print("Micro F1: ", f1_score(devel_indices, predicted_indices, average = 'micro'))
        print("Macro F1: ", f1_score(devel_indices, predicted_indices, average = 'macro'))

        os.remove("train.txt")
        os.remove("test.txt")
        i += 1

    print(to_labels(["__label__UNRELATED", "__label__SUPPORT", "__label__NEGATE", "__label__NEGATE,SUPPORT"]))
    print("\n\n================\n\n")
    print("FINAL REPORT")
    print(classification_report(devel_data, prediction, labels=None, target_names=None, sample_weight=None, digits=3))
    print("Micro F1: ", f1_score(devel_data, prediction, average = 'micro'))
    print("Macro F1: ", f1_score(devel_data, prediction, average = 'macro'))

run_kfold()

def run_error_anal():

    data = classify.read_data("../data/processed_data.txt")
    label, text = zip(*data)

    train_texts, devel_texts, train_labels, devel_labels = train_test_split(text, label, test_size = 0.1, random_state = 20)
    # create the feature extractor and label encoder
    to_features = classify.TextToFeatures(train_texts)
    to_labels = classify.TextToLabels(train_labels)

    # train the classifier on the training data
    classifier = classify.Classifier()
    classifier.train(to_features(train_texts), to_labels(train_labels))

    # make predictions on the development data
    predicted_indices = classifier.predict(to_features(devel_texts))
    

    # measure performance of predictions
    devel_indices = to_labels(devel_labels)
    f1 = f1_score(devel_indices, predicted_indices, average = "micro")
    accuracy = accuracy_score(devel_indices, predicted_indices)

    # calculate baseline performance (predict everything as unrelated)
    bs_indices = np.full((len(predicted_indices)), 2)
    bs_f1 = f1_score(devel_indices, bs_indices, average = "micro")
    bs_accuracy = accuracy_score(devel_indices, bs_indices)

    # print out performance
    bs_msg = "BASELINE: {:.1%} F1 and {:.1%} accuracy on GEOSCIENCE data"
    print(bs_msg.format(bs_f1, bs_accuracy))

    msg = "PREDICTION: {:.1%} F1 and {:.1%} accuracy on GEOSCIENCE data"
    print(msg.format(f1, accuracy))
    print(classification_report(devel_indices, predicted_indices, labels=None, target_names=None, sample_weight=None, digits=3))
    print("Micro F1: ", f1_score(devel_indices, predicted_indices, average = 'micro'))
    print("Macro F1: ", f1_score(devel_indices, predicted_indices, average = 'macro'))

    result_weight = np.vstack((to_features.vectorizer.get_feature_names(),classifier.classifier.coef_)).transpose()

    feature_weights = classifier.classifier.coef_.tolist()


    vocab_list = to_features.vectorizer.get_feature_names()
    
    negate_weight = feature_weights[0]
    ns_weight = feature_weights[1]
    support_weight = feature_weights[2]
    unrelated_weight = feature_weights[3]

    sorted_negate = sortListWithIndex(negate_weight)[-100:]
    sorted_ns = sortListWithIndex(ns_weight)[-100:]
    sorted_support = sortListWithIndex(support_weight)[-100:]
    sorted_unrelated = sortListWithIndex(unrelated_weight)[-100:]


    outFile = open("../data/top100_weight_4class.txt", "w")

    header = "ranking\tnegate\tnegate&support\tsupport\tunrelated\n"
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

# run_error_anal()
 

