import mysql.connector
import pygame
from Database import (get_continent, get_continent_list, get_airport_list,
                      get_airport_type_list, get_country_list, get_user_location, set_user_location, db_query, update_player)

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

def LocalAirportFetcher():
    return True

# Takes a list and displays as numbered menu
def display_menu_list(disp_list):
    counter = 1
    for x in disp_list:
        print(f"{counter}. {x[0]}")
        counter += 1

def display_continent_list(continents):
    counter = 1
    for x in continents:
        print(f"{counter}. {get_continent(x[0])}")
        counter += 1


def InternationalAirportFetcher(cursor, user_id=1):
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
    display_menu_list(get_airport_list(cursor, country_sel, airport_type_sel))
    selection = int(input("Select Airport: "))

    airports = get_airport_list(cursor, country_sel, airport_type_sel)
    airport_sel = airports[selection - 1][0]

    set_user_location(airports[selection - 1][1], user_id, cursor)

    print(f"\nLocation updated to {airport_sel}")

# After the algorithm fetches the airports, the player is asked if they want to select to go to one of the airports.
# If the player says no they get returned to the main menu, otherwise the flight game starts
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
def UserLog(user, input):
    sql = f"SELECT CO2_BUDGET,LOCATION,SCREEN_NAME,ID,MONEY,FUEL,FUEL_EFFICIENCY FROM GAME WHERE SCREEN_NAME = '{input}'"
    result = db_query(sql,cursor)
    if cursor.rowcount>0:
        for row in result:
            print(f"Hello, you are {row[2]}, at airport {row[1]}, with a CO2_budget of {row[0]}. You have {row[4]}$, very rich :3.")
    user.location = row[1]
    user.CO2_Budget = row[0]
    user.databaseID = row[3]
    user.Fuel = row[5]
    user.Money= row[4]
    user.Fuel_Efficiency = row[6]
def Shop(user):

    print(f"Your current balance: {user.Money}$")
    print(f"Your current CO2 budget: {user.CO2_Budget}")
    items = {
        "Speedbooster_5min": 50,
        "Protectingshield_5min": 50,
        "Advanced_engines": 200,
        "Advanced_fuselage": 200,
    }

    print("Available items:")
    for item, price in items.items():
        print(f"{item}: {price} currency")
    selected_item = input("Enter the item you want to purchase: ")
    if selected_item not in items:
        print("Invalid item selection.")
        return

    item_price = items[selected_item]
    if user.Money < item_price:
        print("You don't have enough money.")
        return
    user.Money = user.Money - item_price
    print(f"Purchase of {selected_item} successful. Your new balance: {user.Money}")
    update_player(cursor,user)
    return True
def EventSystem():
    return True
class Player:
    databaseID = 0
    location = "Placeholder"
    CO2_Budget = 10000
    Fuel = 100
    Money = 100
    Fuel_Efficiency = 5
user = Player
run = False
print("1 - Would you like to register a new user?")
print("2 - Would you like to login as a user?")
print("3 - Quit")
UsInput = int(input("Which choice would you like to pick?"))
if UsInput==1:
    UsInput = input("Enter in new username: ")
    UserReg(UsInput)
    UserLog(user,UsInput)
    run = True
elif UsInput==2:
    UsInput = input("Enter in your username: ")
    UserLog(user, UsInput)
    run = True
else:
    run = False
while run == True:
    #The program will have to remind the player what airport they are located in:
    #Or if they crashed
    print("1 - Move to a local airport: ")
    print("2 - Move to an international airport: ")
    print("3 - Pick up quests from the airport: ")
    print("4 - Airport shop: ")
    print("5 - Airplane stats: ")
    print("6 - Log out. ")
    UsInput = int(input("Which choice would you like to pick?"))
    if UsInput == 1:
        print("WIP")
    elif UsInput == 2:
        InternationalAirportFetcher(cursor)
    elif UsInput == 3:
        print("WIP")
    elif UsInput == 4:
        Shop(user)
    elif UsInput == 5:
        print("WIP")
    else:
        run = False
print("Bye bye user!")
