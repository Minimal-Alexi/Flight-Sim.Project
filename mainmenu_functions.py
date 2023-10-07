import mysql.connector
from display_functions import display_menu_list,display_country_list,display_continent_list
from Database import (get_continent, get_continent_list, get_airport_list,
                      get_intl_airport_type_list, get_local_airport_type_list, get_country_list, get_user_location,
                      update_player,get_country_from_ident,db_query,getcountry,getcoordinates, get_airport_name_from_ident)
from geopy import distance
from random import randint, random, choice
from Player import Player
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


def distance_limiter(airports,user):
    counter = 0
    airports [:] = [x for x in airports if not distance.distance((x[2],x[3]),getcoordinates(cursor,user.location)).km > user.Fuel*user.Fuel_Efficiency]


def Fuel_Calc(ident,user):
    user.Fuel=int(user.Fuel-distance.distance(getcoordinates(cursor,ident), getcoordinates(cursor, user.location)).km/user.Fuel_Efficiency)


def player_status(user):
    print(f"Current Player Stats:")
    print(f"Fuel Efficiency: {user.Fuel_Efficiency} km/liters")
    print(f"Fuel: {user.Fuel} liters")
    print(f"Money: {user.Money}$")
    print(f"CO2 Budget: {user.CO2_Budget} credits")
    stop = input()


def local_airport_fetcher(cursor, user_id, user: Player):
    # This function will run a cli menu where the user selects an local airport
    print(f"Current location: {get_airport_name_from_ident(user.location, cursor)}")

    country_rn = get_country_from_ident(user.location, cursor)

    # Get airport_type from user
    display_menu_list(get_local_airport_type_list(cursor,country_rn[1]))
    selection = int(input("Select Airport Type: "))

    airport_types = get_local_airport_type_list(cursor, country_rn[1])
    airport_type_sel = airport_types[selection - 1][0]

    # Display available airports
    airports = get_airport_list(cursor, country_rn[1], airport_type_sel)
    distance_limiter(airports,user)
    display_menu_list(airports)

    selection = int(input("Select Airport: "))
    airport_sel = airports[selection - 1][0]

    Fuel_Calc(airports[selection - 1][1], user)
    user.update_location(airports[selection - 1][1], cursor)
    print(f"\nLocation updated to {airport_sel}")

    if is_event():
        event_encounter(user, cursor)



def InternationalAirportFetcher(cursor, user_id, user: Player):

    # This function will run a cli menu where the user selects an international airport
    print(f"Current location: {get_airport_name_from_ident(user.location, cursor)}")

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
    display_menu_list(get_intl_airport_type_list(cursor, country_sel))
    selection = int(input("Select Airport Type: "))

    airport_types = get_intl_airport_type_list(cursor, country_sel)
    airport_type_sel = airport_types[selection - 1][0]

    # Display available airports
    airports = get_airport_list(cursor, country_sel, airport_type_sel)
    distance_limiter(airports,user)
    display_menu_list(airports)
    selection = int(input("Select Airport: "))
    airport_sel = airports[selection - 1][0]
    Fuel_Calc(airports[selection - 1][1], user)
    user.update_location(airports[selection - 1][1], cursor)
    print(f"\nLocation updated to {airport_sel}")

    if is_event():
        event_encounter(user, cursor)




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




# Returns True if an event should be triggered based on chance
def is_event():
    chance = random()
    if chance < 0.10:
        return True
    else:
        return False


# function to spawn an event
def random_event(events):
    random_event = choice(list(events.items()))[1]
    return random_event


# events definition
events = {
    "Event 1": ("You've encountered a sudden robbery! You have lost 35 euros. Sad.", "money", -35),
    "Event 2": ("Uh oh! Seems like there's a LEAK in your FUEL TANK! You lost 10 litres of it. ):", "fuel", -10),
}

def event_encounter(user, cursor):
    event = random_event(events)
    print(event[0])
    if event[1] == "money":
        user.Money = user.Money + event[2]
    elif event[1] == "fuel":
        user.Fuel = user.Fuel + event[2]

