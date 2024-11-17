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
        name = request.json['ruolo']
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
        db.removePerson(id)
        db.close()
        log.info("removePerson from: " + request.remote_addr)
        return jsonify({'status': 'ok'}), 200
    except KeyError:
        log.error("removePerson from: " + request.remote_addr)
        abort(400)






if __name__ == '__main__':
    app.run(debug=True)
    