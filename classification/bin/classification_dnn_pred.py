import numpy as np
import sys

from sklearn.metrics import f1_score
from utils import classify

import pickle
from joblib import load

def sortListWithIndex(list_of_numbers):
    '''
    sort list with number, and keep indices
    input: list of numbers
    output: sorted list of tuple [(index, number)]
    '''
    enum_list = list(enumerate(list_of_numbers))

    return sorted(enum_list, key = lambda x: x[1])

print("==============")
print("START testing")
print("==============")

    
# read test data
devel_texts = classify.read_test_data(sys.argv[1])

# open saved feature and label encoders
to_features_svm = classify.TextToFeatures(pickle.load(open("models/svm_features.pickle", "rb")))
to_labels = classify.TextToLabels(load("models/labels.pickle"))

# load dnn classifier
dnn_clf = classify.DNN_Classifier()
dnn_clf.load_model()

# make a prediction
print("Make DNN pred")
pred3 = dnn_clf.predict(to_features_svm(devel_texts))
pred3 = np.asarray(pred3)

# check the output
print(pred3)
print(np.shape(pred3))
print(devel_texts[0])
print(np.shape(devel_texts))

# write an output
with open(sys.argv[2], "w") as output:
    for pred, text in zip(pred3, devel_texts):
        print(pred, text)
        res = "%s\t%s\n" % (to_labels.le.inverse_transform([int(pred)])[0], text)
        print(res)
        output.write(res)
