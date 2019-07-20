from bottle import Bottle, route, run
from bottle import request, response
from bottle import post, get, put, delete
from json import dumps, loads
from datetime import datetime


app = Bottle()


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

@app.route('/question')
def question():
    value = request.body.read()
    v = loads(value)
    return {"problem" : "you are the problem", "solution": "what can i do about that"}


@app.route('/solution', method='POST')
def solution():
    return ""


run(app, host='172.30.0.163', port=8082, debug=True)

