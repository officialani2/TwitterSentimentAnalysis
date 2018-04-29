import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from tkinter import *
import pandas as pd
import numpy as np
from tabulate import tabulate

# created by: ANIRUDDH SHUKLA 

root = Tk()


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'In8jQppCfuSmqjzhR4PdbVNUy'
        consumer_secret = 'g1qAUMffDWnjrn3UZMr2pxFARgpGTtVXI2Z0VOatRw0P3rOzKP'
        access_token = '943535993444999169-P800O4ktHPJiMVMjAWRJ6DCuDGY2iii'
        access_token_secret = '8G1r54nE02lCuZB81m5FB8IVXCNATjj4b56kSQrtI9epj'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main(string123):
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    # string123 = input("Enter your query:\n")
    tweets = api.get_tweets(string123, count=200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {0:.2f} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {0:.2f} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets percentage: {0:.2f} % ".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:500]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:500]:
        print(tweet['text'])


root.title("Twitter Analysis")
root.geometry("400x400")
title = Label(root, text="Welcome to Twitter Analysis", font=("Times New Roman", 20))
title.pack()
label = Label(root, text="Enter your query:")
label.place(x=20, y=50)
# label.pack(side=LEFT)
name = StringVar()
field = Entry(root, textvariable=name)
field.place(x=135, y=50)
# field.pack(side=LEFT)


def call():
    main(str(name.get()))


submitButton = Button(root, text="Submit", command=call)
# submitButton.pack(side=LEFT)
submitButton.place(x=310, y=45)
root.mainloop()
