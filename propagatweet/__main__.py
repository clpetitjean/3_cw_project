
from propagatweet.twitter_collection.tweet_collection import *
import propagatweet.tweet_analysis.classification as classification
from propagatweet.twitter_connect import tweet_storage
from propagatweet.tweet_analysis import tweet_credibility
from propagatweet.visualization import tweet_comparison
from propagatweet.utils import conversion, path_management


def print_choice_msg(choices, msg):
    print(msg)
    for (k, v) in choices.items():
        print('\t{} \t-\tEnter {}'.format(v, k))


def get_yes_no(msg):
    choices = {'y': 'Yes', 'n': 'No'}

    choice = ""
    while not ('y' in choice or 'n' in choice):
        print_choice_msg(choices, msg)
        choice = input().lower()
    if 'y' in choice:
        return 1
    else:
        return 0


def get_int(msg):
    print(msg)
    print("Enter an integer")
    n = input()
    while not n.isnumeric():
        print("Enter an integer")
        n = input()
    return int(n)


def get_choice_type_request():
    choices = {
        1: 'Keyword',
        2: 'Username',
        3: 'Hashtag'
    }

    msg = 'Choose the type of tweets to search on Twitter\nSearch by :'

    print_choice_msg(choices, msg)

    choice = input()
    print(choice)
    while (not choice.isnumeric()) or int(choice) not in choices.keys():
        print('Incorrect input')
        print_choice_msg(choices, msg)
        choice = input()

    choice = int(choice)
    print('Search by {}'.format(choices[choice]))
    return choice


def get_str_input(msg):
    txt = ""
    while len(txt) == 0:
        print('Enter the searched {}'.format(msg))
        txt = input().strip()
    return txt


def get_username():
    msg = 'username'
    username = get_str_input(msg).replace('@', '')
    while len(username.split()) > 1:
        print('Invalid username')
        username = get_str_input(msg).replace('@', '')
    return username


def get_hashtag():
    msg = 'hashtag'
    hashtag = get_str_input(msg)
    while len(hashtag.split()) > 1:
        print('Invalid hashtag')
        hashtag = get_str_input(msg)
    if hashtag[0] != '#':
        hashtag = '#' + hashtag
    return hashtag


def get_keywords():
    msg = 'keyword'
    keyword = ' '.join(get_str_input(msg).split())
    return keyword


def get_query(choice):
    if choice == 1:
        # keywords
        query = get_keywords()
    elif choice == 2:
        # username
        query = get_username()
    else:
        # hashtag
        query = get_hashtag()
    return query


def get_requested_tweets(choice, query, count_tweets=50):
    tweets = []
    if choice == 1:
        # keywords
        tweets = get_tweet_from_keyword(keyword=query, count_tweets=count_tweets)
    elif choice == 2:
        # username
        tweets = get_tweet_from_user(screen_name=query, count_tweets=count_tweets)
    else:
        # hashtag
        tweets = get_tweet_from_hashtag(hashtag=query, count_tweets=count_tweets)
    return tweets


def main():
    choice = get_choice_type_request()
    query = get_query(choice)
    count_tweets = get_int('Enter the number of tweets')
    tweets = get_requested_tweets(choice, query, count_tweets)

    tweet_storage.store_tweets(tweets, query)
    filename = tweet_storage.tweet_file_name(query, '.json')

    path = path_management.get_file_path_data(filename)
    df = conversion.json_to_dataframe(path)
    clf = classification.load_trained_classifier()

    df = tweet_credibility.predict_proba_dataframe(clf, df)

    # Affichage de des retweets/like en fonction de la crédibilité
    print('Creating the plot...')
    tweet_comparison.retweets_on_fake_news_scatterplot(df)

    true = tweet_comparison.get_true_news(clf, df)
    fake = tweet_comparison.get_fake_news(clf, df)

    true_text = true['full_text'].values[0]
    true_prob = true['true_news'].values[0]

    fake_text = fake['full_text'].values[0]
    fake_prob = fake['fake_news'].values[0]


    print("Predicted Truest Tweet")
    print(true_text)
    print('Probability that it is a true news : {}\n'.format(true_prob))

    print("Predicted Fakest Tweet")
    print(fake_text)
    print('Probability that it is a fake news : {}\n'.format(fake_prob))

    print('Creating the graph...')
    tweet_comparison.tweet_comparison(true, fake, count_tweets)

    return None


if __name__ == '__main__':
    main()
