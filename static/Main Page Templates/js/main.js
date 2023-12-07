let Player_Pos_Marker, player_data = JSON.parse(sessionStorage.getItem('userData')), distance_circle;
const LocalAirportButton = document.getElementById("Local Airports Filter"),
    InternationalAirportButton = document.getElementById("International Airports Filter");

function initMap() {
    let user_location = player_data['location_coords'];
    user_location = new google.maps.LatLng(user_location[0], user_location[1]);
    console.log(user_location)
    let mapProp = {
        center: user_location,
        zoom: 5,
    };
    let map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    Player_Pos_Marker = new google.maps.Marker({
        position: user_location,
        map,
        title: "Player position",
        fullcolor: "Blue"
    });
    distance_circle =
        {
            strokeColor: '#007BFF', // Color of the circle border
            strokeOpacity: 0.8,      // Opacity of the circle border
            strokeWeight: 2,         // Thickness of the circle border
            fillColor: '#007BFF',   // Fill color of the circle
            fillOpacity: 0.3,        // Opacity of the circle fill
            map: map,                // Assuming 'map' is your Google Map instance
            center: user_location, // Center the circle on the player's position
            radius: player_data['Fuel'] * player_data['Fuel_Efficiency'] * 1000
        };
    distance_circle = new google.maps.Circle(distance_circle);
    let infoWindow = new google.maps.InfoWindow({
        content: "You are currently at this position." + " " + player_data['location_name'] + " (" + player_data['location_icao'] + ")"
    });
    Player_Pos_Marker.addListener('click', function () {
        infoWindow.open(map, Player_Pos_Marker);
    });
    /*
    AirportFetcher(1)
    AirportFetcher(2)
     */
}
//Type 1 is local, type 2 is local.
function AirportFetcher(type)
{
    let Server_Request = new XMLHttpRequest();
    let Json = JSON.stringify(
        {
            databaseID:player_data['databaseID'],
            type_request:type,
        })
    Server_Request.open("POST", "/Main", true);
    Server_Request.setRequestHeader("Content-Type", "application/json");
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
    Server_Request.send(Json);
}

initMap()
document.getElementById("username").textContent = player_data['username'];
document.getElementById("currentlocation").textContent = player_data['location_name'] + "(" + player_data['location_icao'] + ")";
document.getElementById("budget").textContent = player_data['CO2_Budget'];
document.getElementById("fuel").textContent = player_data['Fuel'];
document.getElementById("money").textContent = player_data['Money'];

LocalAirportButton.onclick = function()
{
        AirportFetcher(1);
}
