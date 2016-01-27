from pyramid.view import view_config
from .slack import SlackAPI

slack = SlackAPI()

@view_config(route_name='home', renderer='templates/home.pt')
def home_view(request):
    return {'project': 'SlackWebApp'}

@view_config(route_name='channels', renderer='templates/channels.pt')
def channels_view(request):
    return {'channels': slack.list_channels()}

