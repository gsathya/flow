var map = L.map('map').setView([20, 0], 2);
var osmAttr = '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>';
var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

var tileLayer = L.tileLayer(osmUrl, {
    attribution: osmAttr,
    maxZoom: 18
}).addTo(map);

var markers = new L.FeatureGroup();

function loadMapwihtoutsrc()
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
    oReq.open("get", "/dailysrc", true);
    oReq.send();
}

function loadMap()
{
    var oReq = new XMLHttpRequest();
    oReq.onload = reqListener;
    function reqListener(){
	      var json = JSON.parse(this.responseText);
        var ips = {};
        
        $.each(json, function(key, val){

            for(var idx in val) {
                path = val[idx];

                var start_lat = path[0][0];
                var start_lng = path[0][1];
                var ip = path[0][2];
                
                var marker = L.marker([start_lat, start_lng]);
	              marker.bindPopup("<b>" + ip + "</b><br />");
	              markers.addLayer(marker);
                console.log(ip);
                var end_lat = path[path.length-1][0];
                var end_lng = path[path.length-1][1];
                var ip = path[path.length-1][2];                

                var marker = L.marker([end_lat, end_lng]);
	              marker.bindPopup("<b>" + ip + "</b><br />");
	              markers.addLayer(marker);

                var pathColor = get_random_color();
                var points = [];
                
                for(var j=0; j<path.length;j++) {
                    var point = new L.LatLng(path[j][0], path[j][1])
                    points.push(point);
                }
                var polyline = new L.Polyline(points, {
                    color: pathColor,
                    weight: 3,
                    opacity: 0.5,
                    smoothFactor: 1
                });
		            markers.addLayer(polyline);

            }
        });
	      map.addLayer(markers);	
    }
    oReq.open("get", "/dailystats", true);
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
		      markers.addLayer(polyline);
            }
  });
    }	      	      
    var params = "srcip=" + srcip;
    oReq.open("get", "/dailystats?" + params, true);
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
	$.each(json, function(idx, obj){
	    // TODO parse response and plot polylines
        });
    }	      	      
    var params = "mac=" + mac;
    oReq.open("get", "/monthlystats?" + params, true);
    oReq.send();
}
