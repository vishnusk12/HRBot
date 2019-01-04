# -*- coding: utf-8 -*-
"""
Created on Thu May 17 12:47:42 2018

@author: Vishnu
"""

import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib

os.chdir('C:/Users/hp/eclipse-workspace/HRBot/HRBot/')
count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()

if __name__ == '__main__':
    data_frame = pd.read_csv('intent_training.csv')
    data_frame['user_input'] = data_frame['user_input'].astype(str)
    X_train_counts = count_vect.fit_transform(data_frame['user_input'])
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
                         ('clf', SGDClassifier(loss='hinge', penalty='l2',
                                               alpha=1e-3, n_iter=5, random_state=42)), ])
    text_clf.fit(data_frame['user_input'], data_frame['label'])
    joblib.dump(text_clf, 'intent_model.pkl')
