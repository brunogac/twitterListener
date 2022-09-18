import os
from dotenv import load_dotenv
from datetime import datetime
import tweepy
import json

load_dotenv()
#Chaning tweepy class to save data on file
class TweetListener(tweepy.StreamingClient):
    def on_data(self, raw_data):
        out.write(json.dumps(json.loads(raw_data),ensure_ascii=False)+'\n')
        return super().on_data(raw_data)


def erase_all_rules(client):
    """Erase rules (if they exist)"""        
    try:
        for rule in client.get_rules()[0]:
            client.delete_rules(rule.id)
    except:
        pass

def add_rules_from_file(client):
    
    """Load file rules.txt and create rules for the streaming endpoint
    Rules can be created on:
    https://developer.twitter.com/apitools/query
    save each rule on a line on the file rules.txt.
    """
    
    with open('rules.txt','r') as f:
        lines = f.readlines()
        for number, line in enumerate(lines):
            x=client.add_rules(tweepy.StreamRule(value=line,tag=f"rule #{number + 1}",id=str(number+1)))
            if x[3]['summary']['not_created'] == 0:
                print(f'Rule #{number+1} added successfully')
            else:
                print(f'Rule #{number+1}, failed: please verify query syntax')
            
            
if __name__ == '__main__':
    #Load API Key from a .env file
    BearerToken = os.getenv('Bearer_Token')

    #create directory and file to save data
    os.makedirs('data', exist_ok=True)
    now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    out = open(f'data/run_{now}.txt','w',encoding='utf-8')

    #initiating listener
    client =TweetListener(BearerToken)
    
    #deleting possible old rules
    erase_all_rules(client)

    #adding rules from file
    add_rules_from_file(client)

    


    pass