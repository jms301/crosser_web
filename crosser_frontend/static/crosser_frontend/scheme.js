angular.module('scheme', ['schemecon', 'crosserFilters']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });

//.
    //config(["$httpProvider", function(provider) {
     // provider.defaults.headers.common['X-CSRFToken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  //}]);


function PlanCtrl($scope, Scheme, Species, $location) { 
    // set up the PlanController context
    $scope.plan_id = window.location.pathname.split("/")[2]; 
    $scope.scheme = Scheme.get({id: $scope.plan_id}, function () {
     });

    $scope.species = Species.get(function () {
        _.each($scope.species.objects, function(element, index, list) { 
            element.chromosome_lengths = _.map(element.chromosome_lengths.split(","), 
                function(num) { return parseInt(num, 10)});    
        });
    $scope.to_del = [];
    });

    // function to add a new locus to a plant
    $scope.addLocus =   function ( plant ) {
        plant.loci.push({"name": null, "locus_type": null, "linkageGroup": null});
    };

    // function to remove an item from an arbitrary array
    $scope.removeItem = function ( item, arry) {
        $scope.to_del.push(item.resource_uri);
        var index = arry.indexOf(item);
        arry.splice(index, 1);
        console.log($scope.to_del);
    }

    // function to add a new cross to a scheme
    $scope.addCross = function ( scheme ) {
        scheme.crosses.push({"name": null, "left_cross_parent": null, "right_cross_parent": null, "left_plant_parent": null, "right_plant_parent": null, "protocol_zygosity": null, "loci": []});
    };


    // function to select the right item in an options list of plants / crosses 
    $scope.isSelected = function ( item, option ) { 
        if (item != option || item == null || option == null)
            return false; 
        else
            return true; 
    };
  

    // update function 
    $scope.updateScheme = function ( scheme, to_del ) {
        console.log(to_del);
        scheme.patch({"objects" : [scheme], 
                "deleted_objects" : to_del}, {});
    };
}
