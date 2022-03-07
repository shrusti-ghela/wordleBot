#getTweets.py

"""
Created on Sat Mar  5 13:43:59 2022
Name: Twitter Data for Wordle
Description: Setting up dataset of tweets on Wordle
"""
import tweepy 
import pytz
from datetime import datetime
import pandas as pd
import re

from twitterKeys import twitterKeys

class getTweets:
    
    def twitterAuth():
        '''
        This function provides keys for Twitter API authentication.

        '''
        keys = twitterKeys()
        twitter_api_key = keys.get_keys("twitter_api_key")
        twitter_api_secret = keys.get_keys("twitter_api_secret")
        auth = tweepy.AppAuthHandler(twitter_api_key, twitter_api_secret)
        api = tweepy.API(auth)
        return(api)

    def getWordleID():
        '''
        This function gets the Wordle-ID for the day.

        '''
        wordle_start = pytz.timezone("US/Pacific").localize(datetime(2021, 6, 19))
        now = pytz.utc.localize(datetime.now()).astimezone(pytz.timezone("US/Pacific"))
    
        wordle_id = (now-wordle_start).days
        print("Today's wordle_id is: %d (%s)" % (wordle_id, now.strftime("%Y-%m-%d %H:%M PT")))
        return(wordle_id)
    

    def is_valid_wordle_tweet(tweet, wordle_id): 
        '''
        This function checks matches wordle ID for the given day and ensures that the tweet text  is clean.

        Parameters
        ----------
        tweet : string
            The tweet text value extracted from Twitter data.
        wordle_id : string
            Thw wordle ID for the give day.

        Returns
        -------
        bool
            True if the tweet text looks valid, else False.

        '''
        text = (tweet.replace("Y", "y").replace("🟩", "Y")
                     .replace("M", "m").replace("🟨", "M")
                     .replace("N", "n").replace("⬛", "N").replace("⬜", "N"))
        for i in range(wordle_id-20, wordle_id+20):
            if i==wordle_id:
                continue
            if str(i) in text:
                return False
        
        if len(re.findall("Wordle %d" % wordle_id, text)) != 1:
            return False
    
        if re.match("Wordle %d [2-6]/6\n\n[YMN]{5}\n" % wordle_id, text) is None:
            return False
        return True

    def pullTweets(self,api,wordle_id):
        '''
        This function pulls 5000 tweets from twitter for the given Wordle ID.

        '''
        wordle_tweets = []
        cursor = tweepy.Cursor(api.search_tweets, q="wordle %d" % wordle_id)
        tweets = list(cursor.items(5000))
        for tweet in tweets:
            wordle_tweets.append((wordle_id, tweet.text))
        
        print("Pulled %d tweets for wordle %d" % (len(wordle_tweets), wordle_id))
    
        tweets_df = pd.DataFrame([tweet for tweet in wordle_tweets if self.is_valid_wordle_tweet(tweet[1], tweet[0])],
                                     columns=["wordle_id", "tweet_text"])
        tweets_df.to_csv("./data/tweets.csv")
        
    if __name__ == "__main__":
        api = twitterAuth()
        wordle_id = getWordleID()
        pullTweets(api, wordle_id)
        
        

