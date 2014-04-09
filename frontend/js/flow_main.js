var map = L.map('map').setView([20, 0], 3);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

// zoom the map to the polyline
//map.fitBounds(multipolyline.getBounds());

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

function httpGetMonthlyData()
{
    var xmlHttp = null;
    var Url = "http://localhost:5000/monthlysrc";
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

//get source locations and populate them on the map
function getSourceLocations()
{
    var url = "http://localhost:5000/monthlysrc";
    $.getJSON(url, function(json){
              $.each(json, function(idx, obj){
                     var lat = obj.srclat;
                     var lng = obj.srclng;
                     var marker = L.marker([lat, lng]).addTo(map);
                     marker.bindPopup("<b>Bismark Router</b><br />");
                     });
    });
    
    var json = {
    "122.107.200.10": {
        "srclat": -37.8167,
        "srclng": 145.13330000000002
    },
    "175.45.79.18": {
        "srclat": -27.0,
        "srclng": 133.0
    },
    "175.45.79.31": {
        "srclat": -27.0,
        "srclng": 133.0
    },
    "175.45.79.44": {
        "srclat": -27.0,
        "srclng": 133.0
    },
    "196.203.238.252": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "196.24.45.146": {
        "srclat": -33.983300000000014,
        "srclng": 18.400000000000006
    },
    "197.136.0.108": {
        "srclat": 1.0,
        "srclng": 38.0
    },
    "197.5.1.210": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.15.219": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.17.6": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.27.71": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.3.119": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.30.24": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.31.243": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.31.27": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "197.5.8.172": {
        "srclat": 34.0,
        "srclng": 9.0
    },
    "203.178.130.210": {
        "srclat": 35.69,
        "srclng": 139.69
    },
    "213.244.128.169": {
        "srclat": 51.51249999999999,
        "srclng": -0.08789999999999054
    },
    "217.163.1.108": {
        "srclat": 51.5,
        "srclng": -0.12999999999999545
    },
    "217.163.1.79": {
        "srclat": 51.5,
        "srclng": -0.12999999999999545
    },
    "217.163.1.92": {
        "srclat": 51.5,
        "srclng": -0.12999999999999545
    }, 
    "38.98.51.12": {
        "srclat": 34.0522, 
        "srclng": -118.24369999999999
    }, 
    "4.71.254.166": {
        "srclat": 38.0, 
        "srclng": -97.0
    }, 
    "41.231.21.44": {
        "srclat": 34.0, 
        "srclng": 9.0
    }
};
    
    var markers = new Array();
    var counter = 0;
    $.each(json, function(idx, obj){
           var lat = obj.srclat;
           var lng = obj.srclng;
           markers[counter] = L.marker([lat, lng]).addTo(map);
           markers[counter].bindPopup($('<a href="#" class="monthlylink">Monthly Data</a>')
                                      .click(function() {
                                             window.location = "http://localhost:8000/monthly.html?srcip=" + idx;
                                             })[0]);
           counter++;
           });
    
    map.fitBounds(markers.getBounds());
    
}
