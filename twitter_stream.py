#tutorial: http://adilmoujahid.com/posts/2014/07/twitter-analytics/
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twilio.rest import TwilioRestClient #For sending texts
from twilio.rest.exceptions import *
from uuid import uuid4
import json
import logging


#Variables that contains the user credentials to access Twitter API 

# Translation from user id: followArray = ['Rebel_zs', 'realDonaldTrump'] , '25073877'

followArray = ['812134730405650432', '25073877', '174454316']
#trackArray filters out responses from Twitter server -- can only filter out terms, not op
trackArray  = []

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    #we need to parse these from the config file
    def __init__(self, twilio_user_config, twitter_api_config):
        #makes a new unique file for every run
        self.outfile = 'results/result.'+str(uuid4())+'.json'
        self.twilio_user = TwilioUser(parse_json_file('twilio_user_config.json'))
        self.api_config  = TwitterAPIConfig(parse_json_file('twitter_api_cred.json'))
        
    def on_data(self, data):
        for t in data:
            try:
                tweet = json.loads(data)
                userId = str(tweet['user']['id'])
            
                if userId in followArray:
                    print tweet
                    #write resulting tweet to a file for analysis
                    with open(self.outfile, 'a') as f:
                        json.dump(tweet, f)
                        f.write("\n\n")
                    #Send an alert    
                    self.sendTextAlert()
                    return True
            except ValueError:
                print 'error in processing tweet: valueError'
                pass
            except KeyError:
                print 'Got a keyError, continuing...'
                pass
        
    def on_error(self, status):
        print status
        
    def sendTextAlert(self):
        try:
            #client = TwilioRestClient('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')
            client = TwilioRestClient(self.api_config.account_sid,
                                      self.api_config.account_auth_token)
 
            client.messages.create(from_=self.twilio_user._from,
                                   to=self.twilio_user.to,
                                   body=self.twilio_user.body)
        except ValueError:
             print 'error in sending text: Value Error'

        except TwilioRestException as e:
            print 'Twilio Error', e


class TwilioUser(object):
    def __init__(self, json_data):
       self._from = json_data['from']
       self.to = json_data['to']
       self.body = json_data['body']

class TwitterAPIConfig(object):
    def __init__(self, json_data):
        self.account_sid = json_data['account_sid']
        self.account_auth_token = json_data['account_auth_token']
 
class AuthConfig(object):
    def __init__(self, json_data):
        self.access_token = json_data['access_token']
        self.access_token_secret = json_data['access_token_secret']
        self.consumer_key = json_data['consumer_key']
        self.consumer_secret = json_data['consumer_secret']
        
#returns a json object
def parse_json_file(filename):
    with open(filename, 'r') as d:
        data = json.loads(d.read())
    return data


if __name__ == '__main__':

    auth_obj = AuthConfig(parse_json_file('auth.json'))
    
    #This handles Twitter authentication and the connection to Twitter Streaming API
    listener = StdOutListener('twilio_user_config.json', 'twitter_api_cred.json')

    #want to open a pipe for this and for one that serves changes to the file or pipes to standard out
    auth = OAuthHandler(auth_obj.consumer_key, auth_obj.consumer_secret)
    auth.set_access_token(auth_obj.access_token, auth_obj.access_token_secret)
    
    stream = Stream(auth, listener)
    
    #'async = True' as an arg to stream.filter sets the stream to run on a separate thread from the program -- otherwise the stream will consume the entire thread the prog runs on
    #This line filter Twitter Streams to capture data from specific users
    while True:
        try:
            stream.filter(track=trackArray, follow=followArray)
        #catch all exceptions in stream and reconnect
        except Exception: 
            logging.exception('stream filter')
            time.sleep(10)
            continue

