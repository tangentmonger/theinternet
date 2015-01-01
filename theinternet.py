import urllib.parse
from secrets import Secrets
import TwitterSearch


def run_search():
    sources = []
    try:
        tso = TwitterSearch.TwitterSearchOrder()
        tso.set_search_url("?%s" % urllib.parse.urlencode({"q":SEARCH_TERM}))
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
    return []

def log_results(parsed_results):
    pass



SEARCH_TERM = '"the internet is a * place"'
NUMBER_OF_TWEETS = 50

search_results = run_search()
parsed_results = parse_results(search_results)
log_results(parsed_results)
