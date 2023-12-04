from flask import Flask,request,render_template,Response,jsonify
from flask_cors import CORS
import json
from Authentication_Handling import UserReg,UserLogin
app = Flask(__name__)
CORS(app)
@app.route('/Authenticate', methods = ["GET","POST"])
def login():
    if request.is_json:
        try:
            json_user = request.get_json()
            username = json_user["username"]
            password = json_user["password"]
            signtype = json_user["signtype"]
            if signtype == 1:
                if UserReg(username,password) == True:
                    response = {
                        "message": "Account succesfully created!",
                        "status": 200,
                    }
                    status = 200
                else:
                    response = {
                        "message": "Invalid username info added. Username already exists",
                        "status": 400
                    }
                    status = 400
                return jsonify(response), status
            elif signtype == 2:
                if UserLogin(username,password) == True:
                    response = {
                        "message": "Account succesfully logged into!",
                        "status": 200
                    }
                    status = 200
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
    return render_template('Main Page.html')
if __name__ == "__main__":
    app.run(use_reloader=True,host="127.0.0.1", port=5000, debug = True)