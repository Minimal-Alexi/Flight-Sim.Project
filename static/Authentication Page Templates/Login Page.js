let signupBtn = document.getElementById("signupBtn")
let signinBtn = document.getElementById("signinBtn")
let nameField = document.getElementById("nameField")
let submitBtn = document.getElementById("submit")
let title = document.getElementById("title")
let signtype = 1;

signinBtn.onclick = function(){
    nameField.style.maxHeight = "60px";
    title.innerHTML = "EcoFLY - Sign In";
    signupBtn.classList.add("disable")
    signinBtn.classList.remove("disable")
    signtype = 2;
}

signupBtn.onclick = function(){
    nameField.style.maxHeight = "60px";
    title.innerHTML = "EcoFLY - Sign Up";
    signupBtn.classList.add("disable")
    signinBtn.classList.remove("disable")
    signtype = 1;
}

submitBtn.onclick = function()
{
        let Server_Request = new XMLHttpRequest();
        const username = document.getElementById("username").value,password = document.getElementById("password").value;
        let json = JSON.stringify({
            "username":username,
            "password":password,
            "signtype":signtype
        })
        // The stuff we do here is so that the Python app receives the data from the website. Look at it, it's beautiful!!!!!!!!
    Server_Request.open("POST", "/Authenticate", true);
    Server_Request.setRequestHeader("Content-Type", "application/json");
    console.log(json);
        // This should receive data from the server...half the time it works, other half it doesn't. Try refreshing the page, re-entering/exiting.
        // I assume it's a cache issue?
    Server_Request.onreadystatechange = function() {
        if (Server_Request.readyState == XMLHttpRequest.DONE) {
            if (Server_Request.status == 200) {
                // Successful response from the server
                let response = JSON.parse(Server_Request.responseText);
                console.log(response);
                // Handle the response as needed
                sessionStorage.setItem('userData',JSON.stringify(response));
                window.location.href = '/Main';
            } else {
                // Error response from the server
                console.error("Error:", Server_Request.status, Server_Request.statusText);
                // Handle the error as needed
            }
        }
    };

    Server_Request.send(json);
}