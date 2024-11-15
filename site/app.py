from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
import db
import logger

log = logger.Log('app', 'logFile.log').get_logger()
db = db.DatabaseManager()
app = Flask(__name__)
CORS(app)

@app.route('/getData', methods=['GET'])
def home():    
    log.info("getData from: " + request.remote_addr)
    return jsonify(db.getRuoliPersone()), 200


@app.route('/getRole', methods=['GET'])
def getRole():
    log.info("getRole from: " + request.remote_addr)
    return jsonify(db.getRuoli()), 200


@app.route('/getPerson', methods=['GET'])
def getPerson():
    log.info("getPerson from: " + request.remote_addr)
    return jsonify(db.getPersone()), 200

@app.route('/addPerson', methods=['POST'])
def addPerson():
    try:
        name = request.json['name']
        db.addPerson(name, None)
        log.info("addPerson from: " + request.remote_addr)
        return jsonify({'status': 'o'}), 200
    except KeyError:
        log.error("addPerson from: " + request.remote_addr)
        abort(400)

@app.route('/addRole', methods=['POST'])
def addRole():
    try:
        name = request.json['ruolo']
        db.addRole(name)
        log.info("addRole from: " + request.remote_addr)
        return jsonify({'status': 'ok'}), 200
    except KeyError:
        log.error("addRole from: " + request.remote_addr)
        abort(400)


if __name__ == '__main__':
    app.run(debug=True)
    
