
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


searchTweet = "#ONBudget"
getUserData = 0



api = tweepy.API(auth,wait_on_rate_limit=True) ##Free API issues, need to wait on rate limit

# Open/Create a file to write data
csvFile = open('data/'+searchTweet+'_tweets.csv', 'w', newline='',encoding='utf8')
#Use csv Writer
csvWriter = csv.writer(csvFile)


tagList = [] #List of Hashtags
currTagList = []
urlList = [] #List of URLs in tweets
currurlList = [] #List of URLs in tweets
userList = [] #List of user IDs with matching tweets
userSNList = [] #List of user Screen_names with matching tweets
tweets = 0 # Tweet Counter

userSN_ID = {} #Dict for storying user Screen Names with IDs

def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page


csvWriter.writerow(["user ID", "Username", "Location", "Date", "Tweet","ReTweeted","hashtags","URLs","followers","friends"])

rtCheck = 0
for tweet in tweepy.Cursor(api.search,q=searchTweet, lang="en",tweet_mode='extended').items():
    for attrH in tweet.entities["hashtags"]:
    ###    print(attrH['text'])
        tagList.append(attrH['text'].encode("utf-8"))
        currTagList.append(attrH['text'].encode("utf-8"))
    for attrU in tweet.entities["urls"]: #URL fetching code
       urlList.append(attrU["expanded_url"])
       currurlList.append(attrU["expanded_url"])
    userList.append(tweet.user.id)
    userSNList.append(tweet.user.screen_name)
    userSN_ID[tweet.user.screen_name] = tweet.user.id
    if tweet.full_text.startswith('RT @'):
        rtCheck = 1
    else:
        rtCheck = 0

    # print("---------------------------------------------------\n",tweet.full_text,"\n-----------------------------------------------------------------------\n")
    tweets = tweets+1
    if tweets % 20 == 0:
        print("Tweets searched = ",tweets,'\n')
    csvWriter.writerow([tweet.user.id, tweet.user.screen_name, tweet.user.location, tweet.created_at, tweet.full_text,rtCheck, currTagList,currurlList,tweet.user.followers_count,tweet.user.friends_count])
    currTagList = []

print("Total Tweets = ", tweets)

csvFile.close()


###Code to store Network info
# Open/Create a file to write data





if (getUserData):
    csvFile = open('data/'+searchTweet+'_users.csv', 'w', newline='')
    #Use csv Writer
    csvWriter = csv.writer(csvFile)

    iter=0
    print("total unique people = ",len(userSN_ID.keys()))
    from itertools import combinations
    for key1, key2 in combinations(userSN_ID.keys(), r = 2):

        # print(key1,key2)
        link = api.show_friendship(source_screen_name=key1, target_screen_name=key2)
        # print(link[0].following,link[0].followed_by)
        if (link[0].followed_by):
            print(key1,"->",key2)
            csvWriter.writerow([key1.encode('utf-8'),key2.encode('utf-8')])
        if (link[1].followed_by):
            print(key2,"->",key1)
            csvWriter.writerow([key2.encode('utf-8'),key1.encode('utf-8')])
        iter = iter+1
        if iter % 20 == 0:
            print("Friends searched = ",iter)

    # print("---------------------------------------------------\n",followersList,"\n-----------------------------------------------------------------------\n")
    csvFile.close()


###### Old bad code
##friendList = defaultdict(list) # List of friends of the Users who Tweeted
## print("user list----",len(userSNList))
## print('Starting getting Friends Lists')
## for user in userSNList:
##     followers = api.followers_ids(screen_name=user)
##     print('Starting pagination')
##     for page in paginate(followers, 100):
##         results = api.lookup_users(user_ids=page)
##         for friend in page:
##         # print('page-----------------',page)
##             friendList.setdefault(user,[]).append(friend)
##             csvWriter.writerow([user.encode('utf-8'),userSN_ID[user],friend])
##         #print('\n\nuser: ', user ,'---- friends=',page)
##         ##for result in results:
##         ##    print ("friend - ",result.screen_name, "user - ",user)

## for k, v in Counter(friendList).items():
##     print(k, len(v))

###### CURRENT CODE for finding friends list of users
# counter=0
# followersList = []
# for sn,id in userSN_ID.items():
#     print('for loop user\n')
#     for follower in tweepy.Cursor(api.followers, user_id=id).items():
#         counter=counter+1
#         followersList.append([id,follower.screen_name,follower.id])
#         csvWriter.writerow([sn.encode('utf-8'),id,follower.screen_name.encode('utf-8'),follower.id])
#         print([sn,id,follower.screen_name.encode('utf-8'),follower.id])
#     print("counter---",counter)



print('\n')
print(Counter(tagList),'\n')
# print(Counter(urlList),'\n')




# twData = pd.read_csv('data/ua.csv')
#
# print(twData.head())
