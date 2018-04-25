import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    # Generic class
    def __init__(self):
        # keys and tokens from Twitter
        consumer_key = 'ev8iNTgyxaiqKyldTOfvBkAj3'
        consumer_secret = 'ONGXWVeJEKlrU7AboEjnwgX4QTAFVovZwWnjzgzDtfMfr314DF'
        access_token = '943535993444999169-P800O4ktHPJiMVMjAWRJ6DCuDGY2iii'
        access_token_secret = '8G1r54nE02lCuZB81m5FB8IVXCNATjj4b56kSQrtI9epj'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth)  # fetch tweets from API
        except:
            print ("ERROR:AUTHENTICATION FAILED")

    def clean_tweet(self, tweet):
        # Utility function to clean tweet text by removing links, special characters using regex
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))  # create TextBlob object of passed tweet text
        # sentiment Analysis
        if analysis.sentiment.polarity > 0:
            return 'positive tweet'
        elif analysis.sentiment.polarity == 0:
            return 'neutral tweet'
        else:
            return 'negative tweet'

    def get_tweets(self, query, count=10):
        tweets = []  # empty list
        try:
            # calling twitter api
            fetched_tweets = self.api.search(q=query, count=count)
            # parsing tweets
            for tweet in fetched_tweets:
                parsed_tweet = {}
                # empty dictionary
                parsed_tweet['text'] = tweet.text
                # saving tweets
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                # appending parsed tweet to list
                if tweet.retweet_count > 0:
                    # adding re tweets only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print ("ERROR: " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query='Donald Trump', count=200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} % ".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


if __name__ == '__main__':
    main()
