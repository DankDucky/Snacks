import json
import os
import random
import bottle
import platform

from api import ping_response, start_response, move_response, end_response

last_move=''

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#00FF00"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data, indent=2))
    
    global last_move


    directions = ['up', 'down', 'left', 'right']
    #direction = random.choice(directions)
    if last_move=='':
        direction = 'down'
    
    if last_move=='down':
        direction='right'
        
    if last_move=='right':
        direction='up'
        
    if last_move=='up':
        direction='left'
        
    if last_move=='left':
        direction='down'

        
    last_move = direction
    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    s = platform.system()
    if s == 'Darwin':
        bottle.run(
            application,
            host=os.getenv('IP', '0.0.0.0'),
            port=os.getenv('PORT', '8080'),
            debug=os.getenv('DEBUG', True),
            #server='paste'
            server='tornado'      )
    else:
        bottle.run(
            application,
            host=os.getenv('IP', '0.0.0.0'),
            port=os.getenv('PORT', '80'),
            debug=os.getenv('DEBUG', True)
        )


