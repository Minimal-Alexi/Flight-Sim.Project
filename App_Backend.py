from flask import Flask,request,render_template,Response,jsonify
from flask_cors import CORS
import json
from Authentication_Handling import UserReg,UserLogin
from Player_Data import Player
app = Flask(__name__)
CORS(app)
#There are a lot of printing functions in this app to ensure the console user understands how the app works.
#Who knew console printing could be this useful? ~Min/Alex
@app.route('/Authenticate', methods = ["GET","POST"])
def login():
    if request.is_json:
        try:
            json_user = request.get_json()
            username = json_user["username"]
            password = json_user["password"]
            signtype = json_user["signtype"]
            if signtype == 1:
                result,user = UserReg(username,password)
                if result == True:
                    response = {
                        "message": "Account succesfully created!",
                        "status": 200,
                    }
                    # This next bit will send the JSON data over to the Main Page for printing.
                    response.update(user.get_JSON_data())
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

    return render_template('Login Page.html')

@app.route('/Main', methods = ["GET","POST"])
def main():
    if request.is_json:
        pass
    return render_template('Main Page.html')
if __name__ == "__main__":
    app.run(use_reloader=True,host="127.0.0.1", port=5000, debug = True)