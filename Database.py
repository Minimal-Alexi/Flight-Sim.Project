# All MariaDB interactions go here

# takes sql text for query and cursor and returns result of query
def db_query(sql, cursor):
    cursor.execute(sql)
    return cursor.fetchall()


# prints contents of list in new line
def display_list(print_list):
    for x in print_list:
        print(x)


# sends user location to the db
def set_user_location(location, id, cursor):
    cursor.execute(f"update game set location = '{location}' where id = '{id}'")


# gets user location from the db
def get_user_location(id, cursor):
    return db_query(f"select game.location, airport.name "
                    f"from game, airport "
                    f"where game.id= '{id}'"
                    f"and game.location = airport.ident", cursor)[0]


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


# Takes
def get_continent_list(cursor):
    return db_query("select distinct continent from airport", cursor)


# Takes continent code and returns list of countries in that continent
def get_country_list(cursor, continent):
    return db_query(f"select distinct name from country where continent = '{continent}'", cursor)


# Takes country name and returns list of distinct airport types
def get_airport_type_list(cursor, country):
    return db_query(f"select distinct type "
                    f"from airport, country where airport.iso_country = country.iso_country and country.name = '{country}'", cursor)


def get_airport_list(cursor, country, airport_type):
    return db_query(f"select airport.name, airport.ident "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}' "
                    f"and airport.type = '{airport_type}'", cursor)

