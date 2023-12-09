let player_data = JSON.parse(sessionStorage.getItem('userData'))
const button1 = document.getElementById('item-1'),
    button2 = document.getElementById('item-2'),
    button3 = document.getElementById('item-3'),
    button4 = document.getElementById('item-4'),
    button5 = document.getElementById('item-5');
function RefuelPrices() {
    let Server_Request = new XMLHttpRequest();
    let json = JSON.stringify({
        "request_type":1,
        "databaseID":player_data['databaseID']
    })
    Server_Request.open("POST", "/Shop", true);
    Server_Request.setRequestHeader("Content-Type", "application/json");
    Server_Request.onreadystatechange = function () {
        if (Server_Request.readyState == XMLHttpRequest.DONE) {
            if (Server_Request.status == 200) {
                // Successful response from the server
                let response = JSON.parse(Server_Request.responseText);
                console.log(response);
                document.getElementById('Refuel$').textContent = response['Refuel$'];
                document.getElementById('RefuelCO2').textContent = response['RefuelCO2'];
                document.getElementById('Env-Refuel$').textContent = response['Env-Refuel$'];
                document.getElementById('Env-RefuelCO2').textContent = response['Env-RefuelCO2'];
            } else {
                // Error response from the server
                console.error("Error:", Server_Request.status, Server_Request.statusText);
            }
        }
    };
    Server_Request.send(json);
}

function BuyingItems(itemID)
{
    let Server_Request = new XMLHttpRequest();
    let json = JSON.stringify({
        "request_type":2,
        "databaseID":player_data['databaseID'],
        "itemID":itemID
    })
    Server_Request.open("POST", "/Shop", true);
    Server_Request.setRequestHeader("Content-Type", "application/json");
    Server_Request.onreadystatechange = function () {
        if (Server_Request.readyState == XMLHttpRequest.DONE) {
            if (Server_Request.status == 200) {
                // Successful response from the server
                let response = JSON.parse(Server_Request.responseText);
                console.log(response);
                if(response['status'] == 'Success')
                {
                    alert(response["message"])
                    sessionStorage.setItem('userData',JSON.stringify(response['user']));
                    console.log(JSON.parse(sessionStorage.getItem('userData')));
                }
            } else {
                // Error response from the server
                console.error("Error:", Server_Request.status, Server_Request.statusText);
            }
        }
    };
    Server_Request.send(json);
}





RefuelPrices()
button1.onclick = function()
{
    BuyingItems(1)
}
button2.onclick = function()
{
    BuyingItems(2)
}
button3.onclick = function()
{
    BuyingItems(3)
}
button4.onclick = function()
{
    BuyingItems(4)
}
button5.onclick = function()
{
    BuyingItems(5)
}