from flask import Flask, render_template, jsonify, request, abort, make_response, session
from flask_cors import CORS
import db as dbm
import logger
import hashlib
import os
from datetime import datetime

log = logger.Log('app', 'logFile.log').get_logger()
app = Flask(__name__)

CORS(app, resources={r"/*": {
    
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

keyEnv = os.getenv("keySession")
if keyEnv is None:
    log.error("key not found")
    exit(1)

app.secret_key = hashlib.sha512(keyEnv.encode()).hexdigest()

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response("", 200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response

@app.route('/getData', methods=['GET'])
def home():
    db = dbm.DatabaseManager()
    log.info("getData from: " + request.remote_addr)
    risp = db.getRuoliPersone()
    db.close()
    return jsonify(risp), 200

@app.route('/getRole', methods=['GET'])
def getRole():
    db = dbm.DatabaseManager()
    
    tok = request.headers.get('Authorization')
    if(db.checkToken(tok) == False):
        log.error("getPerson from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 401
    
    log.info("getRole from: " + request.remote_addr)
    risp = db.getRuoli()
    db.close()
    return jsonify(risp), 200

@app.route('/getPerson', methods=['GET'])
def getPerson():
    db = dbm.DatabaseManager()
    
    tok = request.headers.get('Authorization')
    if(db.checkToken(tok) == False):
        log.error("getPerson from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 401
    
    log.info("getPerson from: " + request.remote_addr)
    risp = db.getPersone()
    db.close()
    return jsonify(risp), 200

@app.route('/addPerson', methods=['POST'])
def addPerson():
    db = dbm.DatabaseManager()
    
    if(db.checkToken(request.headers.get('Authorization')) == False):
        log.error("addPerson from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 401
    db.close()

    try:
        db = dbm.DatabaseManager()
        name = request.json['name']
        db.addPerson(name, None)
        db.close()
        log.info("addPerson from: " + request.remote_addr)
        return jsonify({'status': 'ok'}), 200
    except KeyError:
        log.error("addPerson from: " + request.remote_addr)
        abort(400)

@app.route('/addRole', methods=['POST'])
def addRole():
    try:
        db = dbm.DatabaseManager()
    
        if(db.checkToken(request.headers.get('Authorization')) == False):
            log.error("addPerson from: " + request.remote_addr)
            db.close()
            return jsonify({'status': 'no'}), 401
        db.close()
    
        db = dbm.DatabaseManager()
        name = request.json['roleName']
        db.addRole(name)
        db.close()
        log.info("addRole from: " + request.remote_addr)
        return jsonify({'status': 'ok'}), 200
    except KeyError:
        log.error("addRole from: " + request.remote_addr)
        abort(400)
        
@app.route('/removePerson', methods=['POST'])
def removePerson():
    db = dbm.DatabaseManager()
    
    if(db.checkToken(request.headers.get('Authorization')) == False):
        log.error("addPerson from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 401
    db.close()
    try:
        db = dbm.DatabaseManager()
        id = request.json['id']
        print("id: ", id)
        db.removePerson(id)
        db.close()
        log.info("removePerson from: " + request.remote_addr)
        return jsonify({'status': 'ok'}), 200
    except KeyError:
        log.error("removePerson from: " + request.remote_addr)
        abort(400)

@app.route('/removeRole', methods=['POST'])
def removeRole():
    db = dbm.DatabaseManager()
    
    if(db.checkToken(request.headers.get('Authorization')) == False):
        log.error("addPerson from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 401
    db.close()
    
    try:
        db = dbm.DatabaseManager()
        id = request.json['roleId']
        if(db.removeRole(id)):
            log.info("removed Role from: " + request.remote_addr)
            db.close()
            return jsonify({'status': 'ok'}), 200
        log.info("filed remove role from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 402
    except KeyError:
        log.error("removeRole from: " + request.remote_addr)
        abort(400)

@app.route('/setRole', methods=['POST'])
def setRole():
    db = dbm.DatabaseManager()
    
    if(db.checkToken(request.headers.get('Authorization')) == False):
        log.error("addPerson from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 401
    db.close()
    
    try:
        db = dbm.DatabaseManager()
        id = request.json['personId']
        role = request.json['roleId']
        if(role == 'null'):
            role = None
        if(db.updateRole(id, role)):
            log.info("setRole from: " + request.remote_addr)
            db.close()
            return jsonify({'status': 'ok'}), 200
        log.info("filed setRole from: " + request.remote_addr)
        db.close()
        return jsonify({'status': 'no'}), 402
    except KeyError:
        log.error("setRole from: " + request.remote_addr)
        abort(400)

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == "OPTIONS":
        return make_response("", 200)
    try:
        db = dbm.DatabaseManager()
        user = request.json['user']
        passw = request.json['password']
        passw = hashlib.sha512(passw.encode()).hexdigest()
        data = db.login(user, passw)
        if data is not None:
            if 'session_expire' in data and data['session_expire'] < datetime.now():
                print("exp: ", data['session_expire'])
                db.updateSession(user, passw)
            
            token = db.getTokens(user, passw)
            print("token: ", token)
            
            resp = make_response(jsonify({'status': 'ok', 'token': token[0]['session_id']}), 200)
            db.close()
            return resp

        
        db.close()
        log.error("login from: " + request.remote_addr)
        resp = make_response(jsonify({'status': 'no', 'token': ''}), 401)
        return resp
    except KeyError:
        log.error("login from: " + request.remote_addr)
        abort(400)

'''
oggi una news ma inutile
ce no

se gio lalista stampata qui in testa me le ricordo
non lavevo stampata in testa
tutto qua. da ora in poi lo userò
lho detto --> lo farò

tutti e due
NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
SIIIIIIIIIIIIIIIIIIIIIIIIIIII


bocco python
questo è python



MA A ME COSA ME NE FREGA DI HARRU POTTER SCUSA????????????????????


SI COSSRISPONDE AL MIO LIVELLO DI



NON ME NE FREGA NIENTE!!!!!!!!!!!!


ANCORA PEGGIO 


MA MI INTERESSAAAA 
TUTTO CIO CHE PendingDeprecationWarning




ANCHE QUESTO MI INTERESSA E bFA PARTE DELLINSIEME DI PRIMA (TUTTO QUELLO CHE DICI)




TUTTO QUELLO CHE DICI ⊆ TUTTO QUELLO CHE MI INTERESS
in harry potter c'è il diario di tom riddle (voldemort) che giunge nelle mani di ginny weasly (la sorella del rosso(ron)) --> lei ci scrive e lui gli risponde facendo comparire delle scritte sul diario come fai tu

'''

if __name__ == '__main__':
    app.run(debug=True)
    