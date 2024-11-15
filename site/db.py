import mysql.connector
import os

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

    def getPersone(self):
        self.cursor.execute("SELECT id, name FROM user ORDER BY role desc")
        return self.cursor.fetchall()
    
    def getRuoli(self):
        self.cursor.execute("SELECT * FROM role ORDER BY id desc")
        return self.cursor.fetchall()
    
    def getRuoliPersone(self):
        self.cursor.execute("SELECT u.id, u.name, r.role_name FROM user u, role r where u.role = r.id union select u.id, u.name, 'Fortunello' FROM user u where role is null")
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
        try:
            self.cursor.execute("INSERT INTO role (role_name) VALUES (%s)", (name,))
            self.connection.commit()
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: ruolo già esistente")
        return False
    
    def updateRole(self, personId, roleId):
        try:
            self.cursor.execute("UPDATE user SET role = %s WHERE id = %s", (roleId, personId))
            self.connection.commit()
        except mysql.connector.errors.IntegrityError as e:
            print(e)
            print("Errore: ruolo non esistente")
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