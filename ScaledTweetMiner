import tweepy 
from tqdm.notebook import tqdm
import pandas as pd
import re
import time
pd.set_option('display.max_colwidth', 180)
pd.set_option('display.max_rows', None)
api_key = ""
api_secret = ""
access_key = ""
access_secret = ""
bearer = ""
def search_archive(searchTerms = [], retweets = False, numTweets = 1000, start = None, end = None):
    start_time = time.time()
    team_tweets = []
    s_query = ""
    for item in searchTerms:
        if s_query == "":
            s_query += item + " "
        else: 
            s_query += f"OR {item }"
    query = f'({s_query})'
    if retweets == False:
        query += " -is:retweet "
    query += " lang:en"
    print(f"Search query: {query}")

    
    for i,response in tqdm(enumerate(tweepy.Paginator(client.search_all_tweets, 
                                     query = query,
                                     user_fields = ['username', 'public_metrics', 'location'],
                                     tweet_fields = ['created_at', 'geo', 'public_metrics', 'text'],
                                     expansions = ['author_id'],
                                     start_time = start,
                                     end_time = end,
                                  max_results=500).flatten(numTweets))):
        team_tweets.append(response)
        time.sleep(0.002)
    print(f'{time.time()- start_time} seconds')
    return team_tweets

def clean_tweet(tweet):
    # Remove hashtags, @mentions, URLs, and RTs
    tweet = re.sub(r'#\w+', '', tweet)
    tweet = re.sub(r'@\w+', '', tweet)
    tweet = re.sub(r'https?://\S+', '', tweet)
    tweet = re.sub(r'RT', '', tweet)
    tweet = re.sub(r'\n','', tweet)

    # Strip whitespace and punctuation
    tweet = tweet.strip()
    tweet = re.sub(r'[^\w\s]', '', tweet)

    # Convert to lowercase
    tweet = tweet.lower()

    return tweet

client = tweepy.Client(bearer_token=bearer,wait_on_rate_limit=True)
start="2023-01-22T15:00:00-00:00"
end= "2023-01-22T16:00:00-00:00"
raw_tweets = search_archive(searchTerms= ['Arsenal'],
                            retweets=False, 
                            numTweets=100, 
                            start=start, 
                            end= end )
tweet_texts= [tweet.text for tweet in raw_tweets]
tweet_dates = [tweet.created_at for tweet in raw_tweets]
df = pd.DataFrame(tweet_texts)
df[0] = df[0].apply(clean_tweet)
df['date'] = tweet_dates
df.to_csv("tweetstest.csv")
