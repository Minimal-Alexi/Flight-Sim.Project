from Password_Management import hashing
import mysql.connector
from Database import (db_query)
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )
cursor = connection.cursor()

def UserReg(name,password):
    sql = f"SELECT ID FROM GAME WHERE SCREEN_NAME = '{name}'"
    result = db_query(sql, cursor)
    if len(result)==0:
        sql = f"SELECT max(id) FROM GAME"
        result = db_query(sql, cursor)
        if cursor.rowcount == 1 and result[0] != (None,):
            (maxi,) = result[0]
            maxi = int(maxi)
            maxi = maxi + 1
        else:
            maxi = 1
        sql = f"INSERT INTO GAME (ID,MONEY,CO2_BUDGET,LOCATION,SCREEN_NAME,FUEL,FUEL_EFFICIENCY,PASSWORD) VALUES ({maxi},1000,10000,'EFHK','{name}',100,10,'{hashing(password)}')"
        db_query(sql, cursor)
        print("Registration succesfull!")
        return True
    else:
        print("Registration failed. User already exists.")
        return False

