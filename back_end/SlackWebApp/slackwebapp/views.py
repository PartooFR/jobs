from pyramid.view import view_config
from .slack import SlackAPI

slack = SlackAPI()

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    return {'project': 'SlackWebApp'}

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
