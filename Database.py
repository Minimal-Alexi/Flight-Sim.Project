# All MariaDB interactions go here

# takes sql text for query and cursor and returns result of query
def db_query(sql, cursor):
    cursor.execute(sql)
    return cursor.fetchall()

# Deprecated: moved to method of Player to keep class and DB in sync
# def set_user_location(location, id, cursor):
#     cursor.execute(f"update game set location = '{location}' where id = '{id}'")


# gets user location from the db
def get_user_location(id, cursor):
    return db_query(f"select game.location, airport.name "
                    f"from game, airport "
                    f"where game.id= '{id}'"
                    f"and game.location = airport.ident", cursor)[0]


# gets user local airport from db
def get_local_airport(id, cursor):
    return db_query(f"SELECT NAME "
                    f"FROM AIRPORT "
                    f"WHERE ISO_COUNTRY "
                    f"IN (SELECT ISO_COUNTRY FROM AIRPORT, GAME "
                    f"WHERE GAME.LOCATION = AIRPORT.IDENT AND GAME.ID = {id} AND )", cursor)

def get_country_from_ident(ident, cursor):
    return db_query(f"select country.iso_country, country.name "
                    f"from country, airport "
                    f"where country.iso_country = airport.iso_country "
                    f"and airport.ident = '{ident}'", cursor)[0]

def get_airport_name_from_ident(ident, cursor):
    return db_query(f"SELECT name "
                    f"FROM airport "
                    f"WHERE ident = '{ident}'", cursor)[0][0]

# takes continent code as a string and returns the full name of the continent
def get_continent(continent_code):
    continents = {"EU": "Europe",
                  "AS": "Asia",
                  "NA": "North America",
                  "AF": "Africa",
                  "AN": "Antarctica",
                  "SA": "South America",
                  'OC': "Australia"}
    return continents[continent_code]


# Gets continent list from the db
def get_continent_list(cursor):
    return db_query("select distinct continent from airport", cursor)


# Takes continent code and returns list of countries in that continent
def get_country_list(cursor, continent):
    return db_query(f"select distinct country.name "
                    f"from country, airport "
                    f"where country.continent = '{continent}'"
                    f"and country.iso_country = airport.iso_country "
                    f"and (airport.type = 'medium_airport' or airport.type =  'large airport')"
                    f"ORDER BY COUNTRY.NAME", cursor)


# Takes country name and returns list of distinct airport types
def get_intl_airport_type_list(cursor, country):
    return db_query(f"select distinct type "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}'"
                    f"and type = 'large_airport'", cursor)

# Takes country name and returns list of distinct airport types
def get_local_airport_type_list(cursor, country):
    return db_query(f"select distinct type "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}'"
                    f"and (type = 'medium_airport' or type = 'large_airport')", cursor)

def get_airport_list(cursor, country, airport_type):
    return db_query(f"select airport.name, airport.ident,airport.LATITUDE_DEG,airport.LONGITUDE_DEG "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}' "
                    f"and airport.type = '{airport_type}'"
                    f"ORDER BY airport.name", cursor)


#This function updates all the players current stats and positions to the database, extremely useful. We should post it up everywhere.
def update_player(cursor,user):
    sql = f"UPDATE GAME SET CO2_BUDGET = {user.CO2_Budget}, MONEY = {user.Money}, LOCATION = '{user.location}', FUEL = {user.Fuel}, FUEL_EFFICIENCY = {user.Fuel_Efficiency} WHERE {user.databaseID} = ID"
    db_query(sql,cursor)
def getairport(IDENT,cursor):
    name = (db_query(f"SELECT NAME FROM AIRPORT WHERE IDENT = '{IDENT}'",cursor))[0]
    return name
def getcountry(cursor,name):
    country = db_query(f"SELECT COUNTRY.NAME FROM AIRPORT,COUNTRY WHERE AIRPORT.IDENT = '{name}' AND AIRPORT.ISO_COUNTRY = COUNTRY.ISO_COUNTRY",cursor)[0]
    return country
def getcoordinates(cursor,ident):
    return db_query(f"SELECT LATITUDE_DEG, LONGITUDE_DEG FROM AIRPORT WHERE IDENT = '{ident}'",cursor)
def checklarge(cursor,ident):
    (result, )= db_query(f"SELECT TYPE FROM AIRPORT WHERE IDENT = '{ident}'",cursor)[0]
    if result == "large_airport":
        return True
    return False
