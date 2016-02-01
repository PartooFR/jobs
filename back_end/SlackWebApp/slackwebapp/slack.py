from slacker import Slacker, Error as Sl_Error
from datetime import datetime
CONNECTION_OK = 0
CONNECTION_ERROR = 1
CHANNEL_ERROR = 2

base_token = 'xoxp-19294308839-19294044322-19401435232-79ca3b42fa'

def is_valid_token(token):
    sl = Slacker(token)
    try:
        sl.auth.test()
    except Sl_Error as e:
        return e
    return CONNECTION_OK

class SlackAPI:
    
    def __init__(self, token=base_token):
        self.slack = Slacker(token)

        # Dict of existing channels {'name': 'id'}
        self.channels_ids = {}

        # Dict of existing users {'id': 'name'}
        self.users_names = {}

        self.get_channels()
        self.get_users()

    def get_channels(self):
        # Fill self.channels_ids with all existing channels
        #   return CONNECTION_ERROR if can't connect to slack API
        slack_list = self.slack.channels.list()

        if not slack_list.body['ok']:
            return CONNECTION_ERROR

        for chan in slack_list.body['channels']:
            self.channels_ids[chan['name']] = chan['id']
        return CONNECTION_OK
        
    def get_users(self):
        # Fill self.users_ids with all existing users
        #   return CONNECTION_ERROR if can't connect to slack API
        slack_list = self.slack.users.list()

        if not slack_list.body['ok']:
            return CONNECTION_ERROR

        for user in slack_list.body['members']:
            self.users_names[user['id']] = user['name']
        return CONNECTION_OK
    
    def get_channel_id(self, channel_name):
        # return id for channel name passed as argument
        if channel_name in self.channels_ids.keys():
            return self.channels_ids[channel_name]

        else:
            rl= self.get_channels()

            if rl is not CONNECTION_OK:
                return rl

            if channel_name in self.channels_ids.keys():
                return self.channels_ids[channel_name]

            else:
                return None

    def list_channels(self):
        # list all existing channels
        rl = self.get_channels()

        if rl is not CONNECTION_OK:
            return rl
        else:
            return sorted(self.channels_ids.keys())

    def parse_messages(self, content):
        # if not subtype return only messages not events (like joining)
        messages = []
        for mess in content:
            if mess['type'] != 'message':
                continue

            if 'subtype' in mess:
                continue
            
            if 'user' in mess:
                mess['author'] = self.users_names[mess['user']]
            else:
                mess['author'] = 'slack'
            mess['timestamp'] = datetime.fromtimestamp(
                        float(mess['ts'])).strftime('%Y-%m-%d %H:%M:%S')
            messages.append(mess)

        return messages

    def messages_count(self, channel_name):
        # get number of messages on a channel
        chan_id = self.get_channel_id(channel_name)

        if not chan_id:
            return CHANNEL_ERROR
        elif chan_id is CONNECTION_ERROR:
            return chan_id
        else:
            raw_messages = self.slack.channels.history(chan_id)
            if not raw_messages.body['ok']:
                return CONNECTION_ERROR
          
            return len(self.parse_messages(raw_messages.body['messages']))

    def all_messages_count(self):
        count = {}
        channels = self.list_channels()
        
        if isinstance(channels, type(CONNECTION_ERROR)):
            return channels

        for chan in channels:
            count[chan] = self.messages_count(chan)

        return count

    def get_messages(self, channel_name):
        # get all messages from a channel
        chan_id = self.get_channel_id(channel_name)

        if not chan_id:
            return CHANNEL_ERROR
        elif chan_id is CONNECTION_ERROR:
            return chan_id
        else:
            raw_messages = self.slack.channels.history(chan_id)
            if not raw_messages.body['ok']:
                return CONNECTION_ERROR
          
            return self.parse_messages(raw_messages.body['messages'])          

