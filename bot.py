import tweepy #for tweeting
import secrets #twitter keys
import random #randomly generate the next target

usernames = ['___gibson','WonsonSoup','KevGuev7','its_pastable','Dr_Whomstve','sassyderrick', 
             'LauraWhiteley23','zeekay_94','sabah_abbasi','niko_is_a_star']

annoying_message = ['howdy partner!','u up?','beep beep!','honk honk!','welcome to heck buddy',
                    'you\'re my best friend']

def tweep():
  name = random.choice(usernames)
  annoy = random.choice(annoying_message)
  message = annoy + " @" + name
  return message

def tweet(message):
  auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
  auth.set_access_token(secrets.access_token, secrets.access_token_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Currently Tweeting.......")
  api.update_status(status=message)

if __name__ == '__main__':
  tweet(tweep())
