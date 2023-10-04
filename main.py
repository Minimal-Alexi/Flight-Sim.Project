import mysql.connector
from Shop import shop
import pygame
from Database import (get_continent, get_continent_list, get_airport_list,
                      get_airport_type_list, get_country_list, get_user_location, set_user_location, db_query, update_player)
from more_functions import display_continent_list, display_menu_list, local_airport_fetcher,display_country_limit_list
from mainmenu_functions import (UserLog,UserReg,Goodbye)
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

# After the algorithm fetches the airports, the player is asked if they want to select to go to one of the airports.
# If the player says no they get returned to the main menu, otherwise the flight game starts
def InternationalAirportFetcher(cursor, user_id):
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
    display_country_limit_list(get_airport_list(cursor, country_sel, airport_type_sel),user)
    selection = int(input("Select Airport: "))

    airports = get_airport_list(cursor, country_sel, airport_type_sel)
    airport_sel = airports[selection - 1][0]

    set_user_location(airports[selection - 1][1], user_id, cursor)

    print(f"\nLocation updated to {airport_sel}")
#This function registers the user into the database
def Shop(user):
    print(f"Your current balance: {user.Money}$")
    print(f"Your current CO2 budget: {user.CO2_Budget}")
    print(f"Your current CO2 budget: {user.Fuel}")
    Refuel = 100 - user.Fuel
    #All items have a money and CO2 price
    items = {
        "+5km/l Fuel Efficiency": (1000,100),
        "Refueling Services": (Refuel*10,Refuel*10+500),
        "Environmental-Friendly Refueling Services": (Refuel * 10 + 500, Refuel * 10),
        "One-Time Extra Cargo capacity": (200, 250),
        "One-Time Fuel Drop Tanks": (200, 1000)
    }

    print("Available items:")
    for item, price in items.items():
        #Here we unpack the touples into two different variables.
        (moneyprice, CO2_price) = price
        print(f"{item}: {moneyprice}$, {CO2_price} CO2 tokens")
    selected_item = input("Enter the item you want to purchase: ")
    if selected_item not in items:
        print("Invalid item selection.")
        return False
    #We do that again.
    (moneyprice, CO2_price) = items[selected_item]
    if user.Money < moneyprice:
        print("You don't have enough money.")
        return False
    if user.CO2_Budget < CO2_price:
        print("Are you sure you want to go into negative CO2 budget?")
        UsInput = input("Yes/No ")
        if UsInput == "No":
            return False
    user.Money = user.Money - moneyprice
    user.CO2_Budget = user.CO2_Budget - CO2_price
    print(f"Purchase of {selected_item} successful. Your new balance: {user.Money}")
    update_player(cursor,user)
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
UsInput = int(input("Which choice would you like to pick?: "))
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
    print("1 - Move to a local airport ")
    print("2 - Move to an international airport ")
    print("3 - Pick up quests from the airport ")
    print("4 - Airport shop ")
    print("5 - Player stats ")
    print("6 - Log out. ")
    UsInput = int(input("Which choice would you like to pick?: "))
    if UsInput == 1:
        local_airport_fetcher(cursor,user.databaseID)
    elif UsInput == 2:
        InternationalAirportFetcher(cursor,user.databaseID)
    elif UsInput == 3:
        print("WIP")
    elif UsInput == 4:
        if Shop(user) == True:
            print("Purchase successful")
        else:
            print("Purchase failed")
    elif UsInput == 5:
        print("WIP")
    else:
        run = False
Goodbye()