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
        xhr.open("POST","/Authenticate",true);
        xhr.setRequestHeader("Content-Type", "application/json");
        console.log(json);
        xhr.send(json);
}
fetch('http://localhost:5000/Authenticate')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });