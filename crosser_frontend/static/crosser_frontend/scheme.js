angular.module('scheme', ['schemecon', 'crosserFilters']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });



function PlanCtrl($scope, Scheme, Species, $location) { 
    // set up the PlanController context
    $scope.plan_id = window.location.pathname.split("/")[2]; 

    $scope.add_parents = function(c, index, crosses) {
            if (c.left_plant_parent != null)
                c.left_parent = c.left_plant_parent;
            else
                c.left_parent = c.left_cross_parent;
    
            if (c.right_plant_parent != null)
                c.right_parent = c.right_plant_parent;
            else
                c.right_parent = c.right_cross_parent;
            
        };
    
   $scope.strip_parents = function(c, index, crosses) {
            if (c.left_parent != null) {
                if (c.left_parent.indexOf('/api/v1/cross/')==0)
                    c.left_cross_parent = c.left_parent
                else if (c.left_parent.indexOf('/api/v1/plant/')==0)
                    c.left_plant_parent = c.left_parent

            }
            if (c.right_parent != null) {
                if (c.right_parent.indexOf('/api/v1/cross/')==0)
                    c.right_cross_parent = c.right_parent
                else if (c.right_parent.indexOf('/api/v1/plant/')==0)
                    c.right_plant_parent = c.right_parent

            }

            delete c.left_parent 
            delete c.right_parent 
        };


    $scope.scheme = Scheme.get({id: $scope.plan_id}, function () {
        // add in fake left_parent & right_parent properties to the crosses
        // this allows us to use convenient ng-options stuff in the frontend
        // the properties will be split out before saving.
        _.each($scope.scheme.crosses, $scope.add_parents);

        // setup array 'parents' that can be used to populate select options 
        // the type field is used to provide groupings in the dropdown
        tmp_plants =  _.map($scope.scheme.plants, 
        function(plant, index, parents){
            return {type: "Plants", name: plant.name, 
                    resource_uri: plant.resource_uri};
        });
        tmp_cross = _.map($scope.scheme.crosses, 
        function(cross, index, parents){
            return {type: "Crosses", name: cross.name, 
                    resource_uri: cross.resource_uri};
        });
        $scope.parents = tmp_cross.concat(tmp_plants); 
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
        if(!_.contains($scope.to_del, item.resource_uri))
            $scope.to_del.push(item.resource_uri);
        var index = arry.indexOf(item);
        arry.splice(index, 1);
        //console.log($scope.to_del);
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
    
        _.each(scheme.crosses, $scope.strip_parents);
        scheme.update(scheme);
        _.each(scheme.crosses, $scope.add_parents);
    };
}
