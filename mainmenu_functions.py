import mysql.connector
from Database import db_query
from random import randint
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )

# Create a cursor for all interactions with the MariaDB Database
cursor = connection.cursor()
def UserReg(input):
    sql = f"SELECT max(id) FROM GAME"
    result = db_query(sql,cursor)
    if cursor.rowcount == 1 and result[0]!=(None,):
        (maxi, ) = result[0]
        maxi = int(maxi)
        maxi = maxi + 1
    else:
        maxi = 1
    sql = f"INSERT INTO GAME (ID,MONEY,CO2_BUDGET,LOCATION,SCREEN_NAME,FUEL,FUEL_EFFICIENCY) VALUES ({maxi},100,10000,'EGCC','{input}',100,5)"
    db_query(sql,cursor)
#This function logs in hte players data into the python function, so we don't have to constantly call from the DB.
def getairport(IDENT):
    name = (db_query(f"SELECT NAME FROM AIRPORT WHERE IDENT = '{IDENT}'",cursor))[0]
    return name
def getcountry(name):
    country = db_query(f"SELECT COUNTRY.NAME FROM AIRPORT,COUNTRY WHERE AIRPORT.NAME = '{name}' AND AIRPORT.ISO_COUNTRY = COUNTRY.ISO_COUNTRY",cursor)[0]
    return country
def UserLog(user, input):
    sql = f"SELECT CO2_BUDGET,LOCATION,SCREEN_NAME,ID,MONEY,FUEL,FUEL_EFFICIENCY FROM GAME WHERE SCREEN_NAME = '{input}'"
    result = db_query(sql,cursor)
    if cursor.rowcount>0:
        for row in result:
            name = getairport(row[1])[0]
            country = getcountry(name)[0]
            print(f"Hello, you are {row[2]}, at airport {name} ({country}), with a CO2_budget of {row[0]}. You have {row[4]}$, very rich :3.")
    user.location = row[1]
    user.CO2_Budget = row[0]
    user.databaseID = row[3]
    user.Fuel = row[5]
    user.Money= row[4]
    user.Fuel_Efficiency = row[6]

def Goodbye():
    Randomgoodbye = randint(1, 5)
    GoodbyeMessage = {
            1:"Guess this was too Boe-ing for you",
            2:"I'll just sit over here and watch, carry-on.",
            3:"At this moment I think your head is in the clouds.",
            4:"I'd stick around but I gotta jet.",
            5:"Nooo...but think of all the Californians, they were looking UP to you...well...nevermind, it's probably better if you log out."
        }
    print(GoodbyeMessage[Randomgoodbye])

def player_status(user):
    print(f"Current Player Stats:")
    print(f"Fuel Efficiency: {user.Fuel_Efficiency} km/liters")
    print(f"Fuel: {user.Fuel} liters")
    print(f"Money: {user.Money}$")
    print(f"CO2 Budget: {user.CO2_Budget} credits")
    stop = input()