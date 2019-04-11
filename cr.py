
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


api = tweepy.API(auth,wait_on_rate_limit=True) ##Free API issues, need to wait on rate limit

# Open/Create a file to write data
csvFile = open('data/tweets.csv', 'w', newline='')
#Use csv Writer
csvWriter = csv.writer(csvFile)


tagList = [] #List of Hashtags
currTagList = []
urlList = [] #List of URLs in tweets
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


csvWriter.writerow(["user ID", "Username", "Location", "Date", "Tweet","hashtags","followers","friends"])


for tweet in tweepy.Cursor(api.search,q="#pakistan_Zindabad", lang="en",tweet_mode='extended').items():
    for attrH in tweet.entities["hashtags"]:
    ###    print(attrH['text'])
        tagList.append(attrH['text'].encode("utf-8"))
        currTagList.append(attrH['text'].encode("utf-8"))
    ###for attrU in tweet.entities["urls"]: #URL fetching code
    ###    print(attrU["expanded_url"])
    ###    urlList.append(attrU["expanded_url"])
    #print("ID: ",tweet.user.id," - Screen_name: ",tweet.user.screen_name, " - location: ",tweet.user.location.encode('utf-8') )
    userList.append(tweet.user.id)
    userSNList.append(tweet.user.screen_name)
    userSN_ID[tweet.user.screen_name] = tweet.user.id
    ###print (tweet.entities["hashtags"][0]['text'])
    ###print('\n')
    #print('\n')
    #print (tweet.full_text)
    #print('\n')
    ###print (tweet.entities['urls'])
    ###print('\n\n\n')
    # print("---------------------------------------------------\n",tweet,"\n-----------------------------------------------------------------------\n")
    tweets = tweets+1
    if tweets % 20 == 0:
        print(tweets,'\n')
    csvWriter.writerow([tweet.user.id, tweet.user.screen_name.encode("utf-8"), tweet.user.location.encode("utf-8"), tweet.created_at, tweet.full_text.encode("utf-8"),currTagList,tweet.user.followers_count,tweet.user.friends_count])


    # print('user SN ID-----',userSN_ID)

    # print("---------------------------------------------------\n",
    #
    #     "Tweet-",tweet.full_text.encode('utf-8'),"\n",
    #     "\n Tweet.created_at-",tweet.created_at,"\n",
    #     "Tweet.entities[\'hashtags\']-",currTagList,"\n",
    #     "user.ID-",tweet.user.id,"\n",
    #     "user.screen_name-",tweet.user.screen_name,"\n",
    #     "user.location (use this)-",tweet.user.location,"\n",
    #     "geo-",tweet.geo,"\n",
    #     "coordinates-",tweet.coordinates,"\n",
    #     "place-",tweet.place,"\n",
    #     "user.followers_count-",tweet.user.followers_count,"\n",
    #     "user.friends_count-",tweet.user.friends_count,"\n",
    #
    #     "\n-----------------------------------------------------------------------\n")
    currTagList = []

#friends = tweepy.Cursor(api.followers_ids(userList))
#print("followers -- ", friends)

csvFile.close()


###Code to store Network info
# Open/Create a file to write data
csvFile = open('data/users.csv', 'w', newline='')
#Use csv Writer
csvWriter = csv.writer(csvFile)


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



######## NEW CODE FOR FRIENDSHIP RELATIONSHIP
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

# from itertools import permutations
# for key1, key2 in permutations(userSN_ID.keys(), r = 2):

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



# print("---------------------------------------------------\n",followersList,"\n-----------------------------------------------------------------------\n")

# print(friendList.items())

csvFile.close()



print('\n')
print(Counter(tagList),'\n')
#print(Counter(urlList),'\n')
print('Tweets=',tweets,'\n')




# twData = pd.read_csv('data/ua.csv')
#
# print(twData.head())
