
        let Server_Request = new XMLHttpRequest();
        // The stuff we do here is so that the Python app receives the data from the website. Look at it, it's beautiful!!!!!!!! ~Min/Alex
        //You will need to form a json file here and to send it, for example:
        /*
                const username = document.getElementById("username").value,password = document.getElementById("password").value;
        let json = JSON.stringify({
            "username":username,
            "password":password,
            "signtype":signtype
        })
        make sure to use JSON.stringify
         */
    Server_Request.open("POST", "/Authenticate", true);
    Server_Request.setRequestHeader("Content-Type", "application/json");
        // This should receive data from the server...half the time it works, other half it doesn't. Try refreshing the page, re-entering/exiting. ~Min/Alex
        // I assume it's a cache issue? Could also be that the version of your webpage is older compared to the active one. ~Min/Alex
    Server_Request.onreadystatechange = function() {
        if (Server_Request.readyState == XMLHttpRequest.DONE) {
            if (Server_Request.status == 200) {
                // Successful response from the server
                let response = JSON.parse(Server_Request.responseText);
                console.log(response);
                // Handle the response as needed
            } else {
                // Error response from the server
                console.error("Error:", Server_Request.status, Server_Request.statusText);
                // Handle the error as needed
            }
        }
    };
    //This sends the JSON over,replace with apropiate variable
    Server_Request.send();