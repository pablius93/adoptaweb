function contactInfoMap() {
    var mapCanvas = document.getElementById("map");
    var address = $("#cell-address").text();
    var city = $("#cell-city").text();
    var fullAddress = city + " " + address;
    fullAddress = fullAddress.replace(/[^\w\-]+/g, ' ')
                             .replace(/\-\-+/g, '')
                             .replace(/^-+/, '')
                             .replace(/-+$/, '');
    console.log(fullAddress);
    $.get('http://maps.google.com/maps/api/geocode/json', {'address': fullAddress})
        .done(
            function(data, status)
            {
                var lat = data.results[0].geometry.location.lat;
                var lng = data.results[0].geometry.location.lng;
                var center = new google.maps.LatLng(lat, lng);
                var mapOptions = {
                    center: center,
                    zoom: 18,
                    panControl: true,
                    zoomControl: true,
                    mapTypeControl: false,
                    scaleControl: false,
                    streetViewControl: false,
                    overviewMapControl: true,
                    rotateControl: false
                }
                var marker = new google.maps.Marker({
                    position: center
                });
                var map = new google.maps.Map(mapCanvas, mapOptions);
                marker.setMap(map);
                google.maps.event.addListener(marker,'click',function() {
                    var infoWindow = new google.maps.InfoWindow({
                        content: $("#cell-pet-name").text()
                    });
                    infoWindow.open(map,marker);
                });
            }
        );
}
