from flask import Flask,request,render_template,Response
import json
from Authentication_Handling import UserReg
app = Flask(__name__)
@app.route('/LogIn', methods = ["GET","POST"])
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
                        "status": 200
                    }
                else:
                    response = {
                        "message": "Invalid username info added. Username already exists",
                        "status": 400
                    }
                json_response = json.dumps(response)
                http_response = Response(response=json_response, status=400, mimetype="application/json")
                return http_response
        except ValueError:
            response ={
                    "message": "Invalid username info added",
                    "status": 400
                }
            json_response = json.dumps(response)
            http_response = Response(response=json_response, status=400, mimetype="application/json")
            return http_response

    return render_template('Login Page.html')

if __name__ == "__main__":
    app.run(use_reloader=True,host="127.0.0.1", port=5000, debug = True)