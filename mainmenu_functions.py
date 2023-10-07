import mysql.connector
from display_functions import display_menu_list,display_country_list,display_continent_list
from Database import (get_continent, get_continent_list, get_airport_list,
                      get_airport_type_list, get_country_list, get_user_location, set_user_location, update_player,get_country_from_ident,db_query,getcountry)
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
#Creates user entry in DB
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
def getairport(IDENT):
    name = (db_query(f"SELECT NAME FROM AIRPORT WHERE IDENT = '{IDENT}'",cursor))[0]
    return name
#This function logs in the players data into the python function, so we don't have to constantly call from the DB.
def UserLog(user, input):
    sql = f"SELECT CO2_BUDGET,LOCATION,SCREEN_NAME,ID,MONEY,FUEL,FUEL_EFFICIENCY FROM GAME WHERE SCREEN_NAME = '{input}'"
    result = db_query(sql,cursor)
    if cursor.rowcount>0:
        for row in result:
            name = getairport(row[1])[0]
            country = getcountry(cursor,row[1])[0]
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

def local_airport_fetcher(cursor, user_id):
    # This function will run a cli menu where the user selects an local airport
    location = get_user_location(user_id, cursor)
    print(f"Current location: {location[1]}")

    country_rn = get_country_from_ident(location[0], cursor)


    # Get airport_type from user
    display_menu_list(get_airport_type_list(cursor,country_rn[1]))
    selection = int(input("Select Airport Type: "))

    airport_types = get_airport_type_list(cursor, country_rn[1])
    airport_type_sel = airport_types[selection - 1][0]

    # Display available airports
    display_menu_list(get_airport_list(cursor, country_rn[1], airport_type_sel))
    selection = int(input("Select Airport: "))

    airports = get_airport_list(cursor, country_rn[1], airport_type_sel)
    airport_sel = airports[selection - 1][0]

    set_user_location(airports[selection - 1][1], user_id, cursor)

    print(f"\nLocation updated to {airport_sel}")

def InternationalAirportFetcher(cursor, user_id,user):
    # This function will run a cli menu where the user selects an international airport
    location = get_user_location(user_id, cursor)
    print(f"Current location: {location[1]}")

    # Get continent from user
    display_continent_list(get_continent_list(cursor))
    selection = int(input("Select Continent: "))

    continents = get_continent_list(cursor)
    continent_sel = continents[selection - 1][0]

    # Get country from user
    display_menu_list(get_country_list(cursor, continent_sel))
    selection = int(input("Select Country: "))

    countries = get_country_list(cursor, continent_sel)
    country_sel = countries[selection - 1][0]

    # Get airport_type from user
    display_menu_list(get_airport_type_list(cursor, country_sel))
    selection = int(input("Select Airport Type: "))

    airport_types = get_airport_type_list(cursor, country_sel)
    airport_type_sel = airport_types[selection - 1][0]

    # Display available airports
    display_country_list(get_airport_list(cursor, country_sel, airport_type_sel),user)
    selection = int(input("Select Airport: "))

    airports = get_airport_list(cursor, country_sel, airport_type_sel)
    airport_sel = airports[selection - 1][0]

    set_user_location(airports[selection - 1][1], user_id, cursor)

    print(f"\nLocation updated to {airport_sel}")

def NewUser():
    print("Welcome to GreenFLY - The Ultimate Flight Simulator!")
    print("-------------------------------------------------------")
    print("You are starting from Helsinki international airport, your purpose is to travel to LA International airport to deliver water to drought struck California")
    print("You will face many challenges, quests, and financial hurdles, remember to keep your CO2 budget in the positive!")
    print("Are you ready to fly? :3")
    print("\n1 Start your Flight")
    print("2 - Exit")
    user_input = input("Which choice would you like to pick?: ")
    if user_input == '1':
        return True
    elif user_input == '2':
        return False
    else:
        print("Wrong choice. Please enter either 1 or 2.")
        NewUser()