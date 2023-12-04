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
        let xhr = new XMLHttpRequest();
        const username = document.getElementById("username").value,password = document.getElementById("password").value;
        let json = JSON.stringify({
            "username":username,
            "password":password,
            "signtype":signtype
        })
        // The stuff we do here is so that the Python app receives the data from the website. Look at it, it's beautiful!!!!!!!!
    xhr.open("POST", "/Authenticate", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(json);
    // This should probably be our template for receiving requests from the server, please read it carefully.
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200) {
                // Successful response from the server
                let response = JSON.parse(xhr.responseText);
                console.log(response);
                // Handle the response as needed
            } else {
                // Error response from the server
                console.error("Error:", xhr.status, xhr.responseText);
                // Handle the error as needed
            }
        }
    };

    xhr.send(json);
}