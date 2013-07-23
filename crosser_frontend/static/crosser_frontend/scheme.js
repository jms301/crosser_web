angular.module('scheme', ['ui.bootstrap', 'schemecon', 'crosserFilters']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });



function PlanCtrl($scope, Scheme, Plant, Cross, Locus, Species, $location) { 
    // set up the PlanController context
    $scope.plan_id = window.location.pathname.split("/")[2]; 

    $scope.get_plant_by_uri = function (ref) { 
        return _.findWhere($scope.scheme.plants, {resource_uri: ref});
    };

    $scope.get_cross_by_uri = function (ref) {
        
        return _.findWhere($scope.scheme.crosses, {resource_uri: ref});
    };

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
        // setup an array 'ancestor_loci' in each cross so we can tell which loci are available to add into any cross. 
        _.each($scope.scheme.crosses, $scope.add_loci_list);

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

    // function to get all origin plants for any cross
    $scope.add_loci_list = function(cross, index, crosses) {
        plants = [];
        parents = [];
        loci = [];

        parents.push(cross.left_parent);
        parents.push(cross.right_parent);

        while(parents.length != 0) { 
            process = parents.pop();
            //console.log(process);
            if (process.indexOf('/api/v1/cross/')==0) { 
                c = $scope.get_cross_by_uri(process);
                //console.log(process);
                //console.log(c);
                parents.push(c.right_parent);
                parents.push(c.left_parent);
            } else if (process.indexOf('/api/v1/plant/')==0) {
                plants.push($scope.get_plant_by_uri(process));
            }
        }
        console.log(plants);
        cross.ancestor_loci = _.flatten(_.map(_.uniq(plants), 
        function(plant, index, plants) { 
            return plant.loci
        }));
    };

    $scope.strip_loci_list = function(cross, index, crosses) {
        delete cross.ancestor_loci; 
    };
    // function to add a new locus to a plant
    $scope.add_locus =   function ( plant ) {
        plant.loci.push({"name": null, "locus_type": null, "linkageGroup": null});
    };
    // function to remove a locus from the scheme & any crosses
    $scope.removeLocus = function (locus, plant) {
        _.each($scope.scheme.crosses, function(cross){ 
            cross.loci = _.reject(cross.loci, function(l){
               return locus.resource_uri == l;
            });
        });

        plant.loci = _.reject(plant.loci, function (item){ 
            return item === locus; // have to match exactly otherwise we remove things with a blank resource_uri.
        }); 
        $scope.to_del.push(locus.resource_uri);
    };

    // function to remvoe a locus from a cross
    $scope.removeCrossLocus = function (cross, locus) {
        cross.loci = _.reject(cross.loci, function(l){
            return locus == l;
        });
    }

    // function to remove a cross from the scheme & parent array
    $scope.removeCross = function (cross) {
        $scope.parents = _.reject($scope.parents, function (item){ return item.resource_uri == cross.resource_uri}); 
        $scope.scheme.crosses = _.reject($scope.scheme.crosses, function (item){ return item.resource_uri == cross.resource_uri}); 
        $scope.to_del.push(cross.resource_uri);
    };
    // function to remove an item from an arbitrary array
    $scope.removeItem = function ( item, arry) {
        $scope.to_del.push(item.resource_uri);
        var index = arry.indexOf(item);
        arry.splice(index, 1);
    };

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
        _.each(scheme.crosses, $scope.strip_parents);
        _.each(scheme.crosses, $scope.strip_loci_list);
        scheme.update(scheme);
        _.each(scheme.crosses, $scope._loci_list);
        _.each(scheme.crosses, $scope.add_parents);
    };
}
