import mysql.connector
import pygame
from Database import (get_continent, get_continent_list, get_airport_list,
                      get_airport_type_list, get_country_list, get_user_location, set_user_location)

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
def FlightGame():
    return True


class Player:
    location = None
    CO2_Budget = 10000
    Fuel = 100
    Money = 100
print("1 - Would you like to register a new user?")
print("2 - Would you like to login as a user?")
print("3 - Quit")
run = True
while run == True:
    #The program will have to remind the player what airport they are located in:
    #Or if they crashed
    print("1 - What local airports are available?")
    print("2 - What international airports are available?")
    UsInput = int(input("Which choice would you like to pick?"))
    if UsInput == 1:
        print("WIP")
    elif UsInput == 2:
        InternationalAirportFetcher(cursor)
