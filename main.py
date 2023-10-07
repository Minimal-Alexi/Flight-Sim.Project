import mysql.connector
from Database import (get_continent, get_continent_list, get_airport_list,
                      get_airport_type_list, get_country_list, get_user_location, set_user_location, update_player,get_country_from_ident)
from mainmenu_functions import (UserLog,UserReg,Goodbye,player_status,getairport,local_airport_fetcher,InternationalAirportFetcher,NewUser)
connection = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='flight_game',
         user='flight_sim',
         password='menudb',
         autocommit=True
         )

# Create a cursor for all interactions with the MariaDB Database
cursor = connection.cursor()

#These are global variables, they can be edited in any function. This will be important for later.
BoughtFuelTank = False
BoughtExtraCash = False
def Shop(user):
    print(f"Your current balance: {user.Money}$")
    print(f"Your current CO2 budget: {user.CO2_Budget}")
    print(f"Your current CO2 budget: {user.Fuel}")
    Refuel = 100 - user.Fuel
    #All items have a money and CO2 price
    items = {
        "+5km/l Fuel Efficiency": (1000,100),
        "Refueling Services": (Refuel*10,Refuel*10+500),
        "Environmental-Friendly Refueling Services": (Refuel * 10 + 500, Refuel * 10),
        "One-Time Extra Cargo capacity": (200, 250),
        "One-Time Fuel Drop Tanks": (200, 1000)
    }
    print("Available items:")
    for item, price in items.items():
        #Here we unpack the touples into two different variables.
        (moneyprice, CO2_price) = price
        print(f"{item}: {moneyprice}$, {CO2_price} CO2 tokens")
    selected_item = input("Enter the item you want to purchase: ")
    if selected_item not in items:
        print("Invalid item selection.")
        return False
    #We do that again.
    (moneyprice, CO2_price) = items[selected_item]
    quantity = 1;
    if selected_item == "+5km/l Fuel Efficiency":
        quantity = int(input("Insert the quantity of the item you want to purchase. (Max fuel efficiency is 20) "))
        if user.Fuel_Efficiency==20 or quantity*5+user.Fuel_Efficiency>20:
            return False
    if user.Money < moneyprice*quantity:
        print("You don't have enough money.")
        return False
    if user.CO2_Budget < CO2_price*quantity:
        print("Are you sure you want to go into negative CO2 budget?")
        UsInput = input("Yes/No ")
        if UsInput == "No":
            return False
    if selected_item == "+5km/l Fuel Efficiency":
        user.Fuel_Efficiency = user.Fuel_Efficiency+5*quantity
    elif selected_item == "One-Time Extra Cargo capacity":
        BoughtExtraCash = True
    else:
        BoughtFuelTank = True
    user.Money = user.Money - moneyprice*quantity
    user.CO2_Budget = user.CO2_Budget - CO2_price*quantity
    print(f"Purchase of {selected_item} successful. Your new balance: {user.Money}. You have {user.CO2_Budget} carbon credits left.")
    stop = input()
    update_player(cursor,user)
    return True
class Player:
    databaseID = 0
    location = "Placeholder"
    CO2_Budget = 10000
    Fuel = 100
    Money = 100
    Fuel_Efficiency = 5
user = Player
run = False
print("1 - Would you like to register a new user?")
print("2 - Would you like to login as a user?")
print("3 - Quit")
UsInput = int(input("Which choice would you like to pick?: "))
if UsInput==1:
    UsInput = input("Enter in new username: ")
    UserReg(UsInput)
    UserLog(user,UsInput)
    if NewUser()==True:
        run = True
        stop = input("Press any key to continue...")
elif UsInput==2:
    UsInput = input("Enter in your username: ")
    UserLog(user, UsInput)
    run = True
else:
    run = False
move = True
while run == True:
    #The program will have to remind the player what airport they are located in:
    #if move == False:
        #print(f"You are at {getairport(user.location)[0]} ({get_country_from_ident(getairport(user.location),cursor)[0]})")
    print("1 - Move to a local airport ")
    print("2 - Move to an international airport ")
    print("3 - Pick up quests from the airport ")
    print("4 - Airport shop ")
    print("5 - Player stats ")
    print("6 - Log out. ")
    UsInput = int(input("Which choice would you like to pick?: "))
    if UsInput == 1:
        user.Fuel = 100
        local_airport_fetcher(cursor,user.databaseID,user)
        move = True
        update_player(cursor,user)
    elif UsInput == 2:
        InternationalAirportFetcher(cursor,user.databaseID,user)
        move = True
        update_player(cursor, user)
    elif UsInput == 3:
        print("WIP")
        move = False
    elif UsInput == 4:
        if Shop(user) == True:
            print("Purchase successful")
            move = False
        else:
            print("Purchase failed")
            move = False
            stop = input()
    elif UsInput == 5:
        player_status(user)
        move = False
    elif UsInput == 6:
        if BoughtFuelTank == True or BoughtExtraCash == True:
            print("Beware, if you leave you loose your one-time purchases and quests!")
            confirm = int(input("Are you sure you want to leave, type 6 again if so."))
            if confirm == 6:
                run = False
        run = False
    else:
        print("Not available, please try again")
        stop = input("Press any key to continue...")
        move = False
Goodbye()