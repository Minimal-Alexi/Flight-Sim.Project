import mysql
import pygame
from InternationalAirportSelection import cli_get_airport_type_from_user

connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='',
         autocommit=True
         )

# Create a cursor for all interactions with the MariaDB Database
cursor = connection.cursor()

def LocalAirportFetcher():
    return True

def InternationalAirportFetcher(cursor):
    # This function will run a cli menu where the user selects an international airport
    cli_get_airport_type_from_user(cursor)

# After the algorithm fetches the airports, the player is asked if they want to select to go to one of the airports.
# If the player says no they get returned to the main menu, otherwise the flight game starts
def FlightGame():
    return True


class Player:
    location = "Placeholder"
    CO2_Budget = 10000
    Fuel = 100
    Money = 100
    Fuel_Efficiency = 5

run = False
print("1 - Would you like to register a new user?")
print("2 - Would you like to login as a user?")
print("3 - Quit")
UsInput = int(input("Which choice would you like to pick?"))
if UsInput==1:
    print("WIP")
    run = True
elif UsInput==2:
    print("WIP")
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
    print("5 - Log out. ")
    UsInput = int(input("Which choice would you like to pick?"))
    if UsInput == 1:
        print("WIP")
    elif UsInput == 2:
        InternationalAirportFetcher(cursor)
    elif UsInput == 3:
        print("WIP")
    elif UsInput == 4:
        print("WIP")
    else:
        run = False
print("Bye bye user!")
