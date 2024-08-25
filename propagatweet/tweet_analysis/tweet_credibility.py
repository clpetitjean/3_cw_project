"""From a dataframe of tweets, assesses the probability of each being Fake or True"""
from propagatweet.tweet_analysis.classification import load_trained_classifier
from data_cleansing import *


def predict_dataframe(clf, df):
    """
        assigns a binary evaluation of fake or true tweets in a dataframe

        Parameters
        ----------
        clf : scikit-learn pipeline, trained classifier

        df : pandas.dataframe, contains tweets

        Returns
        -------
        df : pandas.dataframe, each tweet being assigned a type of credibility 0 or 1,
             with 0 being true news
    """
    pred = clf.predict(df['full_text'].astype(str))
    df = df.assign(label=pred)
    return df


def predict_proba_dataframe(clf, df):
    """
        assigns a detailed evaluation of fake or true tweets in a dataframe

        Parameters
        ----------
        clf : scikit-learn pipeline, trained classifier

        df : pandas.dataframe, contains tweets

        Returns
        -------
        df : pandas.dataframe, each tweet being assigned a degree of credibility between 0 and 1,
             with 0 being true news
     """
    pred_proba = pd.DataFrame(clf.predict_proba(cleaner_df(df)['full_text'].astype(str)))
    df = df.assign(true_news=pred_proba[0], fake_news=pred_proba[1])
    return df


if __name__ == '__main__':
    df = json_to_dataframe(PATH_DATA_JSON)
    clf = load_trained_classifier()
    df = predict_proba_dataframe(clf, df)
    print(df)
