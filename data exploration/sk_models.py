import numpy as np
import pandas as np
from sklearn.linear_model import LogisticRegression, Ridge, Lasso
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report, confusion_matrix


class SKModel:

    def __init__(self, model, cv_k):
        if model == 0:
            self.clf = LogisticRegression()
        elif model == 1:
            self.clf = RandomForestClassifier()
        elif model == 2:
            self.clf = LDA()
        elif model == 3:
            self.clf = BernoulliNB()
        elif model == 4:
            self.clf = KNeighborsClassifier()
        elif model == 5:
            self.clf = DecisionTreeClassifier()
        elif model == 6:
            self.clf = MLPClassifier(hidden_layer_sizes=(10, 10, 10), max_iter=1000)
        else:
            self.clf = None

        self.cv_k = cv_k


    def cross_validate(self, X_train, y_train):
        scores = cross_val_score(self.clf, X_train, y_train, cv=self.cv_k)
        return sum(scores)/len(scores)

    def generate_predictions(self, X_train, y_train, X_test):
        self.clf.fit(X_train, y_train)
        predictions = self.clf.predict(X_test)
        return predictions

    def evaluate(self, y_test, predictions):
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))
