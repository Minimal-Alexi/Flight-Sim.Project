import time
from flask import jsonify
from Player_Data import Player
from Database import getcountry,getcoordinates,get_local_airport_list
from geopy import distance
import mysql.connector
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )
cursor = connection.cursor()
def Local_Airport_in_Range(user = Player("TEST","EFHK","TEST","TEST",100,"TEST",10,"TEST","TEST","TEST")):
    country = getcountry(cursor,user.location)
    coords=getcoordinates(cursor,user.location)
    result = get_local_airport_list(cursor,country)
    response = {}
    counter = 1
    for i in result:
        dest_coords = (i[2],i[3])
        distance_coords = distance.distance(coords,dest_coords).km
        if distance_coords <= user.Fuel*user.Fuel_Efficiency:
            item = {
                "name":i[0],
                "icao":i[1],
                "distance":distance_coords,
                "latitude_deg":i[2],
                "longitude_deg":i[3]
            }
            response[f"Airport {counter}"]=item
            counter = counter + 1
    return response

Local_Airport_in_Range()