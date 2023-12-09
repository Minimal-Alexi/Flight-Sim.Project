let player_data = JSON.parse(sessionStorage.getItem('userData'))
function fetchquest(quest)
{
    let Server_Request = new XMLHttpRequest();
    let json = JSON.stringify({
        "databaseID":player_data['databaseID'],
        "questID":quest
    })
    console.log(json);
    Server_Request.open("POST", "/Quest", true);
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
                    player_data = JSON.parse(sessionStorage.getItem('userData'))
                    console.log(JSON.parse(sessionStorage.getItem('userData')));
                }
                else
                {
                    alert(response["message"])
                }
            } else {
                // Error response from the server
                console.error("Error:", Server_Request.status, Server_Request.statusText);
            }
        }
    };
    Server_Request.send(json);
}
const button1 = document.getElementById('quest1'),button2 = document.getElementById('quest2'),button3 = document.getElementById('quest3');
button1.onclick = function()
{
    fetchquest(1);
}
button2.onclick = function()
{
    fetchquest(2);
}
button3.onclick = function()
{
    fetchquest(3);
}

let quests = player_data["Quest"]