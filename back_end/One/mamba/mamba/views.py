from pyramid.view import view_config
from pyramid.response import Response
import requests

urlApi = 'https://api.trello.com'

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'mamba'}

@view_config(route_name='index', renderer='templates/index.pt')
def index(request):
    if 'form.submitted' in request.params:
        name= request.params['username']
        return {'title': 'Mamba to Trello', 'text':request.form['text']}
    return {'title': 'Mamba to Trello', 'text':'trello'}
    
@view_config(route_name='authenticate', renderer='templates/authenticate.pt')
def authenticate(request):
    return {'title': 'Authenticate'}
    
@view_config(route_name='boards', renderer='templates/boards.pt')
def boards(request):
    username =  request.matchdict['username']
    url =  urlApi + '/1/members/'+username+'/boards'
    response_dict = requests.get(url).json()
    return {'boards': response_dict}
    
@view_config(route_name='lists', renderer='templates/lists.pt')
def cards(request):
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

    