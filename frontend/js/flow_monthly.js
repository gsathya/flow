var map = L.map('map').setView([20, 0], 3);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

var jsonObj = {
    "avg_rtt": [
                29.93009375,
                42.475359375000004,
                45.6500625,
                217.21212500000001,
                218.230546875,
                216.98095238095237,
                214.92426984126982,
                215.5366984126984,
                223.56509523809524,
                244.18522222222222,
                246.239125,
                263.453890625,
                285.29765625,
                290.78508064516126,
                298.7735081967213,
                298.3849365079365,
                285.97630158730163
                ],
    "dstlat": 33.77629999999999,
    "dstlng": -84.398,
    "hop": [
            1,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18
            ],
    "persistence": [
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a",
                    "n/a"
                    ],
    "prevalence": [
                   1.0,
                   1.0,
                   1.0,
                   1.0,
                   1.0,
                   0.984375,
                   1.0,
                   0.984375,
                   1.0,
                   1.0,
                   1.0,
                   1.0,
                   1.0,
                   0.96875,
                   0.9838709677419355,
                   1.0,
                   1.0
                   ],
    "srclat": -37.8167,
    "srclng": 145.13330000000002,
    "vertex_ip1_lat": [
                       -37.8167,
                       -27.0,
                       -27.0,
                       -27.0,
                       1.3667000000000087,
                       1.3667000000000087,
                       37.53309999999999,
                       37.5155,
                       37.5155,
                       37.5155,
                       37.5155, 
                       37.5155, 
                       33.77629999999999, 
                       33.77629999999999, 
                       33.77629999999999, 
                       33.77629999999999, 
                       33.77629999999999
                       ], 
    "vertex_ip1_lng": [
                       145.13330000000002, 
                       133.0, 
                       133.0, 
                       133.0, 
                       103.80000000000001, 
                       103.80000000000001, 
                       -122.2471, 
                       -121.8962, 
                       -121.8962, 
                       -121.8962, 
                       -121.8962, 
                       -121.8962, 
                       -84.398, 
                       -84.398, 
                       -84.398, 
                       -84.398, 
                       -84.398
                       ], 
    "vertex_ip2_lat": [
                       -37.8167, 
                       -27.0, 
                       -27.0, 
                       1.3667000000000087, 
                       1.3667000000000087, 
                       37.53309999999999, 
                       37.5155, 
                       37.5155, 
                       37.5155, 
                       37.5155, 
                       37.5155, 
                       33.77629999999999, 
                       33.77629999999999, 
                       33.77629999999999, 
                       33.77629999999999, 
                       33.77629999999999, 
                       33.77629999999999
                       ], 
    "vertex_ip2_lng": [
                       145.13330000000002, 
                       133.0, 
                       133.0, 
                       103.80000000000001, 
                       103.80000000000001, 
                       -122.2471, 
                       -121.8962, 
                       -121.8962, 
                       -121.8962, 
                       -121.8962, 
                       -121.8962, 
                       -84.398, 
                       -84.398, 
                       -84.398, 
                       -84.398, 
                       -84.398, 
                       -84.398
                       ]
};

/*
var polylines = new Array();
var multipolyline;
for (var i=0; i<jsonArr.length;i++)
//for(var jsonObj in jsonArr)
{
    var jsonObj = jsonArr[i];
    
    //create marker
    var srcMarker = L.marker([jsonObj.srclat, jsonObj.srclng]).addTo(map);
    var dstMarker = L.marker([jsonObj.dstlat, jsonObj.dstlng]).addTo(map);
    srcMarker.bindPopup("<b>Source Router</b>").openPopup();
    dstMarker.bindPopup("<b>MLab Server" + i + "</b>" + jsonObj.hop.length);
    
    //add lines
    var hopCount = jsonObj.hop.length;
    var lastlat = jsonObj.dstlat, lastlng = jsonObj.dstlng;
    for (var j=0; j<hopCount; j++)
    {
        var srcPoint = new L.LatLng(jsonObj.vertex_ip1_lat[j], jsonObj.vertex_ip1_lng[j]);
        var dstPoint = new L.LatLng(jsonObj.vertex_ip2_lat[j], jsonObj.vertex_ip2_lng[j]);
        var points = [srcPoint, dstPoint];
        var polyline = new L.Polyline(points, {
                                      color: 'red',
                                      weight: 3,
                                      opacity: 0.5,
                                      smoothFactor: 1
                                      }).addTo(map);
        polyline.bindPopup("<b>Info</b><br />Average RTT: " + jsonObj.avg_rtt[j]);
        if(j==hopCount-1 && (jsonObj.vertex_ip2_lat[j]!=jsonObj.dstlat || jsonObj.vertex_ip2_lng[j]!=jsonObj.dstlng))
        {
            lastlat = jsonObj.vertex_ip2_lat[j];
            lastlng = jsonObj.vertex_ip2_lng[j];
        }
    }
    if(lastlat != dstlat || lastlng != dstlng)
    {
        var srcPoint = new L.LatLng(jsonObj.vertex_ip1_lat[j], jsonObj.vertex_ip1_lng[j]);
        var dstPoint = new L.LatLng(jsonObj.vertex_ip2_lat[j], jsonObj.vertex_ip2_lng[j]);
        var points = [srcPoint, dstPoint];
        var polyline = new L.Polyline(points, {
                                      color: 'red',
                                      weight: 3,
                                      opacity: 0.5,
                                      smoothFactor: 1
                                      }).addTo(map);
        polyline.bindPopup("<b>Info</b><br />Last One");
    }
    
    
}*/

//create marker
var srcMarker = L.marker([jsonObj.srclat, jsonObj.srclng]).addTo(map);
var dstMarker = L.marker([jsonObj.dstlat, jsonObj.dstlng]).addTo(map);
srcMarker.bindPopup("<b>Source Router</b>").openPopup();
dstMarker.bindPopup("<b>Destination MLab Server</b>");

//add lines
var count = jsonObj.avg_rtt.length;
for (var j=0; j<count; j++)
{
    var srcPoint = new L.LatLng(jsonObj.vertex_ip1_lat[j], jsonObj.vertex_ip1_lng[j]);
    var dstPoint = new L.LatLng(jsonObj.vertex_ip2_lat[j], jsonObj.vertex_ip2_lng[j]);
    var points = [srcPoint, dstPoint];
    var polyline = new L.Polyline(points, {
                                  color: 'red',
                                  weight: 3,
                                  opacity: 0.5,
                                  smoothFactor: 1
                                  }).addTo(map);
    polyline.bindPopup("<b>Info</b><br />Average RTT: " + jsonObj.avg_rtt[j] + "<br />Persistence: " + jsonObj.persistence[j] + "<br />Prevalence: " + jsonObj.prevalence[j]);
}

/*
multipolyline = new L.multiPolyline(polylines, {
                                    color: 'red',
                                    weight: 3,
                                    opacity: 0.5,
                                    smoothFactor: 1
                                    }).addTo(map);
*/
// zoom the map to the polyline
map.fitBounds(multipolyline.getBounds());

//get json
function httpGetMonthlyData(mac)
{
    var xmlHttp = null;
    var Url = "http://localhost:5000/monthlystatsformac?mac=" + mac;
    xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", Url, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function updateMonthlyData()
{
    var mac = document.getElementById('searchbox').value;
    var jsonObj = httpGetMonthlyData(mac);
}
