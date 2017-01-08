# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 12:12:35 2017

@author: ADEKUNLE
"""

"""
This code work is to build a database of twitter followers using their api and
then analyzing this data with some ML
Runnig the pipeline of Collection, Analytics, Optimization and Deployment
"""
import twython
import datetime as dt
import os
import sys
import time
import json


#SET AUTHENTICATION
def twython_conn():
    app_key = "NZ0vrTxicorkwhxzCbDjxtvjR"
    app_secret = "OD1YGLqFQ7jwKXXUk2ajzNYZvfeRab2tv3p7am5XkqElHcbmO4"
    oauth_token = "374799441-uoi0jYFAz4lZlvnWIGXrpIuOdWpkhCdIsRUKbJX3"
    oauth_token_secret = "0uy4itf3HEu5AdVkJEw2JSzbp9yS1cds2EaVMKktsVycC"
    t = twython.Twython(app_key= app_key, app_secret=app_secret,\
                        oauth_token=oauth_token,\
                        oauth_token_secret = oauth_token_secret)
    return t

#ToDo: write a line of script to know if the credentials are okay or not
#t.verify_credentials() #returns a json file of the details of the api_key

def tweet_search(api, query, max_tweets, max_id, since_id, geocode):
    ''' Function that takes in a search string 'query', the maximum
        number of tweets 'max_tweets', and the minimum (i.e., starting)
        tweet id. It returns a list of tweepy.models.Status objects. '''

    searched_tweets = []
    while len(searched_tweets) < max_tweets:
        remaining_tweets = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=query, count=remaining_tweets,
                                    since_id=str(since_id),
				                    max_id=str(max_id-1))
#                                    geocode=geocode)
            print('found',len(new_tweets),'tweets')
            if not new_tweets:
                print('no tweets found')
                break
            searched_tweets.extend(new_tweets)
            max_id = new_tweets[-1].id
        except twython.TwythonError:
            print('exception raised, waiting 15 minutes')
            print('(until:', dt.datetime.now()+dt.timedelta(minutes=15), ')')
            time.sleep(15*60)
            break # stop the loop
    return searched_tweets, max_id

def write_tweets(tweets, filename):
    ''' Function that appends tweets to a file. '''

    with open(filename, 'a') as f:
        for tweet in tweets:
            json.dump(tweet._json, f)
            f.write('\n')


def get_tweet_id(api, date='', days_ago=9, query='a'):
    ''' Function that gets the ID of a tweet. This ID can then be
        used as a 'starting point' from which to search. The query is
        required and has been set to a commonly used word by default.
        The variable 'days_ago' has been initialized to the maximum
        amount we are able to search back in time (9).'''

    if date:
        # return an ID from the start of the given day
        td = date + dt.timedelta(days=1)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        tweet = api.search(q=query, count=1, until=tweet_date)
    else:
        # return an ID from __ days ago
        td = dt.datetime.now() - dt.timedelta(days=days_ago)
        tweet_date = '{0}-{1:0>2}-{2:0>2}'.format(td.year, td.month, td.day)
        # get list of up to 10 tweets
        tweet = api.search(q=query, count=10, until=tweet_date)
        print('search limit (start/stop):',tweet.items()[0].created_at)
        # return the id of the first tweet in the list
        return tweet.items()[0].id

def main():
    search_phrases = ['Nigeria', '2016', 'economy', 'youth',
                      'Entrepreneur', 'poverty', 'africa', 
                      'education','sex', 'music', 'entertainment', 'dance',
                      'prayer', 'divorce', 'relationship', 'girlfriend',
                      'boo', 'bae']
    min_days_old, max_days_old = 5, 6
    time_limit = 1.5
    max_tweets = 100
    
    afric_geocode = '6.5480747,3.3975005,10,000km'
    
    for search_phrase in search_phrases:

        print('Search phrase =', search_phrase)

        ''' other variables '''
        name = search_phrase.split()[0] #Removes any white space in search_phrase
        json_file_root = name + '/'  + name #Create root file for each sp
        os.makedirs(os.path.dirname(json_file_root), exist_ok=True)
        #Create a folder each for each search_phrase(sp), exist_ok in makedirs
        #...checks if dir already exist or else make
        read_IDs = False #Ques what read_ids is doing
        
        if max_days_old - min_days_old == 1:
            d = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}'.format(d.year, d.month, d.day)
        else:
            d1 = dt.datetime.now() - dt.timedelta(days=max_days_old-1)
            d2 = dt.datetime.now() - dt.timedelta(days=min_days_old)
            day = '{0}-{1:0>2}-{2:0>2}_to_{3}-{4:0>2}-{5:0>2}'.format(
                  d1.year, d1.month, d1.day, d2.year, d2.month, d2.day)
        json_file = json_file_root + '_' + day + '.json'
        if os.path.isfile(json_file):
            print('Appending tweets to file named: ',json_file)
            read_IDs = True
            
        #Authorize the twython_conn() 
        api = twython_conn()
        
        if read_IDs:
            # open the json file and get the latest tweet ID
            with open(json_file, 'r') as f:
                lines = f.readlines()
                max_id = json.loads(lines[-1])['id']
                print('Searching from the bottom ID in file')
        else:
            # get the ID of a tweet that is min_days_old
            if min_days_old == 0:
                max_id = -1
            else:
                max_id = get_tweet_id(api, days_ago=(min_days_old-1))
        # set the smallest ID to search for
        since_id = get_tweet_id(api, days_ago=(max_days_old-1))
        print('max id (starting point) =', max_id)
        print('since id (ending point) =', since_id)
        
        #Tweets gathering
        start = dt.datetime.now()
        end = start + dt.timedelta(hours=time_limit)
        count, exitcount = 0, 0
        while dt.datetime.now() < end:
            count += 1
            print('count =',count)
            # collect tweets and update max_id
            tweets, max_id = tweet_search(api, search_phrase, max_tweets,
                                          max_id=max_id, since_id=since_id,
                                          geocode=afric_geocode)
            # write tweets to file in JSON format
            if tweets:
                write_tweets(tweets, json_file)
                exitcount = 0
            else:
                exitcount += 1
                if exitcount == 3:
                    if search_phrase == search_phrases[-1]:
                        sys.exit('Maximum number of empty tweet strings reached - exiting')
                    else:
                        print('Maximum number of empty tweet strings reached - breaking')
                        break


if __name__ == "__main__":
    main()