let map;
let Player_Pos_Marker, player_data = JSON.parse(sessionStorage.getItem('userData')), distance_circle,Marker_List = [];
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
    map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    Player_Pos_Marker = new google.maps.Marker({
        position: user_location,
        map,
        title: "Player position",
        icon: {
            url: 'static/Main Page Templates/img/Player.bmp', // Replace with the path to your custom icon
            scaledSize: new google.maps.Size(50, 50), // Set the initial size of the icon
        }
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
}
//Type 1 is local, type 2 is local.
function CheckAirport(Type)
{
    if(Type == "Local_Airports" && sessionStorage.getItem(Type) != null)
    {
        console.log(sessionStorage.getItem(Type));
        return true;
    }
    else if(Type == "Intl_Airports" && sessionStorage.getItem(Type) != null)
    {
        console.log(sessionStorage.getItem(Type));
        return true;
    }
    return false;
}
function AirportFetcher(type) {
    return new Promise((resolve, reject) => {
        let Server_Request = new XMLHttpRequest();
        let Json = JSON.stringify({
            databaseID: player_data['databaseID'],
            type_request: type,
        });
        Server_Request.open("POST", "/Main", true);
        Server_Request.setRequestHeader("Content-Type", "application/json");
        Server_Request.onreadystatechange = function () {
            if (Server_Request.readyState == XMLHttpRequest.DONE) {
                if (Server_Request.status == 200) {
                    let response = JSON.parse(Server_Request.responseText);
                    console.log(response);
                    if (type == 1) {
                        sessionStorage.setItem('Local_Airports', JSON.stringify(response));
                    } else if (type == 2) {
                        sessionStorage.setItem('Intl_Airports', JSON.stringify(response));
                    }
                    resolve(); // Resolve the promise on successful completion
                } else {
                    console.error("Error:", Server_Request.status, Server_Request.statusText);
                    reject(new Error("Error fetching data")); // Reject the promise on error
                }
            }
        };
        Server_Request.send(Json);
    });
}
function DeleteMarkers() {
    for (let i = 0; i < Marker_List.length; i++) {
        Marker_List[i].setMap(null);
    }
    Marker_List = [];
}
async function AsynchCreateMarker(type) {
    await AirportFetcher(type);
    DeleteMarkers();
    if(type == 1)
    {
        type = "Local_Airports";
    }
    else
    {
        type = "Intl_Airports"
    }
    const Airport_Data = JSON.parse(sessionStorage.getItem(type))[0];
    for(let i in Airport_Data)
    {
        Values = Airport_Data[i]
        let Marker = new google.maps.Marker({
                position: new google.maps.LatLng(Values["latitude_deg"],Values["longitude_deg"]),
                map,
            }
        )
        Marker_List.push(Marker)
    }
}
function CreateMarker(type) {
    DeleteMarkers();
    if(type == 1)
    {
        type = "Local_Airports";
    }
    else
    {
        type = "Intl_Airports"
    }
    const Airport_Data = JSON.parse(sessionStorage.getItem(type))[0];
    for(let i in Airport_Data)
    {
        Values = Airport_Data[i]
        console.log(Values["latitude_deg"],Values["longitude_deg"]);
        let Marker = new google.maps.Marker({
                position: new google.maps.LatLng(Values["latitude_deg"],Values["longitude_deg"]),
                map,
            }
        )
        Marker_List.push(Marker)
    }
}
initMap()
document.getElementById("username").textContent = player_data['username'];
document.getElementById("currentlocation").textContent = player_data['location_name'] + "(" + player_data['location_icao'] + ")";
document.getElementById("budget").textContent = player_data['CO2_Budget'];
document.getElementById("fuel").textContent = player_data['Fuel'];
document.getElementById("money").textContent = player_data['Money'];

LocalAirportButton.onclick = async function()
{
    if (CheckAirport("Local_Airports") != true) {
        try
        {
            await AsynchCreateMarker(1);
        }
        catch (error) {
            console.error(error);
        }
    }
    else {
        CreateMarker(1);
    }
};
InternationalAirportButton.onclick = async function()
{
    if (CheckAirport("Intl_Airports") != true) {
        try
        {
            await AsynchCreateMarker(2);
        }
        catch (error) {
            console.error(error);
        }
    }
    else {
        CreateMarker(2);
    }
};