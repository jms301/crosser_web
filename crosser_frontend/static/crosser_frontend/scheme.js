angular.module('scheme', ['schemecon', 'crosserFilters']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    }).
    config(["$httpProvider", function(provider) {
      provider.defaults.headers.common['X-CSRFToken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  }]);


function PlanCtrl($scope, Scheme) { 
    $scope.scheme = Scheme.get({id: 1}, function () {
        var old_chromo = $scope.scheme.species.chromosome_lengths;
        $scope.scheme.species.chromosome_lengths = _.map(old_chromo.split(","),
                         function (num) { return parseInt(num, 10)});
     });

    $scope.addLoci =   function ( plant ) {
        plant.loci.push({"name": null, "locus_type": null, "linkageGroup": null});
    };

    $scope.addCross = function ( scheme ) {
        scheme.crosses.push({"name": null, "left_cross_parent": null, "right_cross_parent": null, "left_plant_parent": null, "right_plant_parent": null, "protocol_zygosity": null, "loci": []});
    };

    $scope.isSelected = function ( item, option ) { 
        if (item != option || item == null || option == null)
            return false; 
        else
            return true; 
    };
   
    $scope.updateScheme = function ( scheme ) {
        var _species = scheme.species; 
        scheme.update();
        scheme.species = _species;
    };
}
