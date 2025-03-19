import mysql.connector
import os
import hashlib
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            database=os.getenv("DB_NAME"),
        )
        self.cursor = self.connection.cursor(dictionary=True)
    
    # Abilitazione del context manager per usare "with"
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
    
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def checkGoogleId(self, google_id):
        self.cursor.execute("SELECT id FROM logged WHERE google_id = %s", (google_id,))
        user_id = self.cursor.fetchone()
        if(user_id):
            return user_id['id']
        return None
    
    def insertGoogleUser(self, google_id, email, nome, foto):
        self.cursor.execute(
            "INSERT INTO logged (google_id, email, nome, foto) VALUES (%s, %s, %s, %s)",
            (google_id, email, nome, foto)
        )
        user_id = self.cursor.lastrowid 
        self.connection.commit()
        return user_id

    def updateGoogleUser(self, google_id):
        self.cursor.execute("UPDATE logged SET timestamp = %s where google_id = %s", (datetime.utcnow(), google_id))
        self.connection.commit()
        
        
    def checkAdmin(self, id):
        self.cursor.execute("SELECT id FROM admin WHERE id = %s", (id,))
        user_id = self.cursor.fetchone()
        if(user_id):
            return True
        return False
        

    def getPersone(self):
        self.cursor.execute("SELECT id, name, role FROM user ORDER BY role DESC")
        return self.cursor.fetchall()
    
    def getRuoli(self):
        self.cursor.execute("SELECT * FROM role ORDER BY id DESC")
        return self.cursor.fetchall()
    
    def getRuoliPersone(self):
        query = (
            "SELECT u.id, u.name, r.role_name FROM user u "
            "JOIN role r ON u.role = r.id "
            "UNION "
            "SELECT u.id, u.name, 'Fortunello' FROM user u WHERE role IS NULL"
        )
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def addPerson(self, name, role_id) -> None:
        try:
            self.cursor.execute("INSERT INTO user (name, role) VALUES (%s, %s)", (name, role_id))
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"Errore nell'aggiunta della persona: {e}")
    
    def addRole(self, name) -> bool:
        try:
            self.cursor.execute("INSERT INTO role (role_name) VALUES (%s)", (name,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Errore nell'aggiunta del ruolo: {e}")
        return False
    
    def updateRole(self, personId, roleId) -> bool:
        try:
            self.cursor.execute("UPDATE user SET role = %s WHERE id = %s", (roleId, personId))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Errore nell'aggiornamento del ruolo: {e}")
        return False

    def removePerson(self, personId) -> bool:
        try:
            self.cursor.execute("DELETE FROM user WHERE id = %s", (personId,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Errore nella rimozione della persona: {e}")
        return False
    
    def removeRole(self, roleId) -> bool:
        try:
            self.cursor.execute("DELETE FROM role WHERE id = %s", (roleId,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            print(f"Errore nella rimozione del ruolo: {e}")
        return False


def main():
    with DatabaseManager() as db:
        ruoli = ["io", "tu"]
        for r in ruoli:
            db.addRole(r)
        print(db.getRuoliPersone())

if __name__ == '__main__':
    main()



"""

create database clanZenit;
use clanZenit;


create table if not exists role
(
    id int auto_increment primary key,
    role_name varchar(255) not null unique
);

create table if not exists user
(
    id int auto_increment primary key,
    name varchar(255) not null unique ,
    role int,
    foreign key (role) references role (id)
);

create index role on user (role);

create table logged(
    id int primary key auto_increment,
    google_id varchar(510) unique,
    email varchar(255) not null unique,
    nome varchar(255) not null,
    foto text,
    timestamp timestamp not null default current_timestamp,
    UNIQUE KEY idx_foto (foto(255))
);





create table whitelist(
    id varchar(510) primary key,
    email varchar(255) not null unique,
    nome varchar(255) not null,
    foto text,
    UNIQUE KEY idx_foto (foto(255))
);


create table admin(
    id varchar(510) primary key,
    foreign key (id) references logged(id)


"""