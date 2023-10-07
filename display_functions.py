from Database import get_continent
# Takes a list and displays as numbered menu
def display_menu_list(disp_list):
    counter = 1
    for x in disp_list:
        print(f"{counter}. {x[0]}")
        counter += 1
def display_country_list(disp_list):
    counter = 1
    for x in disp_list:
        print(f"{counter}. {x[0]}")
        counter += 1
def display_continent_list(continents):
    counter = 1
    for x in continents:
        print(f"{counter}. {get_continent(x[0])}")
        counter += 1