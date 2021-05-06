import os
import tweepy
import requests
from requests_oauthlib import OAuth1Session

import time
import json
json_open = open(
    '/home/runner/work/PythonCollections/PythonCollections/python/collection.json', 'r', encoding="utf-8")
collections = json.load(json_open)

# 認証に必要なキーとトークン
API_KEY = os.environ.get("API_KEY")
API_SECRET = os.environ.get("API_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# POST用認証
tw = OAuth1Session(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# キーワードからツイートを取得
api = tweepy.API(auth, wait_on_rate_limit=True)
# tweet
# api.update_status("Hello Tweepy")
information = []
for collection in collections.values():
    for tweet in tweepy.Cursor(api.user_timeline, id=collection["creater"]).items(30):
        information.insert(0, tweet)
        time.sleep(1)
    for tweet in information:
        if (tweet.text[:2] != ['R', 'T']) & (tweet.text[0] != '@') & (tweet.favorite_count > collection["favo"]):
            try:
                img0 = tweet.extended_entities['media'][0]['media_url']
                img1 = tweet.extended_entities['media'][1]['media_url']
                tweet_id = tweet.id
                screen_id = tweet.user.screen_name
                print('-----------------')
                # print(tweet.text)
                # print(img)
                collection_id = "custom-" + collection['collection']
                print("Twitter.com/{}/status/{}".format(screen_id, tweet_id))
                POST_URL = "https://api.twitter.com/1.1/collections/entries/add.json"
                PARAMS = {"tweet_id": tweet_id,
                          "id": collection_id}
                response = tw.post(POST_URL, params=PARAMS)
                print(response.status_code)

            except:
                pass

# for tweet in tweets:
#     print('-----------------')
#     print(tweet.text)
