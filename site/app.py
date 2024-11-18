from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
import db as dbm
import logger

log = logger.Log('app', 'logFile.log').get_logger()
app = Flask(__name__)
CORS(app)

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
    log.info("getRole from: " + request.remote_addr)
    risp = db.getRuoli()
    db.close()
    return jsonify(risp), 200


@app.route('/getPerson', methods=['GET'])
def getPerson():
    db = dbm.DatabaseManager()
    log.info("getPerson from: " + request.remote_addr)
    risp = db.getPersone()
    db.close()
    return jsonify(risp), 200

@app.route('/addPerson', methods=['POST'])
def addPerson():
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
    try:
        db = dbm.DatabaseManager()
        id = request.json['roleId']
        db.removeRole(id)
        db.close()
        log.info("removeRole from: " + request.remote_addr)
        return jsonify({'status': 'ok'}), 200
    except KeyError:
        log.error("removeRole from: " + request.remote_addr)
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
    