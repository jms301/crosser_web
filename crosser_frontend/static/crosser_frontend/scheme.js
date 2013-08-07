/************************
Data Structure used in this controller:

$scope.scheme - The whole scheme object as returned by tastypie
$scope.species - a list of species names & their genome array fetched from tastypie.
$scope.cross_data - object holding local data for the display of crosses, 
                    each key is the cross resource_uri and holds:
                     *  left_parent & right_parent - the parent resource_uris 
                        can be a cross or a plant, and will be converted to 
                        cross_left/right_parent or plant_left/right_parent for
                         upload. 
                        
                     *  poss_loci - the loci that can theoretically be 
                        selected for in that cross 
                        (since their parents have them)

                     *  ancestor_list - the crosses & plants? which could be
                       parents of this cross.

$scope.poss_parents  - a list of all possible parents (crosses & plants) 
                  each including a type variable for cross parent select 
                  drop down.

TODO: 
    * Re-write the 'add_cross and function.

    * Re-write the remove functions so that they actually delete the resource from the database. 

*************************/

angular.module('scheme', ['ui.bootstrap', 'schemecon', 'crosserFilters']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });


function PlanCtrl($scope, Scheme, Plant, Cross, Locus, Species, $location) { 
    // set up the PlanController context
    $scope.plan_id = window.location.pathname.split("/")[2];
    $scope.user_id = document.getElementsByName('userid')[0].value;
    // set up a cross_data array (allows us to keep the JSON clean 
    // to msg the API)
    $scope.cross_data = {};

    // pull down list of species
    $scope.species = Species.get(function () {
        _.each($scope.species.objects, function(element, index, list) { 
            element.chromosome_lengths = _.map(element.chromosome_lengths.split(","), 
                function(num) { return parseInt(num, 10)});    
        });
    $scope.to_del = [];
    });
   
    if($scope.plan_id != 'new') { 
        // pull down the scheme for the scope
        $scope.scheme = Scheme.get({id: $scope.plan_id}, function () {
            // add in fake left_parent & right_parent properties to the crosses
            // this allows us to use convenient ng-options stuff in the frontend
            // the properties will be split out before saving.
            _.each($scope.scheme.crosses, $scope.update_cross_parents);
            // setup an array 'ancestor_list' local data for each cross so 
            // we can see loci are available to add into a cross. 
            _.each($scope.scheme.crosses, $scope.add_ancestor_list);
            $scope.update_parents();
        });
    } else {
    // populate a new scheme object
        $scope.scheme = { 
            name: null,
            species: null,
            crosses:[],
            plants: []
        };
    }

     // update function 
    $scope.updateScheme = function (scheme, to_del) {
        scheme.update(scheme);
    };

    $scope.update_parents = function() { 
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
            $scope.poss_parents = tmp_cross.concat(tmp_plants); 
    };


    $scope.update_cross_parents = function(c, index, crosses) {
        data = {};
        if($scope.cross_data[c.resource_uri] == null)
            $scope.cross_data[c.resource_uri] = {};
        if (c.left_plant_parent != null)
        $scope.cross_data[c.resource_uri].left_parent = c.left_plant_parent;
        else
        $scope.cross_data[c.resource_uri].left_parent = c.left_cross_parent;
   
        if (c.right_plant_parent != null)
        $scope.cross_data[c.resource_uri].right_parent = c.right_plant_parent;
        else
        $scope.cross_data[c.resource_uri].right_parent = c.right_cross_parent;
    };

    $scope.update_cross = function(cross) { 
        $scope.update_parents();
    };

    $scope.update_plant = function(plant) { 
        $scope.update_parents();
    };

    $scope.get_plant_by_uri = function (ref) { 
        return _.findWhere($scope.scheme.plants, {resource_uri: ref});
    };

    $scope.get_cross_by_uri = function (ref) {
        return _.findWhere($scope.scheme.crosses, {resource_uri: ref});
    };

    $scope.get_cross_left_parent = function(c) {   
        return $scope.cross_data[c.resource_uri].left_parent;
    }; 

    $scope.get_cross_right_parent = function(c) {   
        return $scope.cross_data[c.resource_uri].right_parent;
    }; 

    $scope.add_ancestor_list = function(cross, index, crosses) {
        plants = [];
        parents = [];

        parents.push($scope.get_cross_left_parent(cross));
        parents.push($scope.get_cross_right_parent(cross));

        while(parents.length != 0) { 
            process = parents.pop();
            if (process.indexOf('/api/v1/cross/')==0) { 
                c = $scope.get_cross_by_uri(process);
                parents.push($scope.get_cross_left_parent(c));
                parents.push($scope.get_cross_right_parent(c));
            } else if (process.indexOf('/api/v1/plant/')==0) {
                plants.push($scope.get_plant_by_uri(process));
            }
        }
        plants = _.uniq(plants);
        $scope.cross_data[cross.resource_uri].ancestor_list = plants;
        $scope.cross_data[cross.resource_uri].poss_loci = 
            _.flatten(_.map(plants, function(plant){
            return plant.loci;
        }));
    };

    $scope.add_plant = function ( scheme ) { 
        scheme.plants.push ( 
            Plant.save(
                {"name":null, })
        )
    }

    // function to add a new locus to a plant
    $scope.add_locus =   function ( plant ) {
        Locus.save(
            {"name": null, 
            "locus_type": "Tr", 
            "linkage_group": 0, 
            "plant": plant.resource_uri, 
            "position" : 0, 
             "owner": "/api/v1/user/" + $scope.user_id 
            }, 
        function (value) {
            // add the returned created locus values to the plant
            plant.loci.push({
                name: value.name,
                locus_type: value.locus_type,
                linkage_group: value.linkage_group,
                plant: value.plant,
                crosses: value.crosses, 
                owner: value.owner,
                position: value.position,
                resource_uri: value.resource_uri
            });
            // add the new locus to the cross_data lists it needs to be in S
            _.each($scope.scheme.crosses, function(cross){
                //if(_.$scope.cross_data[cross.resource_uri])
            });
        });
    };
    // function to remove a locus from the scheme & any crosses
    $scope.remove_locus = function (locus, plant) {
        Locus.delete({id: locus.id}, function(value) { 
            console.log(value);
            _.each($scope.scheme.crosses, function(cross){ 
                $scope.cross_data[cross.resource_uri].poss_loci = 
                _.without($scope.cross_data[cross.resource_uri].poss_loci, locus);
                    cross.loci = _.without(cross.loci, locus.resource_uri);
                });

            plant.loci = _.reject(plant.loci, function (item){ 
                return item === locus; 
            });           
        });
    };

    // function to remvoe a locus from a cross
    $scope.remove_cross_locus = function (cross, locus) {
        cross.loci = _.reject(cross.loci, function(l){
            return locus == l;
        });
    }

    // function to remove a cross from the scheme & parent array
    $scope.remove_cross = function (cross) {
        $scope.poss_parents = _.reject($scope.poss_parents, function (item){ return item.resource_uri == cross.resource_uri}); 

        $scope.scheme.crosses = _.reject($scope.scheme.crosses, function (item){ return item.resource_uri == cross.resource_uri}); 
        $scope.to_del.push(cross.resource_uri);
    };

    // function to add a new cross to a scheme
    $scope.add_cross = function ( scheme ) {
        scheme.crosses.push({"name": null, "left_cross_parent": null, "right_cross_parent": null, "left_plant_parent": null, "right_plant_parent": null, "protocol_zygosity": null, "loci": []});
    };


    // function to select the right item in an options list of plants / crosses 
    $scope.isSelected = function ( item, option ) { 
        if (item != option || item == null || option == null)
            return false; 
        else
            return true; 
    };
  

}
