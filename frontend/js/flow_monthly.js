var map = L.map('map').setView([20, 0], 2);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

var tileLayer = L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 19
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
            marker.bindPopup("<b>" + idx + "</b><br />Double Click to View Route");
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
    var marker = L.marker([lat, lng]).addTo(map);
    marker.bindPopup("<b>Source Location</b><br />" + srcip).openPopup();
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
           (function(srcip, idx){
            marker.on("dblclick", function() { mapSingleSrcDst(srcip, idx); });
            })(srcip, idx);
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

function searchByMac()
{
    markers.clearLayers();
    var mac = document.getElementById('searchbox').value;
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    
    function reqListener(){
        var json = JSON.parse(this.responseText);
        var srcip = json.srcip;
        var srcLat = json.srcLat;
        var srcLng = json.srcLng;
        var srcMarker = L.marker([srcLat, srcLng]).addTo(map);
        srcMarker.bindPopup("<b>Source Location</b><br />MAC: " + mac + "<br />srcIP: " + srcip).openPopup();
        $.each(json, function(idx, obj){
        
           var dstLat = obj.dstLat;
           var dstLng = obj.dstLng;
           var marker = L.marker([dstLat, dstLng]).addTo(map);
           marker.bindPopup("<b>" + idx + "</b><br />");
               (function(srcip, idx){
                marker.on("dblclick", function() { mapSingleSrcDst(srcip, idx); });
                })(srcip, idx);
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
    var params = "mac=" + mac;
    oReq.open("get", "/monthlystats?" + params, true);
    oReq.send();
}

function mapSingleSrcDst(srcip, dstip){
    
    markers.clearLayers();
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    function reqListener(){
        var json = JSON.parse(this.responseText);
        var srcip = json.srcip;
        var srcLat = json.srcLat;
        var srcLng = json.srcLng;
        var srcMarker = L.marker([srcLat, srcLng]).addTo(map);
        srcMarker.bindPopup("<b>Source Location</b><br />srcIP: " + srcip).openPopup();
        $.each(json, function(idx, obj){
               
               var dstLat = obj.dstLat;
               var dstLng = obj.dstLng;
               var marker = L.marker([dstLat, dstLng]).addTo(map);
               marker.bindPopup("<b>" + idx + "</b><br />");
               //markers.addLayer(marker);
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
    var params = "srcip=" + srcip + "&dstip=" + dstip;
    oReq.open("get", "/monthlystats?" + params, true);
    oReq.send();
}
