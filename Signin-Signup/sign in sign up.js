let signupBtn = document.getElementById("signupBtn")
let signinBtn = document.getElementById("signinBtn")
let nameField = document.getElementById("nameField")
let title = document.getElementById("title")

signinBtn.onclick = function(){
    nameField.style.maxHeight = "0";
    title.innerHTML = "EcoFLY - Sign In";
    signupBtn.classList.add("disable")
    signinBtn.classList.remove("disable")
}

signupBtn.onclick = function(){
    nameField.style.maxHeight = "60px";
    title.innerHTML = "EcoFLY - Sign Up";
    signupBtn.classList.add("disable")
    signinBtn.classList.remove("disable")
}
