import tweepy 
from textblob import TextBlob 
import numpy as np 
import matplotlib.pyplot as plt 
%matplotlib inline
plt.ion()
import copy
import pandas as pd
import re
import time

api_key = ""
api_secret = ""
bearer = ""
access_key = ""
access_secret = ""

authenticator = tweepy.OAuthHandler(api_key,api_secret)
authenticator.set_access_token(access_key,access_secret)
api = tweepy.API(authenticator,wait_on_rate_limit=True)

team1 = "USA"
team2 = "England"


team1_Player1 = "Wright"
team1_Player2 = "Weah"
team1_Player3 = "Pulisic"
team1_Player4 = "Musah"
team1_Player5 = "Adams"
team1_Player6 = "McKennie"
team1_Player7 = "Robinson"
team1_Player8 = "Ream"
team1_Player9 = "Zimmerman"
team1_Player10 = "Dest"
team1_Player11 = "Turner"


team2_Player1 = "Trippier"
team2_Player2 = "Stones"
team2_Player3 = "Maguire"
team2_Player4 = "Shaw"
team2_Player5 = "Bellingham"
team2_Player6 = "Rice"
team2_Player7 = "Sterling"
team2_Player8 = "Mount"
team2_Player9 = "Saka"
team2_Player10 = "Kane"
team2_Player11 = "Pickford"

#6000*22 tweets - or around 120k
number_of_tweets = 6000 


date_since = "2022-11-25"
date_until = "2022-11-26"


americaArray = [team1_Player1, team1_Player2, team1_Player3, team1_Player4, team1_Player5, team1_Player6, team1_Player7,
team1_Player8, team1_Player9, team1_Player10, team1_Player11] # player array for Team 1

englandArray = [team2_Player1, team2_Player2, team2_Player3, team2_Player4, team2_Player5, team2_Player6, team2_Player7,
team2_Player8, team2_Player9, team2_Player10, team2_Player11] # player array for Team 2

def team_sentiment(team, teamArray, numberOfTweets, dateUntil):
    """
    team - string of team
    teamArray - string of player names
    numberOfTweets - int of number of tweets per player to analyze
    dateUntil - day of game
    """
    player_sentiments = {}
    sentiment_distribution = {}
    for player in teamArray:
        start = time.time()
        print("Working on {}...".format(player))
        search = [f'{player} -filter:retweets',f'{team} -filter:retweets']
        tweet_cursor = tweepy.Cursor(api.search_tweets, until = dateUntil,q = search, lang = "en",tweet_mode = "extended").items(numberOfTweets)
        tweetList = [tweet.full_text for tweet in tweet_cursor]
        df = pd.DataFrame(tweetList, columns = ["tweets"])
        for _,row in df.iterrows():
            row['tweets'] = re.sub('http\S+', '', row['tweets'])
            row['tweets'] = re.sub('#\S+', '', row['tweets'])
            row['tweets'] = re.sub('@\S+', '', row['tweets'])
            row['tweets'] = re.sub('\\n', '', row['tweets'])
        df['Polarity'] = df['tweets'].map(lambda tweet: TextBlob(tweet).sentiment.polarity)
        sentiment_distribution[player] = df['Polarity'].tolist()
        total_polarity = 0
        count =0
        for index, row in df.iterrows():
            if row[1] != 0:
                total_polarity+= row[1]
                count+=1
        player_sentiments[player] = total_polarity/count
        end = time.time()
        print(str(end-start) + " seconds")
    return player_sentiments, sentiment_distribution
        
        
        
        
USA_sentiment, USA_sentiment_distribution = team_sentiment("USA", americaArray,6000,date_until )
england_sentiment, england_sentiment_distribution = team_sentiment("England", englandArray,6000,date_until )
  
plt.figure(figsize = (12,8))
plt.bar(USA_sentiment.keys(),USA_sentiment.values())
plt.title("USA Twitter Sentiment")
plt.xlabel("Player")
plt.ylabel("Sentiment Score")
for value, index in enumerate(y):
    plt.text(value, index,
             str(index)[:4])


plt.figure(figsize = (12,8))
x = list(USA_sentiment.keys())
y = list(USA_sentiment.values())
plt.barh(x, y)
for index, value in enumerate(y):
    plt.text(value, index,
             str(value)[:5])
plt.title("USA Twitter Sentiment")
plt.ylabel("Player")
plt.xlabel("Sentiment Score")


plt.figure(figsize = (12,8))
x = list(england_sentiment.keys())
y = list(england_sentiment.values())
plt.barh(x, y)
for index, value in enumerate(y):
    plt.text(value, index,
             str(value)[:5])
plt.title("England Twitter Sentiment")
plt.ylabel("Player")
plt.xlabel("Sentiment Score")


for player in USA_sentiment_distribution:
    plt.hist(USA_sentiment_distribution[player], label = player )
    plt.legend()
    plt.show()
    
for player in england_sentiment_distribution:
    plt.hist(england_sentiment_distribution[player], label = player )
    plt.legend()
    plt.show()

