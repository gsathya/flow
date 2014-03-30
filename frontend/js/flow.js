var map = L.map('map').setView([51.505, -0.09], 3);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

// create a red polyline from an arrays of LatLng points
var pointA = new L.LatLng(28.635308, 77.22496);
var pointB = new L.LatLng(28.984461, 77.70641);
var pointC = new L.LatLng(28.984461, 77.90641);
var pointList = [pointA, pointB, pointC];

var polyline = new L.Polyline(pointList, {
    color: 'red',
    weight: 3,
    opacity: 0.5,
    smoothFactor: 1
}).addTo(map);

// zoom the map to the polyline
map.fitBounds(polyline.getBounds());
