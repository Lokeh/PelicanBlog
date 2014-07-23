Title: Mobile Geolocation Gotchas
Date: 2014-07-17
Category: blogpost
Tags: JavaScript, AngularJS, geolocation, google maps
Slug: geolocation-gotchas
Author: Will Acton
Summary: 

One of the features I wanted to develop when I started planning my current main project, [PDX InTransit](http://github.com/Lokeh/BusTracker), was the ability to filter through stops based on their proximity to your current location. Once I started getting into the details of HTML5's geolocation, it seemed fairly easy: grab the client's position, plug it into Google Maps' API and then using the interface I already had developed for Trimet's services, pull in the stops within, say, 500m. This worked perfect on my desktop and when testing with Chrome's mobile emulation.

However, once I started playing with it on my phone, I found that it was horribly inaccurate at finding my location. Pulling out the data it was returning, it was showing a range of almost 1200m that my position could fall within. This seemed silly: when I opened up Goole's Maps app or any other app using geolocation, it worked fine. Even websites seemed to find my location fine, although somtimes it would take a minute...

It turns out that on mobile (I haven't been able to figure out yet if it's Android, mobile Chrome, or something in between which causes this), even with enableHighAccuracy set to true, the navigator.geolocation service tries to return a position as quickly as possible (at the cost of accuracy). However, if instead of using 'getCurrentPosition' - which is a one-time call to the geolocation API - we use 'watchPosition,' which constantly reports the clients position, after a few cycles it will narrow down to an acceptable range. Here's the code I ended up using:

	:::javascript
	var watch;
	//...
    $scope.getLocation = function (callback) {
        watch = navigator.geolocation.watchPosition(callback, $scope.geoError,
        		{ enableHighAccuracy: true, timeout : 3000, maximumAge: 0 }
        );
    }
    //...
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
	
The problem with this solution is that there's about a 2-6 second lag time in which it has to narrow down your location. My goal is to explore other options to get more accurate information, quicker. Right off hand, I could ping the user's location as soon as they open the app and have it refresh on an interval, however this may impact battery life on mobile devices as it is constantly using GPS.  For now showing a swirly ball while it finds the user's location will have to suffice.