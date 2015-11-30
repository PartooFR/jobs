from pyramid.view import view_config
from pyramid.response import Response
import requests
from pyramid.httpexceptions import HTTPFound

urlApi = 'https://api.trello.com'
appKey = '464961dc9bfdd33036f0131101b6d72d'

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'mamba'}

@view_config(route_name='index', renderer='templates/index.pt')
def index(request):
    if 'form.submitted' in request.params:
        name= request.params['text']
        return HTTPFound(location=request.route_url('boards', username=name))
    return {'title': 'Mamba to Trello', 'text':'trello'}
    
@view_config(route_name='boards', renderer='templates/boards.pt')
def boards(request):
    username =  request.matchdict['username']
    url =  urlApi + '/1/members/'+username+'/boards'
    response_dict = requests.get(url).json()
    return {'boards': response_dict}
    
@view_config(route_name='lists', renderer='templates/lists.pt')
def lists(request):
    board_id = request.matchdict['board_id']
    url = urlApi + '/1/boards/'+board_id+'/lists'
    response_dict = requests.get(url).json()
    return {'lists': response_dict}
    
@view_config(route_name='cards', renderer='templates/cards.pt')
def cards(request):
    board_id = request.matchdict['board_id']
    url = urlApi + '/1/boards/'+board_id+'/cards'
    response_dict = requests.get(url).json()
    return {'cards': response_dict}
    
@view_config(route_name='authenticate', renderer='templates/authenticate.pt')
def authenticate(request):
    if 'form.submit' in request.params:
        token= request.params['token']
        return HTTPFound(location=request.route_url('myboard', token=token))
    return {'title': 'Authenticate', 'token': ''}
    
@view_config(route_name='myboard', renderer='templates/myboards.pt')
def myboard(request):
    token =  request.matchdict['token']
    url =  urlApi+'/1/members/me?fields=username,fullName,url&boards=all&board_fields=name&organizations=all&organization_fields=displayName&key='+appKey+'&token='+token
    response_dict = requests.get(url).json()
    return {'myboards': response_dict}

    