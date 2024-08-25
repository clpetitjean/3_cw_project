"""From a list of tweets, plot both the evolution in time and space of truest and most fake news"""
import seaborn as sns
from propagatweet.visualization.cumulative_visualisation import *
from propagatweet.tweet_analysis.tweet_credibility import *
from propagatweet.twitter_connect.tweet_storage import *
from propagatweet.utils.path_management import *
from propagatweet.visualization.graph_visualisation import *


def retweets_on_fake_news_scatterplot(df):
    """
            displays the tweets in a plan with fake_news probability as x_axis and favorite_count as y_axis, with size
            depending on retweet_count

            Parameters
            ----------
            clf : scikit-learn pipeline, trained classifier

            df : pandas.dataframe, contains tweets

    """

    sns.set_theme(style="whitegrid")
    # Draw a scatter plot while assigning point colors and sizes to different
    # variables in the dataset
    f, ax = plt.subplots(figsize=(6.5, 6.5))
    sns.despine(f, left=True, bottom=True)
    clarity_ranking = ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]
    sns.scatterplot(x="fake_news", y="favorite_count", size='retweet_count',
                    sizes=(10, 15), linewidth=0,
                    data=df, ax=ax)
    plt.show()


def get_true_news(clf, df):
    """
        determines the 'truest' news in a list of tweets

        Parameters
        ----------
        df : pandas.dataframe, contains tweets

        Returns
        -------
        truest_tweet : pandas.series, contains the tweet information which the classifier
                       has determined as the truest

    """
    df = predict_proba_dataframe(clf, df)
    truest_tweet = df[df['true_news'] == max(df['true_news'])]
    return truest_tweet


def get_fake_news(clf, df):
    """
        determines the 'fakest' news in a list of tweets

        Parameters
        ----------
        clf : scikit-learn pipeline, trained classifier

        df : pandas.dataframe, contains tweets

        Returns
        -------
        fakest_tweet : pandas.series, contains the tweet information which the classifier
                       has determined as the most fake

    """
    df = predict_proba_dataframe(clf, df)
    fakest_tweet = df[df['fake_news'] == max(df['fake_news'])]
    return fakest_tweet


def tweet_comparison(tweet_1, tweet_2, count_tweets):
    """
           displays the temporal number of retweets for two tweets

           Parameters
           ----------
           tweet_1 : pandas.series, contains one tweet

           tweet_2 : pandas.series, contains another tweet

       """

    true_id = tweet_1['id'].values[0]
    true_tweet = [get_tweet_from_id(true_id)]

    fake_id = tweet_2['id'].values[0]
    fake_tweet = [get_tweet_from_id(fake_id)]

    rt_true = get_retweets_from_tweet(true_id, count_tweets)
    store_tweets(rt_true, 'true_news')

    rt_fake = get_retweets_from_tweet(fake_id, count_tweets)
    store_tweets(rt_fake, 'fake_news')

    df_r1 = json_to_dataframe(get_file_path_data(tweet_file_name('true_news', '.json')))
    df_r2 = json_to_dataframe(get_file_path_data(tweet_file_name('fake_news', '.json')))

    plt.subplot(2, 2, 1)
    plot_cumulative_retweets(df_r1)
    plt.title('True News')
    plt.subplot(2, 2, 2)
    plot_cumulative_retweets(df_r2)
    plt.title('Fake News')
    plt.subplot(2, 2, 3)
    display_graph(retweeter_graph(true_tweet), true_tweet, 'blue')
    plt.subplot(2, 2, 4)
    display_graph(retweeter_graph(fake_tweet), fake_tweet, 'red')
    plt.show()


if __name__ == '__main__':
    df = json_to_dataframe(PATH_DATA_JSON)
    clf = load_trained_classifier()
    retweets_on_fake_news_scatterplot(predict_proba_dataframe(clf, df))
    tweet_comparison(get_true_news(clf, df), get_fake_news(clf, df))
