from dotenv import load_dotenv
import os
import tweepy  
import time

load_dotenv()  

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# First we setup the auth object.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Then we get the tweepy APi to authentivcate.
api = tweepy.API(auth)

# Helper function to handle the twitter rate limit.
def handle_limit(cursor):
  try:
    while True:
      yield cursor.next()
  except tweepy.RateLimitError:
    time.sleep(1000)

# Print Followers
for follower in handle_limit(tweepy.Cursor(api.followers).items()):
  print(follower.name)

search = "python"
num_of_tweets = 100

# Favorite and comment.
for tweet in handle_limit(tweepy.Cursor(api.search, search).items(num_of_tweets)):
  try:
    tweet.favorite()
    print("I like this tweet!")
  except tweepy.TweepError as e:
    print(e.reason)
  except StopIteration:
    break