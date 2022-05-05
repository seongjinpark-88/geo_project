import numpy as np
import os

from sklearn.metrics import f1_score, accuracy_score
from sklearn.model_selection import KFold, train_test_split
from sklearn.metrics import classification_report, f1_score
from utils import classify
from torch.utils.data import DataLoader
# import matplotlib.pyplot as plt

import torch
from torchmetrics import F1Score
from transformers import AutoTokenizer, AdamW, get_scheduler
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

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
        train_labels, train_texts = classify.read_data_list("train.txt")
        
        # get texts and labels from the development data
        dev_labels, dev_texts = classify.read_data_list("test.txt")

        # tokenize text
        tokenizer = AutoTokenizer.from_pretrained("allenai/scibert_scivocab_uncased", model_max_length=512)

        train_encodings = tokenizer(train_texts, truncation=True, padding=True)
        dev_encodings = tokenizer(dev_texts, truncation=True, padding=True)

        train_dataset = classify.TextDataset(train_encodings, train_labels)
        dev_dataset = classify.TextDataset(dev_encodings, dev_labels)

        # train the classifier on the training data
        classifier = AutoModelForSequenceClassification.from_pretrained("allenai/scibert_scivocab_uncased", num_labels=4)
        
        train_dataloader = DataLoader(train_dataset, batch_size=4, shuffle=True)
        dev_dataloader = DataLoader(dev_dataset, batch_size=2, shuffle=True)

        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

        classifier.to(device)
        classifier.train()

        optim = AdamW(classifier.parameters(), lr=5e-5)
        num_epochs = 3
        num_training_steps = num_epochs * len(train_dataloader)
        lr_scheduler = get_scheduler(
            name="linear", 
            optimizer=optim, 
            num_warmup_steps=0, 
            num_training_steps=num_training_steps
        )

        metric = F1Score(num_classes=4)

        for epoch in range(5):
            classifier.train()
            for batch in train_dataloader:
                optim.zero_grad()
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)

                outputs = classifier(input_ids, attention_mask=attention_mask, labels=labels)
                
                loss = outputs.loss
                loss.backward()
                
                optim.step()
                lr_scheduler.step()

        
        classifier.eval()
        predicted_indices = []
        gold_labels = []
        for batch in dev_dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            with torch.no_grad():
                outputs = classifier(input_ids, attention_mask=attention_mask, labels=labels)
            
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1)
            predicted_indices.extend(prediction)
            gold_labels.extend(labels)



        # measure performance of predictions
        f1 = f1_score(gold_labels, predicted_indices, average = "micro")
        accuracy = accuracy_score(gold_labels, predicted_indices)

        # print out performance
        devel_data.extend(gold_labels)
        prediction.extend(predicted_indices)

        print("%d FOLD" % i)
        msg = "PREDICTION: {:.1%} F1 and {:.1%} accuracy on GEOSCIENCE data"
        print(msg.format(f1, accuracy))
        print(classification_report(gold_labels, predicted_indices, labels=None, target_names=None, sample_weight=None, digits=3))
        print("Micro F1: ", f1_score(gold_labels, predicted_indices, average = 'micro'))
        print("Macro F1: ", f1_score(gold_labels, predicted_indices, average = 'macro'))

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
 

