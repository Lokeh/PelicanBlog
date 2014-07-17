Title: Mobile Geolocation Gotchas
Date: 2014-07-17
Category: blogpost
Tags: JavaScript, AngularJS, geolocation, google maps
Slug: geolocation-gotchas
Author: Will Acton
Summary: 

One of the cooler features I wanted to develop when I started planning my current main project, [PDX InTransit](http://github.com/Lokeh/BusTracker), was the ability to filter through stops based on their proximity to your current location. Once I started getting into the details of HTML5's geolocation, it seemed fairly easy: grab the client's position, plug it into Google Maps' API and then using the interface I already had developed for Trimet's services, pull in the stops within, say, 500m. This worked perfect on my desktop and when testing with Chrome's mobile emulation.

However, once I started playing with it on my phone, I found that it was horribly inaccurate at finding my location. Pulling out some of the data it was returning, it was returning a range of almost 1200m that my position could fall within. This seemed silly: when I opened up Goole's Maps app or any other app using geolocation, it worked fine. Even websites seemed to find my location fine, although it seemd to take a minute...

It turns out that on mobile (I haven't been able to figure out yet if it's Android, mobile Chrome, or something in between which causes this), even with enableHighAccuracy set to true, tries to return a position as quickly as possible (at the cost of accuracy). However, if instead of using 'getCurrentPosition' - which is a one-time call to the geolocation API - one uses 'watchPosition,' which constantly reports the clients position, after a few cycles it will slowly narrow it down to an acceptable range. Here's the code I ended up using:

	:::javascript
    $scope.getLocation = function (callback) {
        watch = navigator.geolocation.watchPosition(callback, $scope.geoError, { enableHighAccuracy: true, timeout : 3000, maximumAge: 0 });
    }
    ...
    var init = function () {
		$scope.getLocation(function (loc) {
            if (loc.coords.accuracy <= 150) {
                navigator.geolocation.clearWatch(watch);
                $scope.loc = { 'lat': loc.coords.latitude, 'lng': loc.coords.longitude };
                $scope.drawMap();
				$scope.getNearbyStops(loc.coords.latitude, loc.coords.longitude);
            }

		});
	}