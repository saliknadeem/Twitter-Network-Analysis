
import config ##custom config file to load API Keys

import tweepy
import csv
import pandas as pd

from collections import Counter


##input your credentials here
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
# Open/Create a file to append data
csvFile = open('data/ua.csv', 'w', newline='')
#Use csv Writer
csvWriter = csv.writer(csvFile)

tagList = []
urlList = []
userList = []
tweets = 0
index=1

csvWriter.writerow(["user ID", "Username", "Location", "Date", "tweet"])


for tweet in tweepy.Cursor(api.search,q="#Paki", lang="en",tweet_mode='extended').items():
    for attrH in tweet.entities["hashtags"]:
    #    print(attrH['text'])
        tagList.append(attrH['text'])
    #for attrU in tweet.entities["urls"]: #URL fetching code
	#    print(attrU["expanded_url"])
    #    urlList.append(attrU["expanded_url"])
    print("ID: ",tweet.user.id," - Screen_name: ",tweet.user.screen_name, " - location: ",tweet.user.location.encode('utf-8') )
    #    userList.append(attrUsr)

    #print (tweet.entities["hashtags"][0]['text'])
    #print('\n')
    print('\n')
    print (tweet.full_text)
    print('\n')
    #print (tweet.entities['urls'])
    #print('\n\n\n')
    tweets = tweets+1
    if tweets % 50 == 0:
        print(tweets,'\n')
    csvWriter.writerow([tweet.user.id, tweet.user.screen_name, tweet.user.location.encode('utf-8'), tweet.created_at, tweet.full_text.encode('utf-8')])
    index = index+1

print('\n\n\n')
print(Counter(tagList),'\n')
#print(Counter(urlList),'\n')
print('Tweets=',tweets,'\n')



csvFile.close()


twData = pd.read_csv('data/ua.csv')

print(twData.head())



