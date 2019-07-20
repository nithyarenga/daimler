from bottle import Bottle, route, run
from bottle import request, response
from bottle import post, get, put, delete
from json import dumps, loads
from datetime import datetime


app = Bottle()



@app.route('/hello')
def hello():
    return "Hello World!"


run(app, host='172.30.0.163', port=8082, debug=True)

