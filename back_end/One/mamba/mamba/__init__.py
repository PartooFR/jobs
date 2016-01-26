from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/home')
    config.add_route('index', '/')
    config.add_route('boards', '/boards/{username}')
    config.add_route('lists', '/board/lists/{board_id}')
    config.add_route('cards', '/board/cards/{board_id}')
    config.add_route('authenticate', '/auth')
    config.add_route('myboard','/myboard/{token}')
    config.scan()
    return config.make_wsgi_app()
