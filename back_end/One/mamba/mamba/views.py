from pyramid.view import view_config
from pyramid.response import Response
import requests

list1= [{
      "id": "4eea4ffc91e31d1746000046",
      "name": "Example Board",
      "desc": "This board is used in the API examples",
      "shortUrl": "https://trello.com/b/OXiBYZoj"
  }, {
      "id": "4ee7e707e582acdec800051a",
      "name": "Public Board",
      "desc": "A board that everyone can see",
      "shortUrl": "https://trello.com/b/IwLRbh3F"
  }]

urlApi = 'https://api.trello.com'

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'mamba'}

@view_config(route_name='index', renderer='templates/index.pt')
def index(request):
    return {'title': 'Mamba to Trello'}
    
@view_config(route_name='authenticate', renderer='templates/authenticate.pt')
def authenticate(request):
    return {'title': 'Authenticate'}
    
@view_config(route_name='boards', renderer='templates/boards.pt')
def boards(request):
    url =  urlApi + '/1/members/trello/boards'
    response_dict = requests.get(url).json()
    return {'boards': response_dict}

@view_config(route_name='cards', renderer='templates/cards.pt')
def cards(request):
    board_id = request.matchdict['board_id']
    response_dict = requests.get(urlApi + '/1/boards/'+board_id+'/cards').json()
    return {'cards': response_dict}
    
@view_config(route_name='lists', renderer='templates/lists.pt')
def cards(request):
    board_id = request.matchdict['board_id']
    response_dict = requests.get(urlApi + '/1/boards/'+board_id+'/lists').json()
    return {'lists': response_dict}

    