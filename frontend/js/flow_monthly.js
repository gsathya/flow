var map = L.map('map').setView([20, 0], 3);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);


function loadMap()
{
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    function reqListener(){
	var json = JSON.parse(this.responseText);
	$.each(json, function(idx, obj){
            var lat = obj.srclat;
            var lng = obj.srclng;
            var marker = L.marker([lat, lng]).addTo(map);
            marker.bindPopup("<b>" + idx + "</b><br />");
        });
    }
    oReq.open("get", "/monthlysrc", true);
    oReq.send();
}

function fillMap(json)
{    

    var markers = new Array();
    var counter = 0;
    
    var srcLat = json.srclat;
    var srcLng = json.srclng;
    markers[counter] = L.marker([srcLat, srcLng]).addTo(map);
    markers[counter].bindPopup("<b>Source Router</b>").openPopup();

    $.each(json, function(idx, obj){
            if(idx=="srclat" || idx=="srclng"){
                //do nothing
            }else{
                var dstLat = obj.dstlat;
                var dstLng = obj.dstlng;
                markers[counter] = L.marker([dstLat, dstLng]).addTo(map);
                markers[counter].bindPopup("<b>Destination M-Lab</b>");
                var hopCount = obj.hop.length;
                var currentHop = 0;
                for(var i=0; i<hopCount; i++){
                    //if(currentHop+2 == obj.hop[i]){
           
                    //}
                    var pointA = new L.LatLng(obj.vertex_ip1_lat[i], obj.vertex_ip1_lng[i]);
                    var pointB = new L.LatLng(obj.vertex_ip2_lat[i], obj.vertex_ip2_lng[i]);
                    var points = [pointA, pointB]
                    var polyline = new L.Polyline(points, {
                                         color: get_random_color(),
                                         weight: 3,
                                         opacity: 0.5,
                                         smoothFactor: 1
                                         }).addTo(map);
                    polyline.bindPopup("<b>Info</b><br />Average RTT: " + obj.avg_rtt[i] + "<br />Persistence: " + obj.persistence[i] + "<br />Prevalence: " + obj.prevalence[i]);
                }
            }
           });

    function get_random_color() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.round(Math.random() * 15)];
        }
        return color;
    }    
}

function updateMonthlyData()
{
    var mac = document.getElementById('searchbox').value;
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    function reqListener(){
	var json = JSON.parse(this.responseText);
	console.log(json);
	$.each(json, function(idx, obj){
            var lat = obj.srclat;
            var lng = obj.srclng;
            var marker = L.marker([lat, lng]).addTo(map);
            marker.bindPopup("<b>" + idx + "</b><br />");
        });
    }
    var url = "/monthlystatsformac?mac=" + mac;
    oReq.open("get", url, true);
    oReq.send();
}
