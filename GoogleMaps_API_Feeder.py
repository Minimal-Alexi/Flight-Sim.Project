import time
from Player_Data import Player
from Database import getcountry,getcoordinates,get_local_airport_list,get_country_list,get_airport_list
from geopy import distance
import mysql.connector
#TestDummy = Player("TEST","EFHK","TEST","TEST",100,"TEST",10,"TEST","TEST","TEST")
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )
cursor = connection.cursor()
#These functions send over a JSON file with all the airports in range.
def Local_Airport_in_Range(user):
    country = getcountry(user.location)
    coords = getcoordinates(user.location)
    result = get_local_airport_list(country)
    response = {}
    counter = 1
    if user.BoughtFuelTank == True:
        max_distance = 250
    else:
        max_distance = 0
    max_distance = (max_distance + user.Fuel)*user.Fuel_Efficiency
    for i in result:
        if i[1] != user.location:
            dest_coords = (i[2], i[3])
            distance_coords = distance.distance(coords, dest_coords).km
            if distance_coords <= max_distance:
                item = {
                    "name": i[0],
                    "icao": i[1],
                    "distance": int(distance_coords),
                    "latitude_deg": i[2],
                    "longitude_deg": i[3]
                }
                response[f"Airport {counter}"] = item
                counter = counter + 1
    return response
#This function especially is ridiculously time intensive. I will look into ways to parallelize it. ~Min/Alex
#Paralleization is way too complex for me and for the project. Let's leave it like this. ~Min/Alex
def Intl_Airport_in_Range(user,target_continent):
    coords = getcoordinates(user.location)
    country_list = get_country_list(target_continent)
    response = {}
    counter = 1
    if user.BoughtFuelTank == True:
        max_distance = 250
    else:
        max_distance = 0
    max_distance = (max_distance + user.Fuel)*user.Fuel_Efficiency
    for i in country_list:
        country = i[0]
        result = get_airport_list(country,"large_airport")
        for j in result:
            if j[1] != user.location:
                dest_coords = (j[2], j[3])
                distance_coords = distance.distance(coords, dest_coords).km
                if distance_coords <= max_distance:
                    item = {
                        "name": j[0],
                        "icao": j[1],
                        "distance": distance_coords,
                        "latitude_deg": j[2],
                        "longitude_deg": j[3]
                    }
                    response[f"Airport {counter}"] = item
                    counter = counter + 1
    return response

"""
result = Intl_Airport_in_Range(TestDummy,"EU")
for i in result:
    print(i,result[i])
result = Local_Airport_in_Range(TestDummy)
for i in result:
    print(i,result[i])
    
"""