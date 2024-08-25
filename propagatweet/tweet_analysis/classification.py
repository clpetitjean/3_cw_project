"""loads the training dataset, trains the classifier, evaluates it and saves it"""
import pandas as pd
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from src.env import *


def load_training_dataset():
    """
    Loads the default training dataset

    Returns
    -------
    (data, labels) : Tuple

    data : array-like, shape (n_samples, n_features), default=None
           The training input sample

    labels : array-like, shape (n_samples,)
             The target values. An array of int.
    """
    df = pd.read_csv(PATH_DATASET_TRAIN)
    data = df['text'].astype(str)
    labels = df['label']
    return data, labels


def save_model(model, path=PATH_TRAINED_MODEL):
    """
    Saves the model in the  specified path

    Parameters
    ----------
    model : scikit-learn model
            The model to save
    path : str
           The path to the file

    """
    dump(model, path)


def pipeline_setup(classifier_type='xgb'):
    """
    Setup of the pipeline

    Parameters
    ----------
    classifier_type : str
                      The machine learning model chosen by the user

    Returns
    -------
    pipeline : scikit-learn pipeline
               The pipeline of the classifier
    """
    if classifier_type == 'xgb':
        model = XGBClassifier()
    elif classifier_type == 'nb':
        model = MultinomialNB()
    elif classifier_type == 'svm':
        model = SVC()

    data, labels = load_training_dataset()
    pipeline = Pipeline(steps=[
        ('count_vect', CountVectorizer(stop_words='english')),
        ('tfidf_transformer', TfidfTransformer()),
        ('clf', model)
    ])
    pipeline.fit(data, labels)
    return pipeline


def bayes_selection(data, labels, test_size=0.2, random_state=25):
    """
    Cross-validate Naive Bayes models to select the best one based on accuracy.
    Then evaluates the model on the test data set and prints confusion matrix and metrics.

    Parameters
    ----------
    data : array-like, shape (n_samples, n_features), default=None
           The testing input sample
           If None, the training dataset is used
    labels : array-like, shape (n_samples,), default=None
             The target values. An array of int.
             If None, the training dataset is used
    test_size : float or int, default=0.2
                If float, should be between 0.0 and 1.0 and represent
                the proportion of the dataset to include in the test split.
                If int, represents the absolute number of test samples.
                If None, the value is set to the complement of the train size.
    random_state : int, RandomState instance or None, default=None
                   Controls the shuffling applied to the data before applying the split.
                   Pass an int for reproducible output across multiple function calls.

    Returns
    -------
    best_model : Pipeline
                 The best model pipeline based on evaluation metrics.
    """

    nb = pipeline_setup('nb')

    parameters = {
        'clf__alpha': [0.1, 1, 5, 10],
        'clf__fit_prior': [True, False]
    }

    if data is None or labels is None:
        data, labels = load_training_dataset()

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=test_size,
                                                        random_state=random_state)

    clf = GridSearchCV(nb, parameters, n_jobs=-1, cv=3, scoring='accuracy', verbose=1, refit=True)

    best_nb = clf.fit(x_train, y_train)

    y_pred = best_nb.best_estimator_.predict(x_test)
    report = classification_report(y_test, y_pred)
    c = confusion_matrix(y_test, y_pred)
    print(report, c)
    return best_nb.best_estimator_


def svm_selection(data, labels, test_size=0.2, random_state=25):
    """
    Cross-validate Support Vector Machine models to select the best one based on accuracy.
    Then evaluates the model on the test data set and prints confusion matrix and metrics.

    Parameters
    ----------
    data : array-like, shape (n_samples, n_features), default=None
           The testing input sample
           If None, the training dataset is used
    labels : array-like, shape (n_samples,), default=None
             The target values. An array of int.
             If None, the training dataset is used
    test_size : float or int, default=0.2
                If float, should be between 0.0 and 1.0 and represent
                the proportion of the dataset to include in the test split.
                If int, represents the absolute number of test samples.
                If None, the value is set to the complement of the train size.
    random_state : int, RandomState instance or None, default=None
                   Controls the shuffling applied to the data before applying the split.
                   Pass an int for reproducible output across multiple function calls.

    Returns
    -------
    best_model : Pipeline
                 The best model pipeline based on evaluation metrics.
    """

    svm = pipeline_setup('svm')

    parameters = [
        {
            'clf__C': [1, 10, 100],
            'clf__kernel': ['linear']
        },
        {
            'clf__C': [1, 10, 100],
            'clf__gamma': [1, 0.1, 0.01, 0.001],
            'clf__kernel': ['rbf']}
    ]

    if data is None or labels is None:
        data, labels = load_training_dataset()

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=test_size,
                                                        random_state=random_state)

    clf = GridSearchCV(svm, parameters, n_jobs=-1, cv=3, scoring='accuracy', verbose=1, refit=True)

    best_svm = clf.fit(x_train, y_train)

    y_pred = best_svm.best_estimator_.predict(x_test)
    report = classification_report(y_test, y_pred)
    c = confusion_matrix(y_test, y_pred)
    print('model trained', report, c)
    return best_svm.best_estimator_


def xgb_selection(data, labels, test_size=0.2, random_state=25):
    """
    Cross-validate XGBClassifiers to select the best one based on accuracy.
    Then evaluates the model on the test data set and prints confusion matrix and metrics.

    Parameters
    ----------
    data : array-like, shape (n_samples, n_features), default=None
           The testing input sample
           If None, the training dataset is used
    labels : array-like, shape (n_samples,), default=None
             The target values. An array of int.
             If None, the training dataset is used
    test_size : float or int, default=0.2
                If float, should be between 0.0 and 1.0 and represent
                the proportion of the dataset to include in the test split.
                If int, represents the absolute number of test samples.
                If None, the value is set to the complement of the train size.
    random_state : int, RandomState instance or None, default=None
                   Controls the shuffling applied to the data before applying the split.
                   Pass an int for reproducible output across multiple function calls.

    Returns
    -------
    best_model : Pipeline
                 The best model pipeline based on evaluation metrics.
    """

    xgb = pipeline_setup('xgb')

    parameters = {
        'clf__objective': ['binary:logistic'],
        'clf__n_estimators': [100, 300],
        'clf__learning_rate': [0.01, 0.1],
        'clf__max_depth': [3, 4]
    }

    if data is None or labels is None:
        data, labels = load_training_dataset()

    x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=test_size,
                                                        random_state=random_state)

    clf = GridSearchCV(xgb, parameters, n_jobs=-1, cv=3, scoring='accuracy', verbose=1, refit=True)

    best_xgb = clf.fit(x_train, y_train)

    y_pred = best_xgb.best_estimator_.predict(x_test)
    report = classification_report(y_test, y_pred)
    c = confusion_matrix(y_test, y_pred)
    print(report, c)
    return best_xgb.best_estimator_


def save_best_model():
    """
    Save the best naive bayes model (for calculation purposes) trained on the full dataset.
    """
    data, labels = load_training_dataset()
    best_model = bayes_selection(data, labels)
    save_model(best_model)
    return best_model


def load_trained_classifier():
    """
    Loads the trained classifier

    Returns
    -------
    pipe : Pipeline
        Returns the pipeline of the classifier

    """
    trained_model = load(PATH_TRAINED_MODEL)
    return trained_model


if __name__ == '__main__':
    pipe = save_best_model()
