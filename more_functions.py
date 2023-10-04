import mysql
from Database import get_user_location, get_continent, get_airport_type_list, get_airport_list, set_user_location, get_country_from_ident,db_query
from geopy import distance
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )
cursor = connection.cursor()
# Takes a list and displays as numbered menu
def display_menu_list(disp_list):
    counter = 1
    for x in disp_list:
        print(f"{counter}. {x[0]}")
        counter += 1
def display_country_limit_list(disp_list,user):
    counter = 1
    playercords = db_query(f"select LATITUDE_DEG, LONGITUDE_DEG from AIRPORT where IDENT = '{user.location}';", cursor)[0]
    for x in disp_list:
        if distance.distance(playercords, (x[2], x[3])) <= 500:
            print(f"{counter}. {x[0]}")
            counter += 1
def display_continent_list(continents):
    counter = 1
    for x in continents:
        print(f"{counter}. {get_continent(x[0])}")
        counter += 1


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