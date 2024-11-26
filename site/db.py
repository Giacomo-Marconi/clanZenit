import mysql.connector
import os
import hashlib

class DatabaseManager:
    def __init__(self, host="figliolo.it", user="", password="", database="clanZenit2"):
        user = os.getenv("dbUser")
        print(user)
        password = os.getenv("dbPassword")
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    def close(self):
        self.cursor.close()
        self.connection.close()

    def getPersone(self):
        self.cursor.execute("SELECT id, name, role FROM user ORDER BY role desc")
        return self.cursor.fetchall()
    
    def getRuoli(self):
        self.cursor.execute("SELECT * FROM role ORDER BY id desc")
        return self.cursor.fetchall()
    
    def getRuoliPersone(self):
        self.cursor.execute("SELECT u.id, u.name, r.role_name FROM user u, role r where u.role = r.id union select u.id, u.name, 'Fortunello' FROM user u where role is null")
        return self.cursor.fetchall()
    
    def addPerson(self, name, role_id) -> None:
        try:
            self.cursor.execute("INSERT INTO user (name, role) VALUES (%s, %s)", (name, role_id))
            self.connection.commit()
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: nome già esistente / ruolo non esistente")
    
    def addRole(self, name) -> bool:
        try:
            self.cursor.execute("INSERT INTO role (role_name) VALUES (%s)", (name,))
            self.connection.commit()
            return True
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: ruolo già esistente")
        return False
    
    def updateRole(self, personId, roleId) -> bool:
        try:
            self.cursor.execute("UPDATE user SET role = %s WHERE id = %s", (roleId, personId))
            self.connection.commit()
            return True
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: ruolo non esistente")
        return False

    def removePerson(self, personId) -> bool:
        try:
            self.cursor.execute("DELETE FROM user WHERE id = %s", (personId,))
            self.connection.commit()
            return True
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: utente non esistente")
        return False
    
    def removeRole(self, roleId) -> bool:
        try:
            self.cursor.execute("DELETE FROM role WHERE id = %s", (roleId,))
            self.connection.commit()
            return True
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: ruolo non esistente")
        return False
    
    def login(self, user, passw) -> dict:
        self.cursor.execute("SELECT * FROM admin WHERE username = %s and password = %s", (user, passw))
        data = self.cursor.fetchall()
        if(len(data) == 1):
            if(data[0]['username'] == user and data[0]['password'] == passw):
                return data[0]
        return None
    
    def updateSession(self, user, passw) -> None:
        self.updateToken(user, passw)
        self.cursor.execute("UPDATE admin SET session_expire = DATE_ADD(NOW(), INTERVAL 3 DAY) WHERE username = %s and password = %s", (user, passw))
        self.connection.commit()
        
    def updateToken(self, user, passw) -> None:
        token = hashlib.sha512(os.urandom(24)).hexdigest()
        self.cursor.execute("UPDATE admin SET session_id = %s WHERE username = %s and password = %s", (token, user, passw))

    def getTokens(self, user, passw) -> list:
        self.cursor.execute("SELECT session_id, session_expire FROM admin where username = %s and password = %s", (user, passw))
        return self.cursor.fetchall()
    
    def checkToken(self, token) -> bool:
        self.cursor.execute("SELECT * FROM admin where session_id = %s and session_expire > now()", (token,))
        data = self.cursor.fetchall()
        if(len(data)==1):
            return True
        return False
    




def main():
    db = DatabaseManager()
    
    """
    person = ["Figliolo", "Giacomo", "test"]
    for p in person:
        db.addPerson(p)
    """
        
    role = ["io", "tu"]
    for r in role:
        db.addRole(r)
    print(db.getRuoliPersone())



if __name__ == "__main__":
    main()