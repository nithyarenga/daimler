from bottle import Bottle, route, run
from bottle import request, response
from bottle import post, get, put, delete
from json import dumps, loads
from  datetime import datetime
from bin import benz_main

app = Bottle()

version = 0
questioni = ""
knowledgei = 0
lab_view = "0"
fakeq = 0 
img_url = ""
#tags = ["string"]
solutioni = ""

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

def increment_version():
    global version
    if version < 5:
        version = version + 1
    global img_url
    img_url = benz_main.fnget_imgurls(version)
    
@app.route('/hello')
def hello():
    #return "Hello World!"
    #q = benz_main.fnget_question(2)
    return q

@app.route('/knowledge')
def new_knowledge():
    global knowledgei
    global questioni
    global solutioni
    print(knowledgei)
    print(solutioni)
    print(questioni)
    #return {"version": "v", "question":"How to fix the fuel system injector? ","answer":" Cap off the cylinders in the following sequence - 1, 3, 2 and 4. After capping off each cylinder, crank the engine and see if the crank time reduces to 3 to 5 seconds. If it does, you have found your leaking cylinder.If not,proceed to the next cylinder","tags":["DD13","fuel injector"]}
    return {"version": knowledgei, "question": questioni, "answer": solutioni ,"tags":["dd13","fuel"]}
@app.route('/solution')
def question():
    # value = request.body.read()
    #v = loads(value)
    prob = request.query.problem
    global version 
    version = 2
    return {"problem" : "you are the problem", "solution": "what can i do about that", "id": 1}


@app.route('/reset')
def change():
    new_version = request.query.version
    global version
    global img_url
    version = int(new_version)
    if version == 0:
        img_url = ""
    global knowledgei
    knowledgei = int(new_version)
    global lab_view
    lab_view = new_version
    global questioni
    questioni = ""
    global solutioni
    solutioni = ""

@app.route('/change_lab')
def change_lab():
    new_version = request.query.version
    global lab_view
    lab_view = new_version

@app.route('/fake')
def fake():
    increment_version()
    global version
    #if lab_view == "0" :
    #    lab_view = "1"
    #elif lab_view == "1":
    #    lab_view = "0"
    return str(version)

@app.route('/solution', method='POST')
def solution_new():
    #write to db 
    try:
        value = request.body.read()
        print(value)
        if value is not None:
            v = loads(value)
            print(v)
    #except:
     #   print("error in solution post")
    #query = dumps(v)
       # benz_main.fnwrite_solution(1,v["solution"])
        global knowledgei
        knowledgei = 1
        global questioni
        questioni = v["problem"]
        global solutioni
        solutioni = v["solution"]
    except:
        print(v)
   # solution, keywords = benz_main.fnget_recent_solutions(1)
    #global tags
    return ""


@app.route('/current_question')
def current_question():
    return {"version": version, "img_url":img_url}

@app.route('/current_solution', method='POST')
def current_solution():
    return ""

@app.route('/feedback')
def feedback():
    query_id = request.query.id
    return ""

@app.route('/lab_view')
def lab():
    return {"version": lab_view}

@app.route("/metrics")
def metrics():
    global lab_view
    lab_view = "1"


@app.route('/start')
def startn():
    global questioni
    questioni = request.query.search
    increment_version()
    return { "start" : "I found a solution. I see that you have 2 of the 3 parts needed for the job in your bay. I have already requested for a fuel rail test cap and the part runner is on his way." , "steps":["Remove the valve cover and start the engine and let it idle. A small amount of white smoke is normal. If you don’t see smoke, one of the cylinders might be cracked","You have to do a manual cylinder cut-off test to find the problematic cylinder","One of your colleagues fixed a similar problem recently for the same engine. I can pull up his notes.","This is what he did - Cap off the cylinders in the following sequence - 1, 3, 2 and 4. After capping off each cylinder, crank the engine and see if the crank time reduces to 3 to 5 seconds. If it does, you have found your leaking cylinder. If not, proceed to the next cylinder"]}
@app.route('/show')
def feedback():
    global version
    version = "steps"
    return nil
# @app.route('/websocket')
# def handle_websocket():
#     wsock = request.environ.get('wsgi.websocket')
#     if not wsock:
#         abort(400, 'Expected WebSocket request.')
#     while true:
#         try:
#             message = wsock.receive()
#             message = {"problem" : "you are the problem", "solution": "what can i do about that", "tags":["version","truck","version"]}
#             wsock.send(dumps(message))
#         except WebSocketError:
#                 break

run(app, host='172.30.0.163', port=8080, debug=True, reloader=True)

