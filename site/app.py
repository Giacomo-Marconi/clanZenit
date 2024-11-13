from flask import Flask, render_template, jsonify, request, abort
from flask_cors import CORS
import db



db = db.DatabaseManager()
app = Flask(__name__)
CORS(app)

@app.route('/getData', methods=['GET'])
def home():    
    return jsonify(db.getRuoliPersone()), 200


@app.route('/getRole', methods=['GET'])
def getRole():
    return jsonify(db.getRuoli()), 200


@app.route('/getPerson', methods=['GET'])
def getPerson():
    return jsonify(db.getPersone()), 200

@app.route('/addPerson', methods=['POST'])
def addPerson():
    try:
        name = request.json['name']
        role = request.json['role']
        db.addPerson(name, role)
        return jsonify({'status': 'o'}), 200
    except KeyError:
        abort(400)

@app.route('/addRole', methods=['POST'])
def addRole():
    try:
        name = request.json['ruolo']
        db.addRole(name)
        return jsonify({'status': 'ok'}), 200
    except KeyError:
        print("Errore")
        abort(400)
        



if __name__ == '__main__':
    app.run(debug=True)
    
