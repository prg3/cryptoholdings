var REFRESH = 5000 ;
var App = angular.module('App', []);
$http = "Crypto Coins";
var altcoins = new Object();
var btc = new Object();
var total = 0;

mycoins = function($myCoins) {};
 
App.controller('CoinsCtrl', function ($scope, $http, $location) {
	$scope.bitcoins = "0";

//	$scope.$watch('locationPath', function(path) {
//		$location.path(path);
//	});

	$scope.$watch(function() {
		return $location.path(); }, function(path) {
    		$scope.locationPath = path.split("/");
  	});
  	$http.get('http://www.cryptoholdings.com/cgi-bin/altcoins.json')
	       .then(function(res){
		  for (var key in res.data) {
			if ( key != "BTC" ) {
       	   			altcoins[key] = res.data[key];
			} else {
				res.data[key][2] = 1;
				altcoins[key] = res.data[key];
			}
			if ( typeof($location.search(key)) != "undefined") {
				altcoins[key][3] = $location.search(key)
			}
			
		  }
		  $scope.altcoins = altcoins;
        });

	$http.get("http://www.cryptoholdings.com/cgi-bin/bitcoin.json")
		.then(function(res){
			for (var key in res.data) {
				btc[key] = res.data[key];
			}
		$scope.btc = btc;
	});

	$scope.updateTotal = function () {
		$scope.total = parseFloat("0");
		$scope.total = $scope.total + parseFloat($scope.bitcoins);
		angular.forEach($scope.altcoins, function (coin, key) {
			$scope.total = parseFloat($scope.total) + (parseFloat(coin[2]) * parseFloat(coin[3]));
		})
		for (var key in $scope.btc) {
			$scope.btc[key][3] = parseFloat($scope.total) * parseFloat($scope.btc[key][2]);
		}
	}

	$scope.updateCoin = function(coin, value) {
		coin[3] = value;
		coin[4] = value * coin[2];
		$scope.updateTotal();
		$scope.locationPath[coin] = coin[3];
	}



});
