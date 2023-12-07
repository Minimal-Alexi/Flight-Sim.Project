from Password_Management import hashing
import mysql.connector
from Database import (db_query)
from Player_Data import Player
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )
cursor = connection.cursor()

#Puts the user data into the class system for easier manipulation.~Min/Alex
def UserLogin(name, password):
    sql = f"SELECT ID FROM GAME WHERE SCREEN_NAME = '{name}' AND PASSWORD = '{hashing(password)}'"
    result = db_query(sql, cursor)
    if len(result)==1:
        print("User succesfully logged in.")
        sql = f"SELECT ID,MONEY,CO2_BUDGET,LOCATION,SCREEN_NAME,FUEL,FUEL_EFFICIENCY,QUEST,FUELTANK,CARGOCAPACITY FROM GAME WHERE SCREEN_NAME = '{name}'"
        result = db_query(sql,cursor)
        result = result[0]
        user = Player(result[0],result[3],result[4],result[2],result[5],result[1],result[6],result[9],result[8],result[7])
        user.get_Player_data()
        return True,user
    else:
        print("User didn't log in.")
        return False,None
#UserReg picks the data from the form, checks if it's valid, and adds it to the DB.~Min/Alex
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
        sql = f"INSERT INTO GAME (ID,MONEY,CO2_BUDGET,LOCATION,SCREEN_NAME,FUEL,FUEL_EFFICIENCY,PASSWORD,QUEST,FUELTANK,CARGOCAPACITY) VALUES ({maxi},1000,10000,'EFHK','{name}',100,10,'{hashing(password)}','[False, False]','False','False')"
        db_query(sql, cursor)
        print("Registration succesfull!")
        none,user = UserLogin(name,password)
        return True,user
    else:
        print("Registration failed. User already exists.")
        return False,None

def UserList(user,user_list):
    for i in user_list:
        if i.databaseID == user.databaseID:
            print(f"Total user count is {len(user_list)}")
            return False
    user_list.append(user)
    print(f"Total user count is {len(user_list)}")
    return True