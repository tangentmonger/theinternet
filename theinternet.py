import re
import json
import requests
import urllib.parse
from secrets import Secrets
import TwitterSearch

def run_search():
    sources = []
    try:
        tso = TwitterSearch.TwitterSearchOrder()
        tso.set_search_url("?%s" % urllib.parse.urlencode({"q":"\"%s\"" % SEARCH_TERM}))
        tso.set_locale('en')
        tso.set_count(NUMBER_OF_TWEETS) #smallest request that might work
        tso.set_include_entities(False)
        
        twitter_search = TwitterSearch.TwitterSearch(
            consumer_key = Secrets.consumer_key,
            consumer_secret = Secrets.consumer_secret,
            access_token = Secrets.access_token,
            access_token_secret = Secrets.access_token_secret
            )

        tweets = twitter_search.search_tweets(tso)
        retries = 0
        
        while len(sources) < NUMBER_OF_TWEETS and retries < 5:
            for tweet in tweets['content']['statuses']:
                sources.append(tweet['text'])

        tweets = twitter_search.search_next_results()
        retries += 1

    except TwitterSearch.TwitterSearchException as exception:
        print(exception)

    return sources

def parse_results(search_results):

    regex = re.sub('\*', '([\\w\'\\-]+)', SEARCH_TERM)
    result = []
    for source in search_results:
        match = re.search(regex, source, re.IGNORECASE)
        if match:
            result.append(match.groups()[0].lower())
            #assumption: there was exactly one match
    return result

def get_sentiments(parsed_results):
    print(parsed_results)
    sentiments = []
    for word in parsed_results:
        params = {'text': word}
        response = requests.post('http://text-processing.com/api/sentiment/', data={'text':word})
        result = response.json()['probability']

        if result['pos'] > result['neg']:
            sentiments.append(result['pos'])
        else:
            sentiments.append(result['neg'] * -1)

    average = float(sum(sentiments)/len(sentiments))
    print(average)





SEARCH_TERM = 'the internet is a * place'
NUMBER_OF_TWEETS = 15

search_results = run_search()
parsed_results = parse_results(search_results)
sentiments = get_sentiments(parsed_results)
