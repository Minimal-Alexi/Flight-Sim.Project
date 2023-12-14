let map;
let Player_Pos_Marker, player_data = JSON.parse(sessionStorage.getItem('userData')), distance_circle, Marker_List = [];
const LocalAirportButton = document.getElementById("Local Airports Filter"),
    InternationalAirportButton = document.getElementById("International Airports Filter");
let continent;

function circle_maker() {
    let user_location = player_data['location_coords'];
    user_location = new google.maps.LatLng(user_location[0], user_location[1]);
    if (player_data['BoughtFuelTank'] == true) {
        distance_circle =
            {
                strokeColor: '#007BFF', // Color of the circle border
                strokeOpacity: 0.8,      // Opacity of the circle border
                strokeWeight: 2,         // Thickness of the circle border
                fillColor: '#007BFF',   // Fill color of the circle
                fillOpacity: 0.3,        // Opacity of the circle fill
                map: map,                // Assuming 'map' is your Google Map instance
                center: user_location, // Center the circle on the player's position
                radius: (player_data['Fuel'] + 250) * player_data['Fuel_Efficiency'] * 1000
            };
    } else {
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
    }
    distance_circle = new google.maps.Circle(distance_circle);
}

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
    circle_maker()
    let infoWindow = new google.maps.InfoWindow({
        content: "You are currently at this position." + " " + player_data['location_name'] + " (" + player_data['location_icao'] + ")"
    });
    Player_Pos_Marker.addListener('click', function () {
        infoWindow.open(map, Player_Pos_Marker);
    });
}
function winscore()
{
    return parseInt(player_data['money'])+parseInt(player_data['CO2_Budget'])*1000
}

function PlayerMarkerUpdate() {
    let user_location = player_data['location_coords'];
    user_location = new google.maps.LatLng(user_location[0], user_location[1]);
    Player_Pos_Marker.setPosition(user_location)
    distance_circle.setMap(null);
    circle_maker()
    if(player_data['location_icao'] == "KLAX")
    {
        alert("Congratulations player, you have reached the end goal!")
        if(parseInt(player_data['CO2_Budget'])<=0)
        {
            alert("However, the path of smoke and destruction you've left, has forever doomed the countries you have traveled to.\n" +
            "Your journey was inefficient and destructive, but at least the water has arrived on time.\n" +
            "Was it worth it?\n" +
            "Final score:" + winscore())
        }
        else if(parseInt(player_data['CO2_Budget'])>=100)
        {
            alert("You were really close to catastrophe." +
                "But you successfully delivered water to all the poor californians, and you did it on time no less!\n" +
                "I'm sure the Americans will accept immigrants like you, right?\n" +
                "Uhmm...yeah, good luck flying back to Finland!\n"+
                "Final score:" + winscore())
        }
        else
        {
            alert("Hooray, you did your best, protected the environment, and saved California.\n" +
                "Yes...all of it.\n" +
                "Look, the drought was really severe.\n" +
                "Tommorrow president Boe Jiden will give you an award for protecting the planet and saving Californians\n")
            alert("You probably should've stopped at saving just the planet but it's fine. Good job pilot :3.\n"+
                "Final score:" + winscore())
        }
    }
}

//Type 1 is local, type 2 is local.
function CheckAirport(Type) {
    if (Type == "Local_Airports" && sessionStorage.getItem(Type) != null) {
        console.log(sessionStorage.getItem(Type));
        return true;
    } else if (Type == "Intl_Airports" && sessionStorage.getItem(Type) != null && continent == document.getElementById("continent").value ) {
        console.log(sessionStorage.getItem(Type));
        return true;
    }
    return false;
}

function DisplayStats() {
    document.getElementById("username").textContent = player_data['username'];
    document.getElementById("currentlocation").textContent = player_data['location_name'] + "(" + player_data['location_icao'] + ")";
    document.getElementById("budget").textContent = player_data['CO2_Budget'];
    document.getElementById("fuel").textContent = player_data['Fuel'];
    document.getElementById("money").textContent = player_data['Money'];
}

function AirportFetcher(type) {
    return new Promise((resolve, reject) => {
        let Server_Request = new XMLHttpRequest(),Json;
        if (type == 1) {
            Json = JSON.stringify({
                databaseID: player_data['databaseID'],
                type_request: type,
            });
        } else {
            let target_continent = document.getElementById("continent").value;
            Json = JSON.stringify({
                databaseID: player_data['databaseID'],
                type_request: type,
                target_continent: target_continent,
            })
            continent = target_continent;
        }
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

function TravelPost(ICAO, distance) {

    let Server_Request = new XMLHttpRequest();
    let json = JSON.stringify({
        databaseID: player_data['databaseID'],
        type_request: 3,
        destination: ICAO,
        distance: distance
    })
    Server_Request.open("POST", "/Main", true);
    Server_Request.setRequestHeader("Content-Type", "application/json");
    Server_Request.onreadystatechange = function () {
        if (Server_Request.readyState == XMLHttpRequest.DONE) {
            if (Server_Request.status == 200) {
                // Successful response from the server
                let response = JSON.parse(Server_Request.responseText);
                console.log(response);
                sessionStorage.clear();
                sessionStorage.setItem('userData', JSON.stringify(response));
                player_data = JSON.parse(sessionStorage.getItem('userData'))
                DisplayStats()
                DeleteMarkers()
                PlayerMarkerUpdate()

            } else {
                // Error response from the server
                console.error("Error:", Server_Request.status, Server_Request.statusText);
                // Handle the error as needed
            }
        }
    };
    Server_Request.send(json);
}

async function AsynchCreateMarker(type) {
    await AirportFetcher(type);
    DeleteMarkers();
    if (type == 1) {
        type = "Local_Airports";
    } else {
        type = "Intl_Airports"
    }
    const Airport_Data = JSON.parse(sessionStorage.getItem(type))[0];
    for (let i in Airport_Data) {
        Values = Airport_Data[i]
        let Marker = new google.maps.Marker({
                position: new google.maps.LatLng(Values["latitude_deg"], Values["longitude_deg"]),
                map,
                icao: Values["icao"],
                distance: Values["distance"]
            }
        )

        let InfoView = new google.maps.InfoWindow({
            content: Values["name"] + " (" + Values["icao"] + ") " + Values["distance"] + "kms away."
        });
        Marker.addListener('click', function () {
                InfoView.open(map, Marker);
            }
        )
        Marker.addListener('dblclick', function () {
                TravelPost(Marker.icao, Marker.distance);
            }
        )
        Marker_List.push(Marker)
    }
}

function CreateMarker(type) {
    DeleteMarkers();
    if (type == 1) {
        type = "Local_Airports";
    } else {
        type = "Intl_Airports"
    }
    const Airport_Data = JSON.parse(sessionStorage.getItem(type))[0];
    for (let i in Airport_Data) {
        Values = Airport_Data[i]
        let Marker = new google.maps.Marker({
                position: new google.maps.LatLng(Values["latitude_deg"], Values["longitude_deg"]),
                map,
                icao: Values["icao"],
                distance: Values["distance"]
            }
        )

        let InfoView = new google.maps.InfoWindow({
            content: Values["name"] + " (" + Values["icao"] + ") " + Values["distance"] + "kms away."
        });
        Marker.addListener('click', function () {
                InfoView.open(map, Marker);
            }
        )
        Marker.addListener('dblclick', function () {
                TravelPost(Marker.icao, Marker.distance);
            }
        )
        Marker_List.push(Marker)
    }
}

initMap()
DisplayStats()

LocalAirportButton.onclick = async function () {
    if (CheckAirport("Local_Airports") != true) {
        try {
            await AsynchCreateMarker(1);
        } catch (error) {
            console.error(error);
        }
    } else {
        CreateMarker(1);
    }
};
InternationalAirportButton.onclick = async function () {
    if (CheckAirport("Intl_Airports") != true) {
        try {
            await AsynchCreateMarker(2);
        } catch (error) {
            console.error(error);
        }
    } else {
        CreateMarker(2);
    }
};