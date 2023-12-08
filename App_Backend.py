from flask import Flask,request,render_template,Response,jsonify
from flask_cors import CORS
import json
from Authentication_Handling import UserReg,UserLogin,UserList
from Player_Data import Player
from GoogleMaps_API_Feeder import Local_Airport_in_Range,Intl_Airport_in_Range
app = Flask(__name__)
CORS(app)
#There are a lot of printing functions in this app to ensure the console user understands how the app works.
#Who knew console printing could be this useful? ~Min/Alex
#The user variable isn't saved because it isn't stored globally. This list will save the users accessing the site.
user_list = []
#This function searches the user ID in the list
def user_search(user_ID):
    for i in user_list:
        if i.databaseID == user_ID:
            return i
    return None
@app.route('/Authenticate', methods = ["GET","POST"])
def login():
    if request.is_json:
        try:
            json_user = request.get_json()
            username = json_user["username"]
            password = json_user["password"]
            signtype = json_user["signtype"]
            #If signtype = 1 then it's a register request, otherwise it's login.
            if signtype == 1:
                result,user = UserReg(username,password)
                if result == True:
                    response = {
                        "message": "Account succesfully created!",
                        "status": 200,
                    }
                    # This next bit will send the JSON data over to the Main Page for printing.
                    response.update(user.get_JSON_data())
                    UserList(user,user_list)
                    status = 200
                else:
                    response = {
                        "message": "Invalid username info added. Username already exists",
                        "status": 400
                    }
                    status = 400
                return jsonify(response), status
            elif signtype == 2:
                result,user = UserLogin(username,password)
                if result == True:
                    response = {
                        "message": "Account succesfully logged into!",
                        "status": 200
                    }
                    status = 200
                    #This next bit will send the JSON data over to the Main Page for printing.
                    response.update(user.get_JSON_data())
                    UserList(user, user_list)
                else:
                    response = {
                        "message": "Invalid username info added. Wrong password or wrong username. Try again.",
                        "status": 400
                    }
                    status = 400
                return jsonify(response), status
        except ValueError:
            response ={
                    "message": "Invalid user info added",
                    "status": 400
                }
            status = 400
            return jsonify(response), status
    else:
        return render_template('Login Page.html')

@app.route('/Main', methods = ["GET","POST"])
def main():
    if request.is_json:
        try:
            json_request = request.get_json()
            user_ID = json_request['databaseID']
            user = user_search(user_ID)
            if user != None:
                # type request 1-2 means sending local/international airport data respectively. 3 means travelling somewhere.
                type_request = json_request['type_request']
                print(type_request)
                if type_request == 1:
                    print(f"Sent local airport list to user {user.username} ({user.databaseID})")
                    result = Local_Airport_in_Range(user)
                    print(result)
                    return jsonify(result,200)
                elif type_request == 2:
                    print(f"Sent international airport list to user {user.username} ({user.databaseID})")
                    result = Intl_Airport_in_Range(user,"EU")
                    print(result)
                    return jsonify(result,200)
                elif type_request == 3:
                    destination = json_request['location']
        except SystemExit:
            response ={
                    "message": "Client error",
                    "status": 503
                }
            status = 503
            return jsonify(response), status
    else:
        return render_template('Main Page.html')
if __name__ == "__main__":
    app.run(use_reloader=True,host="127.0.0.1", port=5000, debug = True)