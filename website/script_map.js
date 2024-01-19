// Initialize the map
var map = L.map("map",{
  zoomControl: false, // disables the zoom control buttons
  scrollWheelZoom: false, // disables zooming with the scroll wheel
  doubleClickZoom: false, // disables zooming with a double click
  touchZoom: false, // disables pinch-zooming on touch devices
  boxZoom: false, // disables zooming to a specific area selected using the shift key
  keyboard: false, // disables zooming using the + and - keys
  dragging: false, // disables moving the map by dragging
    tap: false // disables tap interaction on touch devices
}).setView([51.3356, 7.8626], 14);

// Add OpenStreetMap as the base map layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Add markers for the coordinates
var hoehleMarker = L.marker([51.341209, 7.872643]).addTo(map);

var krankenhausMarker = L.marker([51.326923, 7.867607]).addTo(map);

var schuleMarker = L.marker([51.327617, 7.852697]).addTo(map);
krankenhausMarker.bindPopup("Krankenhaus");
hoehleMarker.bindPopup("Höhle");
schuleMarker.bindPopup("Schule");
