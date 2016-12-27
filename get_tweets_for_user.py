import tweepy
from tweepy import OAuthHandler
import os
import json

consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
# consumer_key, consumer_secret
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']
# access_secret, access_token

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

def print_tweet_text(tweet):
    print(tweet.text)

def process(tweet, filename=None):
    if filename:
        try:
            with open(filename, 'a') as f:
                f.write(json.dumps(tweet._json) + '\n')
        except BaseException as e:
            print("Error on_data: {}".format(str(e)))
    else:
        print_tweet_text(tweet)

def process_user_tweets(user_id, n=50, filename=None):
    for tweet in tweepy.Cursor(api.user_timeline, id=user_id).items(n):
        process(tweet, filename)


def read_stored_tweets(filename):
    tweets = (json.loads(i) for i in open(filename).read().split('\n') if i)
    return tweets

def process_stored_tweets_texts(read_filename, write_filename=None):
    tweets = read_stored_tweets(read_filename)
    
    for tweet in tweets:
        # print(tweet)
        if write_filename:
            try:
                with open(write_filename, 'a') as f:
                    f.write(tweet['text'] + '\n\n')
            except:
                print("Error on_data: {}".format(str(e)))
        else:
            print(tweet['text'])

def get_users_tweets_count(user_id):
    return api.get_user(id=user_id)._json['statuses_count']

def save_all_user_tweets(user_id):
    n = get_users_tweets_count(user_id)

    process_user_tweets(user_id, n, filename='user_{}.json'.format(user_id))
    process_stored_tweets_texts(read_filename='user_{}.json'.format(user_id),
                                write_filename='user_{}_texts.txt'.format(user_id))
