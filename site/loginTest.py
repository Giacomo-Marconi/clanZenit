import os
import jwt
import datetime
import pymysql
from flask import Flask, request, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from authlib.integrations.flask_client import OAuth
from functools import wraps

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = os.getenv("KEY_SESS")

# Configurazione OAuth
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

# Connessione al database
def get_db_connection():
    return pymysql.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306"))
    )

# Middleware per proteggere le rotte con JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token mancante!"}), 403
        try:
            decoded = jwt.decode(token.split()[1], app.secret_key, algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token scaduto!"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token non valido!"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route("/login")
def login():
    return google.authorize_redirect(url_for("authorize", _external=True))

@app.route("/login/callback")
def authorize():
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()
    print(user_info)
    google_id = user_info["id"]
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM logged WHERE google_id = %s", (google_id,))
    user = cur.fetchone()
    
    if not user:
        cur.execute(
            "INSERT INTO logged (google_id, email, nome, cognome, foto) VALUES (%s, %s, %s, %s, %s)",
            (google_id, user_info["email"], user_info.get("given_name"), user_info.get("family_name"), user_info.get("picture"))
        )
        user_id = cur.lastrowid 
        conn.commit()
    else:
        user_id = user[0]
        cur.execute("UPDATE logged SET timestamp = %s where google_id = %s", (datetime.datetime.utcnow(), google_id))
    
    cur.close()
    conn.close()
    
    jwt_token = jwt.encode({
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=1)
    }, app.secret_key, algorithm="HS256")
    
    return jsonify({"token": jwt_token})

@app.route("/dashboard")
@token_required
def dashboard():
    return jsonify({"message": "Benvenuto nel dashboard", "user": request.user})

if __name__ == "__main__":
    app.run(debug=True)
