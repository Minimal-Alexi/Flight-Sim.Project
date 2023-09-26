import mysql.connector


# takes sql text for query and cursor and returns result of query
def db_query(sql, cursor):
    cursor.execute(sql)
    return cursor.fetchall()


# prints contents of list in new line
def display_list(print_list):
    for x in print_list:
        print(x)


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
    return db_query(f"select airport.name "
                    f"from airport, country "
                    f"where airport.iso_country = country.iso_country "
                    f"and country.name = '{country}' "
                    f"and airport.type = '{airport_type}'", cursor)


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


def cli_get_airport_type_from_user(cursor):

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

    print(f"\nUser has selected {airport_sel}")

