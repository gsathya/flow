var map = L.map('map').setView([20, 0], 3);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

var tileLayer = L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

var markers = new L.FeatureGroup();

function loadMap()
{
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    function reqListener(){
	var json = JSON.parse(this.responseText);
	$.each(json, function(idx, obj){
            var lat = obj.srclat;
            var lng = obj.srclng;
            var marker = L.marker([lat, lng]);
            marker.bindPopup("<b>" + idx + "</b><br />");
	    (function(idx, lat, lng){ 
		marker.on("dblclick", function() { selectSource(idx, lat, lng); });
	    })(idx, lat, lng);
	    markers.addLayer(marker);
        });
	map.addLayer(markers);	
    }
    oReq.open("get", "/monthlysrc", true);
    oReq.send();
}

function selectSource(srcip, lat, lng)
{
    markers.clearLayers();
    var marker = L.marker([lat, lng]);
    marker.bindPopup("<b>" + srcip + "</b><br />");
    markers.addLayer(marker);
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    function reqListener(){
	var json = JSON.parse(this.responseText);
	$.each(json, function(idx, obj){
            var dstLat = obj.dstLat;
            var dstLng = obj.dstLng;
	    var marker = L.marker([dstLat, dstLng]);
	    marker.bindPopup("<b>" + idx + "</b><br />");
	    markers.addLayer(marker);
            var hopCount = obj.hopCount;
	    var pathColor = get_random_color();
            for(var i=0; i<hopCount; i++){
                var pointA = new L.LatLng(obj.vertex_ip1_lat[i], obj.vertex_ip1_lng[i]);
                var pointB = new L.LatLng(obj.vertex_ip2_lat[i], obj.vertex_ip2_lng[i]);
                var points = [pointA, pointB];
                var polyline = new L.Polyline(points, {
                    color: pathColor,
                    weight: 3,
                    opacity: 0.5,
                    smoothFactor: 1
                });
                polyline.bindPopup("<b>Info</b><br />Average RTT: " + obj.avg_rtt[i] + "<br />Persistence: " + obj.persistence[i] + "<br />Prevalence: " + obj.prevalence[i]);
		markers.addLayer(polyline);
            }
        });
    }	      	      
    var params = "srcip=" + srcip;
    oReq.open("get", "/monthlystats?" + params, true);
    oReq.send();
}

function get_random_color() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
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
