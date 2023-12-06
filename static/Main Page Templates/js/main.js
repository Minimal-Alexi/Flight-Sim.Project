let marker, player_data = JSON.parse(sessionStorage.getItem('userData'));
function initMap() {
    const user_location = player_data['location_coords']
    console.log(user_location)
    let mapProp = {
        center: new google.maps.LatLng(user_location[0], user_location[1]),
        zoom: 5,
    };
    let map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(user_location[0], user_location[1]),
        map,
        title: "Hello World!"
    });
}
    initMap()
    let infoWindow = new google.maps.InfoWindow({
        content: "This is the info window content"
    });
    marker.addListener('click', function() {
        infoWindow.open(map, marker);
    });
    document.getElementById("username").textContent = player_data['username'];
    document.getElementById("currentlocation").textContent = player_data['location_name'] + "(" + player_data['location_icao'] + ")";
    document.getElementById("budget").textContent = player_data['CO2_Budget']
    document.getElementById("fuel").textContent = player_data['Fuel']
    document.getElementById("money").textContent = player_data['Money']