from Database import get_continent
from geopy import distance
from Database import getcoordinates

# Takes a list and displays as numbered menu
def display_menu_list(disp_list):
    counter = 1
    for x in disp_list:
        print(f"{counter}. {x[0]}")
        counter += 1
    print("Press 0 to go back to the main menu.")
def display_airport(disp_list,user,cursor):
    counter = 1
    disp_list.sort()
    for x in disp_list:
        print(f"{counter}. {x[0]} ({int(distance.distance((x[2],x[3]),getcoordinates(cursor,user.location)).km)} kms away)")
        counter += 1
    print("Press 0 to go back to the main menu.")
def display_continent_list(continents):
    counter = 1
    for x in continents:
        print(f"{counter}. {get_continent(x[0])}")
        counter += 1
    print("Press 0 to go back to the main menu.")


def player_status(user):
    print(f"Current Player Stats:")
    print(f"Fuel Efficiency: {user.Fuel_Efficiency} km/liters")
    print(f"Fuel: {user.Fuel} liters")
    print(f"Money: {user.Money}$")
    print(f"CO2 Budget: {user.CO2_Budget} credits")
    stop = input()