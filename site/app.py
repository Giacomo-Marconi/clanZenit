from flask import Flask, jsonify, request, abort, make_response, redirect, url_for
from flask_cors import CORS
import db as dbm
import logger
import os
import datetime
import shuffle as sh
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
from functools import wraps
import jwt

# Configurazione del logger
log = logger.Log('app', 'logFile.log').get_logger()


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.getenv("KEY_SESS")

oauth = OAuth(app)
google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_ID"),
    client_secret=os.getenv("GOOGLE_SECR"),
    access_token_url="https://oauth2.googleapis.com/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://www.googleapis.com/oauth2/v1/userinfo",
    client_kwargs={"scope": "openid email profile"},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
)

# Configurazione CORS
# CORS(app, resources={r"/*": {
#     "methods": ["GET", "POST", "OPTIONS"],
#     "allow_headers": ["Content-Type", "Authorization"]
# }}, origins=["http://127.0.0.1"])

CORS(app)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        print(token)
        if not token:
            return jsonify({"message": "Token mancante!"}), 403
        try:
            decoded = jwt.decode(token.split()[1], app.secret_key, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            print("Token scaduto")
            return jsonify({"message": "Token scaduto!"}), 403
        except jwt.InvalidTokenError:
            print("Token non valido")
            return jsonify({"message": "Token non valido!"}), 403
        except IndexError:
            print("Token index error")
            return jsonify({"message": "Token non valido!"}), 403
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print("admin_required")
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token mancante!"}), 403
            
        try:
            decoded = jwt.decode(token.split()[1], app.secret_key, algorithms=["HS256"])
            request.user = decoded
            print(decoded)
            # Verifica se l'utente è admin
            user_id = decoded.get('id')
            
            if not user_id:
                print("ID utente non valido")
                return jsonify({"message": "ID utente non valido nel token!"}), 403
                
            with dbm.DatabaseManager() as db:
                if( not db.checkAdmin(user_id)):
                    print("Utente non admin")
                    return jsonify({"message": "Accesso riservato agli amministratori!"}), 401
            
                
        except jwt.ExpiredSignatureError:
            print("Token scaduto")
            return jsonify({"message": "Token scaduto!"}), 403
        except (jwt.InvalidTokenError, IndexError):
            print("Token non valido")
            return jsonify({"message": "Token non valido!"}), 403
        except Exception as e:
            print(f"Errore durante il controllo admin: {str(e)}")
            return jsonify({"message": "Errore interno del server"}), 500
            
        return f(*args, **kwargs)
    return decorated



# Gestione globale delle richieste OPTIONS
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response("", 200)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response


@app.route('/getData', methods=['GET'])
def get_data():
    with dbm.DatabaseManager() as db:
        log.info("getData da: " + request.remote_addr)
        result = db.getRuoliPersone()
    return jsonify(result), 200


@app.route('/getRole', methods=['GET'])
@admin_required
def get_role():
    with dbm.DatabaseManager() as db:
        result = db.getRuoli()
    return jsonify(result), 200


@app.route('/getPerson', methods=['GET'])
@admin_required
def get_person():
    with dbm.DatabaseManager() as db:
        result = db.getPersone()
    return jsonify(result), 200


@app.route('/addPerson', methods=['POST'])
@admin_required
def add_person():
    try:
        name = request.json['name']
    except KeyError:
        log.error("addPerson: parametro 'name' mancante da: " + request.remote_addr)
        abort(400)
    with dbm.DatabaseManager() as db:
        db.addPerson(name, None)
        log.info("addPerson eseguito da: " + request.remote_addr)
    return jsonify({'status': 'ok'}), 200


@app.route('/addRole', methods=['POST'])
@admin_required
def add_role():
    try:
        role_name = request.json['roleName']
    except KeyError:
        log.error("addRole: parametro 'roleName' mancante da: " + request.remote_addr)
        abort(400)
    with dbm.DatabaseManager() as db:
        if db.addRole(role_name):
            log.info("addRole eseguito da: " + request.remote_addr)
            return jsonify({'status': 'ok'}), 200
        else:
            log.error("addRole fallito da: " + request.remote_addr)
            return jsonify({'status': 'no'}), 402


@app.route('/removePerson', methods=['POST'])
@admin_required
def remove_person():
    try:
        person_id = request.json['id']
    except KeyError:
        log.error("removePerson: parametro 'id' mancante da: " + request.remote_addr)
        abort(400)
    with dbm.DatabaseManager() as db:
        db.removePerson(person_id)
        log.info("removePerson eseguito da: " + request.remote_addr)
    return jsonify({'status': 'ok'}), 200


@app.route('/removeRole', methods=['POST'])
@admin_required
def remove_role():
    try:
        role_id = request.json['roleId']
    except KeyError:
        log.error("removeRole: parametro 'roleId' mancante da: " + request.remote_addr)
        abort(400)
    with dbm.DatabaseManager() as db:
        if db.removeRole(role_id):
            log.info("removeRole eseguito da: " + request.remote_addr)
            return jsonify({'status': 'ok'}), 200
        else:
            log.error("removeRole fallito da: " + request.remote_addr)
            return jsonify({'status': 'no'}), 402


@app.route('/setRole', methods=['POST'])
@admin_required
def set_role():
    try:
        person_id = request.json['personId']
        role_id = request.json['roleId']
        role_id = None if role_id == 'null' else role_id
    except KeyError:
        log.error("setRole: parametri mancanti da: " + request.remote_addr)
        abort(400)
    with dbm.DatabaseManager() as db:
        if db.updateRole(person_id, role_id):
            log.info("setRole eseguito da: " + request.remote_addr)
            return jsonify({'status': 'ok'}), 200
        else:
            log.error("setRole fallito da: " + request.remote_addr)
            return jsonify({'status': 'no'}), 402


@app.route("/login")
def login():
    return google.authorize_redirect(url_for("authorize", _external=True))

@app.route("/login/callback")
def authorize():
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()
    #print(user_info)
    google_id = user_info["id"]
    
    with dbm.DatabaseManager() as db:
        user = db.checkGoogleId(google_id)
    
        if not user:
            print(user_info)
            user_id = db.insertGoogleUser(google_id, user_info["email"], user_info.get("name"), user_info.get("picture"))
        else:
            user_id = db.checkGoogleId(google_id)
            db.updateGoogleUser(google_id)
    
    jwt_token = jwt.encode({
        "id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.secret_key, algorithm="HS256")
    #return jsonify({"token": jwt_token})
    return redirect(f'http://127.0.0.1/login.html?token={jwt_token}')

@app.route('/shuffle', methods=['POST'])
@admin_required
def shuffle_route():
    if sh.shuffle():
        log.info("shuffle eseguito da: " + request.remote_addr)
        return jsonify({'status': 'ok'}), 200
    return jsonify({'status': 'no'}), 402

if __name__ == '__main__':
    app.run(debug=True)


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
