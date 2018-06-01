from twitter_credentials_mine import credentials
import tweepy
from pymongo import MongoClient
import json
from tweepy import Stream
from tweepy.streaming import StreamListener

auth = tweepy.OAuthHandler(credentials['TWITTER_CONSUMER_KEY'],
                           credentials["TWITTER_CONSUMER_KEY_SECRET"])
auth.set_access_token(credentials["TWITTER_ACCESS_TOKEN"],
                      credentials["TWITTER_ACCESS_TOKEN_SECRET"])

api=tweepy.API(auth)

client = MongoClient()
db = client.project4   #creates a new database
royaltweets_collection = db.royaltweets   #creates a new collection

class MyListener(StreamListener):
        
    def on_data(self, data):
        tweet_json = json.loads(data)

        try:
            the_text = tweet_json['extended_tweet']['full_text']
        except KeyError:
        	if 'text' not in tweet_json:
        		return
        	the_text = tweet_json['text']
        
        if (len(the_text) > 4) and (the_text[:4] == 'RT @'):
            return
        
        try:
            tweet = {
                'full_text5': the_text,
                'screen_name': tweet_json['user']['screen_name'],
                'location': tweet_json['user']['location'],
                'created_at':tweet_json['created_at'],
                'retweet_count': tweet_json['retweet_count'],
                'source': tweet_json['source'],
                'favorite_count': tweet_json['favorite_count']
            }
        except:
            print(tweet_json.keys())
            print('error')
            return

        db.royaltweets.insert_one(tweet)

twitter_stream = Stream(auth, MyListener(), tweet_mode='extended')
twitter_stream.filter(track=['#royalwedding', '#royalwedding2018','#meghanmarkle','#princeharry','#princeharryandmeghan','#windsor','#windsorcastle',
                            '#theroyalfamily','#thequeenofengland','#thequeen','#royalfamily','#kensingtonpalace','#harryandmeghan','#harryandmeganroyalromance',
                            '#weddingoftheyear', '#royalweddingcake', '#meganmarkle'])
