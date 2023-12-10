# All MariaDB interactions go here
#Why the fuck, do we not do the cursor stuff in this folder? ~Min/Alex
import mysql.connector
from mysql.connector import errorcode
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True,
         connection_timeout= 60
         )
# takes sql text for query and cursor and returns result of query ~Ashifa

# For any evaluator concerned. I am getting a really stupid error that seems to be innate to MariaDB.
# The connector sometimes just fails to reset itself and to move on to the next DB Query.
# Yes, this was made with the help of StackOverflow, ChatGPT, and some of my friends. It was an effort that took at least 10 hours total to fix up.
# Fuck this.


def db_query(sql):
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        if err.errno == errorcode.CR_SERVER_LOST or err.errno == errorcode.CR_CONN_HOST_ERROR:
            print("Lost connection. Reconnecting...")
            connection.reconnect(attempts=10, delay=50)  # Adjust the number of attempts and delay as needed
            return db_query(sql)  # Retry the query after reconnecting
        else:
            raise
    finally:
        # Make sure to close the cursor to avoid "Unread result found" errors
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

# Deprecated: moved to method of Player to keep class and DB in sync
# def set_user_location(location, id, cursor):
#     cursor.execute(f"update game set location = '{location}' where id = '{id}'")


# gets user location from the db ~Ashifa
def get_user_location(id):
    return db_query(f"select game.location, airport.name "
                    f"from game, airport "
                    f"where game.id= '{id}'"
                    f"and game.location = airport.ident")[0]


# gets user local airport from db ~Ashifa
def get_local_airport(id):
    return db_query(f"SELECT NAME "
                    f"FROM AIRPORT "
                    f"WHERE ISO_COUNTRY "
                    f"IN (SELECT ISO_COUNTRY FROM AIRPORT, GAME "
                    f"WHERE GAME.LOCATION = AIRPORT.IDENT AND GAME.ID = {id} AND )")

def get_country_from_ident(ident):
    return db_query(f"select country.iso_country, country.name "
                    f"from country, airport "
                    f"where country.iso_country = airport.iso_country "
                    f"and airport.ident = '{ident}'")[0]

def get_airport_name_from_ident(ident):
    return db_query(f"SELECT name "
                    f"FROM airport "
                    f"WHERE ident = '{ident}'")[0][0]

# takes continent code as a string and returns the full name of the continent ~Ashifa
def get_continent(continent_code):
    continents = {"EU": "Europe",
                  "AS": "Asia",
                  "NA": "North America",
                  "AF": "Africa",
                  "AN": "Antarctica",
                  "SA": "South America",
                  'OC': "Australia"}
    return continents[continent_code]


# Gets continent list from the db ~Ashifa
def get_continent_list():
    return db_query("select distinct continent from airport")


# Takes continent code and returns list of countries in that continent ~Ashifa
def get_country_list(continent):
    return db_query(f"select distinct country.name "
                    f"from country, airport "
                    f"where country.continent = '{continent}'"
                    f"and country.iso_country = airport.iso_country "
                    f"and (airport.type = 'medium_airport' or airport.type =  'large airport')"
                    f"ORDER BY COUNTRY.NAME")


# Takes country name and returns list of distinct airport types ~Ashifa
def get_intl_airport_type_list(country):
    return db_query(f"select distinct type "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}'"
                    f"and type = 'large_airport'")

# Takes country name and returns list of distinct airport types ~Ashifa
def get_local_airport_type_list(country):
    return db_query(f"select distinct type "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}'"
                    f"and (type = 'medium_airport' or type = 'large_airport')")

def get_airport_list(country, airport_type):
    return db_query(f"select airport.name, airport.ident,airport.LATITUDE_DEG,airport.LONGITUDE_DEG "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}' "
                    f"and airport.type = '{airport_type}' "
                    f"ORDER BY airport.name")

def get_local_airport_list(country):
    return db_query(f"select airport.name, airport.ident,airport.LATITUDE_DEG,airport.LONGITUDE_DEG "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}'"
                    f"and (airport.type = 'medium_airport' or airport.type = 'large_airport')"
                    f"ORDER BY airport.name")



#This function updates all the players current stats and positions to the database, extremely useful. We should post it up everywhere. ~Ashifa
def update_player(user):
    sql = f"UPDATE GAME SET CO2_BUDGET = {user.CO2_Budget}, MONEY = {user.Money}, LOCATION = '{user.location}', FUEL = {user.Fuel}, FUEL_EFFICIENCY = {user.Fuel_Efficiency} WHERE {user.databaseID} = ID"
    db_query(sql)
def getairport(IDENT):
    name = (db_query(f"SELECT NAME FROM AIRPORT WHERE IDENT = '{IDENT}'"))[0]
    return name
def getcountry(name):
    country = db_query(f"SELECT COUNTRY.NAME FROM AIRPORT,COUNTRY WHERE AIRPORT.IDENT = '{name}' AND AIRPORT.ISO_COUNTRY = COUNTRY.ISO_COUNTRY")[0][0]
    return country
def getcoordinates(ident):
    result = db_query(f"SELECT LATITUDE_DEG, LONGITUDE_DEG FROM AIRPORT WHERE IDENT = '{ident}'")
    result = result[0]
    return result
def checklarge(ident):
    (result, )= db_query(f"SELECT TYPE FROM AIRPORT WHERE IDENT = '{ident}'")[0]
    if result == "large_airport":
        return True
    return False