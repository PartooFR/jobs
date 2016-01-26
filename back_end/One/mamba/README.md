#Mamba

This App was my first trial with Pyramid Framework. Basically, it is meant to display user's boards, cards or lists using Trello API.
Given that I started learning how to use Pyramid less than a week ago, this is pretty basic. For what I can tell, there is still room for improvment.


The docs are detailed here : 
* [Pyramid] (http://pyramid-cookbook.readthedocs.org/en/latest/index.html)
* [Trello] (https://developers.trello.com/apis)


## Requirements
This apps requires:
* Python 3.5
* Pyramid 1.5 

It would be useful to have a dependency manager like pip for python modules, but not required.
Bower is needed to install some components , i.e bootstrap...
## Setup

First
Create a virtual env
```sh
export VENV=~/env
```
Then install the app, *make sure you open the terminal at the root of mamba*
```sh
$VENV/bin/python setup.py develop
```

You're ready to try now after this last line 
```sh
$VENV/bin/pserve development.ini
```

## Database
No database required

## Overall architecture

There mainly two views, for two simple features. 

One meant to use a given Id or username, and get public informations. The other uses a user token. 
__init__.py provides with the routes and the views they refer.

In few words, the Pyramid app has 6 views:
* index: It is just form where the user provides his username, and is directed to boards. When the user clicks on submit, the index function fires a httpFound to switch to the next view.
* authenticate: Works like index, except the user provide his token, and is directed to myboard
* boards : Display a user's boards, with links to get specific informations about the boards' cards and lists 
* cards and lists refer to cards and lists found on trello 
* myboard is meant to show specific boards of a given user.

For detailled information, please refer to views.py.

## Improvement

At this stage the user has to provide his token, to grant our app to his trello... Not very convenient, a more serious thorough implementation would store the token directly from trello.
The user could also manage his boards, cards, even create them, if only those actions are available. A simple look at trello's API and everything would be set up.