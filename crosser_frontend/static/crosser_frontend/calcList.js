var app = angular.module('calcList', []).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });

  
app.controller('CalcListCtrl', function($scope) {

});
