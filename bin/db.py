import mysql.connector
import os

class DatabaseManager:
    def __init__(self, host="figliolo.it", user="", password="", database="clanZenit2"):
        user = os.getenv("dbUser")
        password = os.getenv("dbPassword")
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def getPersone(self):
        self.cursor.execute("SELECT * FROM user")
        return self.cursor.fetchall()
    
    def getRuoli(self):
        self.cursor.execute("SELECT * FROM role")
        return self.cursor.fetchall()
    
    def getRuoliPersone(self):
        self.cursor.execute("SELECT u.id, u.name, r.name FROM user u, role r where u.role = r.id")
        return self.cursor.fetchall()
    
    def addPerson(self, name, role_id):
        try:
            self.cursor.execute("INSERT INTO user (name, role) VALUES (%s, %s)", (name, role_id))
            self.connection.commit()
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: nome già esistente / ruolo non esistente")

    def addPerson(self, name):
        try:
            self.cursor.execute("INSERT INTO user (name) VALUES (%s)", (name,))
            self.connection.commit()
            return True
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: nome già esistente")
        return False
    
    def addRole(self, name):
        self.cursor.execute("INSERT INTO role (name) VALUES (%s) where ok", (name,))
        self.connection.commit()
    
    
def main():
    person = ["Figliolo"]
    db = DatabaseManager()
    for p in person:
        db.addPerson(p)
    print(db.getRuoliPersone())



if __name__ == "__main__":
    main()