import mysql
import pygame
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='root',
         password='',
         autocommit=True
         )
def LocalAirportFetcher():
    return True
def InternationalAirportFetcher():
    #for simplicity sake, all large airports are treated as large
    return True
# After the algorithm fetches the airports, the player is asked if they want to select to go to one of the airports.
# If the player says no they get returned to the main menu, otherwise the flight game starts
def FlightGame():
    return True

run = True
while run == True:
    #The program will have to remind the player what airport they are located in:
    #Or if they crashed
    Print("1 - What local airports are available?")
    Print("2 - What international airports are available?")
    UsInput = int(input("Which choice would you like to pick?"))