from pyramid.view import view_config
from .slack import SlackAPI, is_valid_token, CONNECTION_OK
from .mongo import all_messages, save_messages, delete_messages

slack = SlackAPI()
name = slack.get_name()

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    global slack
    global name

    action = 'none'
    if 'token' in request.params and request.params['token'] != '':
        token = request.params['token']

        valid = is_valid_token(token)
        if valid == CONNECTION_OK:
            slack = SlackAPI(token)
            name = slack.get_name()
            action= 'changed'
        else:
            action = valid            

    return {'project': 'SlackWebApp',
            'action': action}

@view_config(route_name='channels', renderer='templates/channels.pt')
def channels_view(request):
    return {'channels': slack.list_channels(),
            'count': slack.all_messages_count()}

@view_config(route_name='messages', renderer='templates/messages.pt')
def messages_view(request):
    channel = request.matchdict['channel'] 
    return {'channel': channel,
            'history': slack.get_messages(channel) 
            }
    
@view_config(route_name='backup', request_method='GET', renderer='templates/backup.pt')
def backup_view(request):
    channel = request.matchdict['channel']
    co = name+'.'+channel
    saved_messages = request.db[co].find()
    return {'title': 'BACKUP',
            'channel': channel,
            'messages': all_messages(saved_messages, 
                slack.get_messages(channel)),
            }

@view_config(route_name='backup', request_method='POST', renderer='templates/backup.pt')
def submitted_view(request):
    channel = request.matchdict['channel']
    co = name+'.'+channel
    selected = request.params.getall('selected_messages')
    collection = request.db[co]
    action = 'none'
    
    if 'form.save' in request.params:
        if save_messages(collection, selected):
            action = 'saved'
    elif 'form.delete' in request.params:
        if delete_messages(collection, selected):
            action = 'deleted'
    return {'title': 'SAVED',
            'channel': channel,
            'messages': all_messages(collection.find({}, {'_id':None}), slack.get_messages(channel)),
            'action': action 
            }

