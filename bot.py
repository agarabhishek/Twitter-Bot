import tweepy
from secrets import *
import json
import datetime

max_tweets = 1000
counterForReplies = 0
reply = '''Hey! I liked your tweet'''

# create an OAuthHandler instance
# Twitter requires all requests to use OAuth for authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 

auth.set_access_token(access_token, access_secret)

#Construct the API instance
api = tweepy.API(auth,wait_on_rate_limit=True) 

data= {}
dateToday = str(datetime.datetime.now().date())

with open('data.txt','r') as json_file: 
    tweets = json.load(json_file)

with open('data.txt','w') as json_file:
    concernedTweets = [status for status in tweepy.Cursor(api.search, q='Star Wars').items(max_tweets)] 
    # print(concernedTweets)
    numberOfTweets = len(concernedTweets)
    print('Today\'s number of tweets are '+str(numberOfTweets))
    data =  []
    for i in concernedTweets:
        data.append({  
        'tweetID': i._json['id_str'],
        'screen_name': i._json['user']['screen_name']
        })
    tweets['tweets'][dateToday] = data
    json.dump(tweets,json_file)

with open('data.txt','r') as json_file:
    tweets = json.load(json_file)
    for tweet in tweets['tweets'][dateToday]:
#        if tweet['screen_name'] == 'reach4abhishek':
        print("Here")
        api.update_status("@"+tweet['screen_name']+" "+reply,in_reply_to_status_id = tweet['tweetID'])
        counterForReplies = counterForReplies + 1
        print(counterForReplies, ' - Reply posted to',tweet['tweetID'])