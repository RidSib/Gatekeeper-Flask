import os
import sqlite3
from flask import Flask, request, render_template, Response, jsonify, g, abort
from gpiozero import LED
from time import sleep
from camera_pi import Camera
from passlib.hash import sha256_crypt
DATABASE = '/home/pi/Desktop/Bsc_Project3/database.db'
QUERY_GET_USER = 'select password, id from USERS where LOGIN = ?'
QUERY_FUNCTION_LIST = 'select f.id, f.function_name, f.function_type from functions ' \
                      +'f inner join user_functions u ' \
                      +'on f.id = u.function_id where u.user_id = ?'
QUERY_IS_USER_FUNCTION_VALID = 'select 1 from user_functions u' \
                               +' where u.user_id = ? and u.function_id = ?'
led = LED(17)
app = Flask(__name__)
led.on()
showCam = 0

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    }
]


#db connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#close db connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#query execution with list of results
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    print "Report: open"
    #print validateLogin('test@uclan.ac.uk', 'test');
    showCam = 0
    return render_template('index.html', showCam=showCam)

@app.route('/', methods=['POST'])
def index2():
    global showCam
    print "Report: post"
    if request.form['submit'] == 'Open door':
        print "Report: open"
        led.off()
        sleep(3)
        led.on()
    elif request.form['submit'] == 'Turn camera on':
        print "Report: on"
        showCam = 1
    elif request.form['submit'] == 'Turn camera off':
        print "Report: off"
        showCam = 0
    return render_template('index.html', showCam=showCam)

@app.route('/api/json', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/api/json/login', methods=['POST'])
def serviceLogin():    
    userId = getUser()
    if userId > 0:
        functionMap = []
        for function in query_db(QUERY_FUNCTION_LIST, [userId]): #gets function list
            print function
            functionList = {
                    'id': function[0],
                    'name': function[1],
                    'type': function[2]
                }
            functionMap.append(functionList)
        return jsonify({'functions': functionMap})
    abort(400)

@app.route('/api/json/activity', methods=['POST'])
def activateFunction():
    if not request.json or not 'function' in request.json:
        abort(400)
    userId = getUser()
    if userId > 0:
        if query_db(QUERY_IS_USER_FUNCTION_VALID, [userId, request.json['function']], one=True) is None:
            abort(400)
        return 'success'
    abort(400)

def getUser():
    #returns list of elements if one false or not set
    if not request.json or not 'login' in request.json or not 'password' in request.json:
        abort(400)
    login = request.json['login']
    password = request.json['password']
    dbPassword = query_db(QUERY_GET_USER, [login], one=True)

    if dbPassword is None:
        return 0
    else:
        if sha256_crypt.verify(password, dbPassword[0]):
            return dbPassword[1] #user ID
        return 0
    #for user in query_db('select * from users'):
        #print user['username'], 'has the id', user['user_id']
    
def gen(camera):
    """Video streaming generator function."""
    while showCam == 1:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
