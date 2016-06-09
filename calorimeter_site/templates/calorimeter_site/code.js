function initialize() {
	var map = new google.maps.Map();
	var mapOptions = {
		center: new google.maps.LatLng(44.5403, -78.5463),
		zoom: 8,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	}
    var map = new google.maps.Map(map_canvas, map_options);
}

google.maps.event.addDomListener(window, 'load', initialize);
