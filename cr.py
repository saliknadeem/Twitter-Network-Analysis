
import config ##custom config file to load API Keys

import tweepy
import csv
import itertools
import pandas as pd
import numpy as np

from collections import Counter
from collections import defaultdict


##input your credentials here
consumer_key = config.consumer_key
consumer_secret = config.consumer_secret
access_token = config.access_token
access_token_secret = config.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)


api = tweepy.API(auth,wait_on_rate_limit=True)

# Open/Create a file to append data
csvFile = open('data/ua.csv', 'w', newline='')
#Use csv Writer
csvWriter = csv.writer(csvFile)

tagList = []
urlList = []
userList = []
userSNList = []
tweets = 0
index=1


def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page









csvWriter.writerow(["user ID", "Username", "Location", "Date", "Tweet"])


for tweet in tweepy.Cursor(api.search,q="#Pakista", lang="en",tweet_mode='extended').items():
    for attrH in tweet.entities["hashtags"]:
    ###    print(attrH['text'])
        tagList.append(attrH['text'])
    ###for attrU in tweet.entities["urls"]: #URL fetching code
	###    print(attrU["expanded_url"])
    ###    urlList.append(attrU["expanded_url"])
    #print("ID: ",tweet.user.id," - Screen_name: ",tweet.user.screen_name, " - location: ",tweet.user.location.encode('utf-8') )
    userList.append(tweet.user.id)
    userSNList.append(tweet.user.screen_name)
    ###print (tweet.entities["hashtags"][0]['text'])
    ###print('\n')
    #print('\n')
    #print (tweet.full_text)
    #print('\n')
    ###print (tweet.entities['urls'])
    ###print('\n\n\n')
    tweets = tweets+1
    if tweets % 50 == 0:
        print(tweets,'\n')
    csvWriter.writerow([tweet.user.id, tweet.user.screen_name, tweet.user.location.encode('utf-8'), tweet.created_at, tweet.full_text.encode('utf-8')])
    index = index+1

#friends = tweepy.Cursor(api.followers_ids(userList))
#print("followers -- ", friends)



friendList = defaultdict(list)

print("user list----",len(userSNList))
print('Starting getting Friends Lists')
for user in userSNList:
    followers = api.followers_ids(screen_name=user)
    print('Starting pagination')
    for page in paginate(followers, 100):
        results = api.lookup_users(user_ids=page)
        friendList[user].append(page)
        #print('\n\nuser: ', user ,'---- friends=',page)
        ##for result in results:
        ##    print ("friend - ",result.screen_name, "user - ",user)
		
print("---------------------------------------------------\n",friendList,"\n-----------------------------------------------------------------------\n")
	

print('\n\n\n')
print(Counter(tagList),'\n')
#print(Counter(urlList),'\n')
print('Tweets=',tweets,'\n')



csvFile.close()


twData = pd.read_csv('data/ua.csv')

print(twData.head())



