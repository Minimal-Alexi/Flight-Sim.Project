import mysql.connector
from Database import ( update_player,get_country_from_ident,checklarge)
from mainmenu_functions import (UserLog,UserReg,Goodbye,getairport,local_airport_fetcher,InternationalAirportFetcher,
                                NewUser,check_end_goal,Win)
from Player import Player
from Quest import QuestMenu
from display_functions import player_status
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
def Shop(user):
    print(f"Your current balance: {user.Money}$")
    print(f"Your current CO2 budget: {user.CO2_Budget}")
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
        quantity = int(input(f"Insert the quantity of the item you want to purchase. (Max fuel efficiency is 50, you have {user.Fuel_Efficiency}) "))
        if user.Fuel_Efficiency==50 or quantity*5+user.Fuel_Efficiency>50:
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
        user.BoughtExtraCash = True
    elif selected_item == "One-Time Fuel Drop Tanks":
        user.BoughtFuelTank = True
    else:
        user.Fuel = user.Fuel+Refuel

    user.Money = user.Money - moneyprice*quantity
    user.CO2_Budget = user.CO2_Budget - CO2_price*quantity
    print(f"Purchase of {selected_item} successful. Your new balance: {user.Money}. You have {user.CO2_Budget} carbon credits left.")
    stop = input()
    update_player(cursor,user)
    return True


user = Player()


run = False
print("1 - Would you like to register a new user?")
print("2 - Would you like to login as a user?")
print("3 - Quit")
UsInput = int(input("Which choice would you like to pick?: "))
if UsInput==1:
    UsInput = input("Enter in new username: ")
    UserReg(UsInput)
    if NewUser()==True:
        run = True
        stop = input("Press any key to continue...")
        UserLog(user, UsInput)
elif UsInput==2:
    UsInput = input("Enter in your username: ")
    UserLog(user, UsInput)
    run = True
else:
    run = False
move = True
while run == True:
    #The program will have to remind the player what airport they are located in:
    if move == False:
        print(f"You are at {getairport(user.location)[0]} ({get_country_from_ident(user.location,cursor)[0]})")
    print("1 - Move to a local airport ")
    print("2 - Move to an international airport ")
    print("3 - Pick up quests from the airport ")
    print("4 - Airport shop ")
    print("5 - Player stats ")
    print("6 - Log out. ")
    UsInput = int(input("Which choice would you like to pick?: "))
    if UsInput == 1:
        local_airport_fetcher(cursor, user.databaseID, user)
        move = True
        update_player(cursor,user)
        if check_end_goal(user.location) == True:
            run = False
            Win(user)
    elif UsInput == 2:
        if checklarge(cursor,user.location) == True:
            InternationalAirportFetcher(cursor,user.databaseID,user)
            move = True
            update_player(cursor, user)
            if check_end_goal(user.location) == True:
                run = False
                Win(user)
        else:
            print("You are not at a large airport, you can't travel internationally!")
            move = False
    elif UsInput == 3:
        QuestMenu(user,cursor)
        move = False
        update_player(cursor, user)
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
        if user.BoughtFuelTank == True or user.BoughtExtraCash == True:
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