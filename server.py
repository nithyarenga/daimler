from bottle import Bottle, route, run
from bottle import request, response
from bottle import post, get, put, delete
from json import dumps, loads
from datetime import datetime


app = Bottle()

version = 1 

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/solution')
def question():
    value = request.body.read()
    v = loads(value)
    return {"problem" : "you are the problem", "solution": "what can i do about that", "id": 1}


@app.route('/solution', method='POST')
def solution():
    #write to db 
    return ""

@app.route('/current_question')
def current_question():
    value = request.body.read()
    v = loads(value)
    message = {"problem" : "you are the problem", "solution": "what can i do about that"}
    return message

@app.route('/current_solution', method='POST')
def current_solution():
    return ""

@app.route('/feedback', method='POST')
def feedback():
    return ""

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = {"problem" : "you are the problem", "solution": "what can i do about that", "tags":["version","truck","version"]}
            wsock.send(dumps(message))
        except WebSocketError:
            break

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("172.30.0.163", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()


run(app, host='172.30.0.163', port=8082, debug=True)

