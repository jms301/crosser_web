/************************
Data Structure used in this controller:

$scope.scheme - The whole scheme object as returned by tastypie
$scope.species - a list of species names & their genome array fetched from tastypie.
$scope.quality - object holding the 'quality' drop down data.
                 Includes:
                    * 'state' value of current state 
                    * 'opts' array for the drop down options & 
                        their related values.

$scope.output_data - object holding local data for the display of outputs, 
                    each key is the output resource_uri and holds: 
                    *   custom_type - either blank or a custom type that will
                        be subbed in for the output_type upon upload. 

$scope.cross_data - object holding local data for the display of crosses, 
                    each key is the cross resource_uri and holds:
                     *  left_parent & right_parent - the parent resource_uris 
                        can be a cross or a plant, 
                        This is used in the drop down to show what is
                        currently selected.
                        Kept in sync with right_cross_parent, right_plant_parent                        etc.
                        
                     *  ancestors - the plants, which are parents of this 
                        cross. Used to show the loci that this cross can select
                        for. 

                     *  descendants - the crosses which descend from this 
                        cross. Used to filter the parent drop down & prevent 
                        user from trying to create looping family trees
 
$scope.poss_parents  - a list of all possible parents (crosses & plants) 
                  each including a type variable for cross parent select 
                  drop down.

TODO: 

    * Put a floating save button always visible top right below login

    * on delete of a plant crosses will still let you add the loci of 
      that plant? 

    * Update to use the latest version of the JSON data structure.
    
    * Enforce constraints on the Loci to match the species array 
        (position / Linkage group).  
*************************/

angular.module('scheme', ['ui.bootstrap', 'schemecon', 'crosserFilters']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });
   
function PlanCtrl($scope, Scheme, Plant, Cross, Locus, Species, Output) { 
//, $location) {

    /**********************************************************
        HOUSE KEEPING  - load or make scheme starting state
            save the scheme when done. 

    **********************************************************/
    // set up the PlanController context
    $scope.plan_id = window.location.pathname.split("/")[2];
    $scope.user_id = document.getElementsByName('userid')[0].value;
    // set up a cross_data array (allows us to keep the JSON clean 
    // to msg the API)
    $scope.cross_data = {};
    $scope.output_data = {};

    // initialize quality data
    $scope.quality = {
        'state': -1,
        'opts' : [ 
            {'name': 'draft (very low)', 'id' : 0, 
                'chunk_size' : 1000,
                'tolerance' : 0.5,
                'fewest_plants': 10},
            {'name': 'low', 'id' : 1,
                'chunk_size' : 500,
                'tolerance' : 0.05,
                'fewest_plants': 100},
            {'name': 'high', 'id' : 2,
                'chunk_size' : 50,
                'tolerance' : 0.005,
                'fewest_plants': 500},
            {'name': 'custom', 'id' : -1} 
                
        ]
    };

    // pull down list of species
    // split into array of ints (starts as csv of ints)
    $scope.species = Species.get(function () {
        _.each($scope.species.objects, function(element, index, list) { 
            element.chromosome_lengths = _.map(element.chromosome_lengths.split(","), 
                function(num) { return parseInt(num, 10)});    
        });
    });
   
    // pull down the scheme for the scope
    $scope.scheme = Scheme.get({id: $scope.plan_id}, function () {
        // add in fake left_parent & right_parent properties to the crosses
        // this allows us to use convenient ng-options stuff in the frontend
        // the properties will be split out before saving.
        _.each($scope.scheme.crosses, $scope.create_cross_parents);
        // setup an array of plants 'ancestors' in cross_data so 
        // we can see which loci are available to add into a cross. 
        _.each($scope.scheme.crosses, $scope.build_ancestors);
        _.each($scope.scheme.outputs, $scope.build_output_data);

        $scope.update_quality();
        $scope.generate_parents();
        $scope.generate_children();
    });

    // update function 
    $scope.scheme_update = function (scheme) {
        scheme.update(); 
    };

    // process function
    $scope.process_scheme = function (proc_url) {
        msg = "Running crosses can take a long time (~5hrs) " 
            + "are you sure you want to continue?"
        outputs_msg = ""; 
        _.each($scope.scheme.outputs, function (outp) { 
            if(outp.data == null || outp.data.length < 2)
                outputs_msg = "You have outputs which don't specify what to output, delete them or specify donors / crosses to output" 
        });
        if($scope.scheme.plants.length != _.uniq(_.pluck($scope.scheme.plants, "name")).length)
            alert("Two of your plants have the same name, cross names must be unique")
        else if($scope.scheme.crosses.length != _.uniq(_.pluck($scope.scheme.crosses, "name")).length)
            alert("Two of your crosses have the same name, cross names must be unique")

        else if($scope.scheme.crosses.length == 0)
            alert("Your scheme has no crosses and cannot be processed");
        else if($scope.scheme.plants.length == 0)
            alert("Your scheme has no plants and cannot be processed");
        else if($scope.scheme.outputs.length == 0)
            alert("Your scheme has no outputs and cannot be processed");
        else if(outputs_msg != "") 
            alert(outputs_msg);
        else if($scope.scheme_form.$invalid) 
            alert("Your scheme is invalid, look for yellow or red items in the form?"); 
        else if(confirm(msg))
        {
            Scheme.update({id: $scope.scheme.id}, $scope.scheme, 
                function (s, header) { 
                    window.location = proc_url;
            });
        }
    };

 /**********************************************************
        LOCAL DATA - Functions for handling the local meta data 
        attached to the scheme data. 

    **********************************************************/

    $scope.update_quality = function () { 
        _.each($scope.quality.opts, function (opt) { 
            if($scope.scheme.system.convergence_tolerance == opt.tolerance &&
               $scope.scheme.system.convergence_chunk_size == opt.chunk_size &&
               $scope.scheme.system.convergence_fewest_plants == opt.fewest_plants) {
               $scope.quality.state = opt.id; 
            
        }
    });
    };

    $scope.set_quality = function(id) { 
        if (id != -1) { 
            opt = _.where($scope.quality.opts, {'id' :id })[0];
            $scope.scheme.system.convergence_tolerance = opt.tolerance;
            $scope.scheme.system.convergence_chunk_size = opt.chunk_size;
            $scope.scheme.system.convergence_fewest_plants = opt.fewest_plants;
        }
    }; 

    $scope.build_output_data = function (output) { 

        var crosses_type_list = 
        ['mean_cross_composition', 
         'success_probability'] 
        var donor_cross_type_list =  ['proportion_distribution']
        var cross_type_list =  ['loci_composition'] 

        if(_.contains(crosses_type_list, output.output_type)) {
            var data = {};
            try { 
                data = angular.fromJson(output.data);
            } catch(e) {
                data.crosses = []; 
            }
            $scope.output_data[output.resource_uri] = {output_type : output.output_type, data: data.crosses };
        } else if(_.contains(donor_cross_type_list, output.output_type)) {
            var data = {};
            try { 
                data = angular.fromJson(output.data);
            }catch(e){
                data.donor = ""; 
                data.cross = ""; 
            } 
            $scope.output_data[output.resource_uri] = {output_type : output.output_type, cross: data.cross, donor: data.donor};
        } else if(_.contains(cross_type_list, output.output_type)) {
            var data = {};
            try { 
                data = angular.fromJson(output.data);
            }catch(e){
                data.cross = ""; 
            } 
            $scope.output_data[output.resource_uri] = {output_type : output.output_type, cross: data.cross};
 
        } else {
            $scope.output_data[output.resource_uri] = {output_type : "Cm", data : null};
        }
    };

    $scope.generate_children = function () { 
        _.each($scope.cross_data, function (cross){
            cross.descendants = [];
        });

        _.each($scope.scheme.crosses, function(c) { 

            parents_todo = [];

            if(c.left_cross_parent)
                parents_todo.push(c.left_cross_parent);

            if(c.right_cross_parent)
                parents_todo.push(c.right_cross_parent);


            while(parents_todo.length > 0) { 
                current = parents_todo.pop();
                data = $scope.cross_data[current]; 

                data.descendants.push(c.resource_uri);
 
                if($scope.is_cross(data.left_parent))
                    parents_todo.push(data.left_parent);
                if($scope.is_cross(data.right_parent))
                    parents_todo.push(data.right_parent);
            }
        });
    };


    $scope.generate_parents = function() { 
            // setup array 'parents' that can be used to populate select options
            // the type field is used to provide groupings in the dropdown
            tmp_plants = _.filter($scope.scheme.plants, function (plant) {
                return (plant.name && plant.name.length != 0 &&
                        plant.name.match(/\S/));
            });

            tmp_cross = _.filter($scope.scheme.crosses, function (cross) {
                return (cross.name && cross.name.length != 0 &&
                        cross.name.match(/\S/));
            });

            tmp_plants =  _.map(tmp_plants, 
            function(plant, index, parents){
                return {type: "Plants", name: plant.name, 
                        resource_uri: plant.resource_uri};
            });
            tmp_cross = _.map(tmp_cross, 
            function(cross, index, parents){
                return {type: "Crosses", name: cross.name, 
                        resource_uri: cross.resource_uri};
            });
            $scope.poss_parents = tmp_cross.concat(tmp_plants); 
    };

    /**********************************************************
        DATA MANIPULATION  - load or make scheme starting state
            save the scheme when done. 

    **********************************************************/
 

    $scope.create_cross_parents = function(c, index, crosses) {
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

    // This is fairly  innefficient, be better to just update the single
    // cross or plant that has changed. Not worth fixing unless the performance
    // becomes an issue though.
    $scope.change_cross = function(cross) { 
        $scope.generate_parents();
    };

    $scope.change_plant = function(plant) { 
        $scope.generate_parents();
    };

    $scope.change_locus = function(locus) { 

    };

    $scope.change_output_type = function(output) {
        if($scope.output_data[output.resource_uri].output_type != "Cm")
            output.output_type = $scope.output_data[output.resource_uri].output_type;
        //else {  //This will wipe out the previously selected output type
                  // when a custom output is selected
        // output.output_type = "";
        //} 
    };

    $scope.change_output_data = function(output) { 
        var crosses_type_list = 
        ['mean_cross_composition', 
         'success_probability'] 
        var donor_cross_type_list =  ['proportion_distribution']
        var cross_type_list =  ['loci_composition'] 

        if(_.contains(crosses_type_list, output.output_type)) {
            output.data = "{\"crosses\": " +
                angular.toJson($scope.output_data[output.resource_uri].data) +
                "}";
        } else if(_.contains(donor_cross_type_list, output.output_type)) {
            output.data = "{\"donor\": \""+ 
                $scope.output_data[output.resource_uri].donor +
                          "\", \"cross\": \"" + 
                $scope.output_data[output.resource_uri].cross + "\" }"
        } else if(_.contains(cross_type_list, output.output_type)) { 
            output.data = "{\"cross\": \""+ 
                $scope.output_data[output.resource_uri].cross + 
                        "\" }"
            
        }

    }; 

    $scope.get_plant_by_uri = function (ref) { 
        return _.findWhere($scope.scheme.plants, {resource_uri: ref});
    };

    $scope.get_cross_by_uri = function (ref) {
        return _.findWhere($scope.scheme.crosses, {resource_uri: ref});
    };

    $scope.get_locus_by_uri = function (ref) { 
        loci = _.pluck($scope.scheme.plants, "loci"); 
        return _.findWhere(_.flatten(loci), {resource_uri: ref});
    };

    $scope.get_species = function () { 
        spec = _.findWhere($scope.species.objects, {resource_uri: $scope.scheme.species});
        if(spec)
            return spec.chromosome_lengths;
        else
            return [];
    };
 
    $scope.get_max_link_group = function () { 
        spec = $scope.get_species();
        if(spec.length !=0 )
            return (spec.length - 1);
        else
            return "??"; 
    };
 
    $scope.get_max_position = function( link_group ) { 
        spec = $scope.get_species();
        if(spec.length != 0 && link_group != null && link_group < spec.length )
            return spec[link_group - 1];
        else
            return "??";
    }; 

    // build the ancestor list for a cross. 
    $scope.build_ancestors = function(cross, index, crosses) {
        plants = [];
        parents = [];

        parents.push($scope.cross_data[cross.resource_uri].left_parent);
        parents.push($scope.cross_data[cross.resource_uri].right_parent);

        while(parents.length != 0) { 
            process = parents.pop();
            if(process == null)
                continue;
            if (process.indexOf('/api/v1/cross/')==0) { 
                c = $scope.get_cross_by_uri(process);
                parents.push($scope.cross_data[process].left_parent);
                parents.push($scope.cross_data[process].right_parent);
            } else if (process.indexOf('/api/v1/plant/')==0) {
                plants.push($scope.get_plant_by_uri(process));
            }
        }
        plants = _.uniq(plants);
        $scope.cross_data[cross.resource_uri].ancestors = plants;
    };

    $scope.add_all_cross_loci = function(c) { 
        c.loci = _.pluck(_.flatten(
            _.pluck($scope.cross_data[c.resource_uri].ancestors, "loci")),
        "resource_uri");
    
    }; 

    $scope.strip_invalid_loci = function(cross_uri) { 
        data = $scope.cross_data[cross_uri];

        _.each(data.descendants.concat([cross_uri]), function (uri) { 

            c = $scope.get_cross_by_uri(uri);
            data = $scope.cross_data[uri];

            loci = _.pluck(_.flatten(_.pluck(data.ancestors, 'loci'))
                , 'resource_uri');

            c.loci = _.reject(c.loci, function(cross_loci) {
                return !(_.contains(loci, cross_loci));
            });

        });
    }; 

    $scope.change_left_parent = function(cross) { 
        value = $scope.cross_data[cross.resource_uri].left_parent;
        if($scope.is_plant(value)) {
            cross.left_plant_parent = value;
            cross.left_cross_parent = null; 
        } else {
            cross.left_cross_parent = value; 
            cross.left_plant_parent = null;
        } 
        $scope.generate_children();
        //TODO this is very inefficient since the ancestors will
        // only have changed for the moved cross and its descendants
        _.each($scope.scheme.crosses, $scope.build_ancestors);
        $scope.strip_invalid_loci(cross.resource_uri);
    };
  
    $scope.change_right_parent = function(cross) { 
        value = $scope.cross_data[cross.resource_uri].right_parent;
        if($scope.is_plant(value)) {
            cross.right_plant_parent = value;
            cross.right_cross_parent = null; 
        } else {
            cross.right_cross_parent = value; 
            cross.right_plant_parent = null;
        } 
        $scope.generate_children();
        //TODO this is very inefficient since the ancestors will
        // only have changed for the moved cross and its descendants
        _.each($scope.scheme.crosses, $scope.build_ancestors);
        $scope.strip_invalid_loci(cross.resource_uri);

    };


    // Function to create a new plant, save it and if the save works
    // add it to the scheme
    $scope.add_plant = function ( scheme ) {
        Plant.save(
            {"name": null, 
            "scheme": scheme.resource_uri, 
            "owner": "/api/v1/user/" + $scope.user_id 
            }, 
        function (value) {
            // add the returned created locus values to the plant
            scheme.plants.push({
                name: null, 
                id: value.id,
                owner: value.owner,
                scheme: scheme.resource_uri, 
                loci: [],
                resource_uri: value.resource_uri
            });
            // re-calculate the local data possible parents list 
            $scope.generate_parents();
        });
    };

    // Function to create a new output, save it and if the save works
    // add it to the scheme
    $scope.add_output = function ( scheme ) {
        Output.save(
            {
            "output_type": null, 
            "data": null, 
            "owner": "/api/v1/user/" + $scope.user_id,
            "scheme": scheme.resource_uri
            }, 
        function (value) {
            // add the returned created locus values to the plant
            scheme.outputs.push({
                output_type: null, 
                data: null,
                id: value.id,
                owner: value.owner,
                scheme: scheme.resource_uri, 
                resource_uri: value.resource_uri,
            });
            $scope.output_data[value.resource_uri] = {custom_type:""};
        });
    };



    // function to create a new locus, save it and if the save works add it 
    //     to the plant
    $scope.add_locus =   function ( plant ) {
        Locus.save(
            {"name": null, 
            "locus_type": "Tr", 
            "linkage_group": null, 
            "plant": plant.resource_uri, 
            "position" : null, 
             "owner": "/api/v1/user/" + $scope.user_id 
            }, 
        function (value) {
            // add the returned created locus values to the plant
            plant.loci.push({
                name: value.name,
                id: value.id,
                locus_type: value.locus_type,
                linkage_group: value.linkage_group,
                plant: value.plant,
                crosses: value.crosses, 
                owner: value.owner,
                position: value.position,
                resource_uri: value.resource_uri
            });
        });
    };

    $scope.remove_plant = function (plant, scheme) { 
        id = plant.resource_uri.split('/').pop();
        if(id)
        Plant.delete({id: id}, function(value) { 
            // remove the plant from the scheme.
            $scope.scheme.plants = _.reject($scope.scheme.plants, 
                function (item){ 
                    return item === plant; 
                });           

            // remove any locus from crosses that reference them. 
            _.each(plant.loci, function (locus) { 
                _.each($scope.scheme.crosses, function(cross){ 
                    cross.loci = _.without(cross.loci, locus.resource_uri);
                });
            });

            // remove the now deleted plant from the possible parents 
            $scope.poss_parents = _.reject($scope.poss_parents, 
            function (item){
                 return item.resource_uri == plant.resource_uri
            }); 
         
        });
   };

    // function to remove a locus from a plant & any crosses
    $scope.remove_locus = function (locus, plant) {
        id = locus.resource_uri.split('/').pop();
        if(id)
        Locus.delete({id: id}, function(value) { 
            _.each($scope.scheme.crosses, function(cross){ 
                    cross.loci = _.without(cross.loci, locus.resource_uri);
                });

            plant.loci = _.reject(plant.loci, function (item){ 
                return item === locus; 
            });           
        });
    };

    // function to remvoe a locus from a cross
    $scope.remove_cross_locus = function (cross, locus) {
        cross.loci = _.without(cross.loci, locus); 
        Cross.save(cross);
    }

    // function to remove a cross from the scheme & parent array
    $scope.remove_cross = function (cross) {
        id = cross.resource_uri.split('/').pop();
        if(id)
            Cross.delete({id: id}, function(value) { 
                $scope.poss_parents = _.reject($scope.poss_parents, function (item){ return item.resource_uri == cross.resource_uri}); 

            $scope.scheme.crosses = _.reject($scope.scheme.crosses, function (item){ return item.resource_uri == cross.resource_uri}); 
        });
    };
   
    // function to remove an output from the scheme & output_data array
    $scope.remove_output = function (output) {
        id = output.resource_uri.split('/').pop();
        if(id) { 
            Output.delete({id: id}, function(value) {
                $scope.scheme.outputs = _.reject($scope.scheme.outputs, function (item){return item.resource_uri == output.resource_uri});
            
            delete $scope.output_data[output.resource_uri];
            });
        }
    };
         

    // function to create a new cross, save it and if the save works add it 
    //     to the scheme
    $scope.add_cross =   function ( ) {
        Cross.save(
            {"name": null, 
             "owner": "/api/v1/user/" + $scope.user_id,
             "right_cross_parent": null, 
             "left_plant_parent": null, 
             "right_plant_parent": null, 
             "left_plant_parent": null, 
             "protocol_zygosity": "He",
             "loci":[],
             "scheme": $scope.scheme.resource_uri 
            }, 
            
        function (value) {
            // add the returned created locus values to the plant
            cross = {
                id: value.id,
                name: null,
                right_cross_parent: null, 
                left_plant_parent: null, 
                right_plant_parent: null, 
                protocol_zygosity: "He", 
                loci: value.loci,
                owner: value.owner,
                resource_uri: value.resource_uri
            };

            $scope.scheme.crosses.push(cross);
            $scope.create_cross_parents(cross);
            $scope.generate_children();
         });
     };

    $scope.is_plant = function(uri) {
        if(uri && uri.split('/').length>3)
            return (uri.split('/')[3] == "plant");
        else 
            return false
    };

    $scope.is_cross = function(uri) { 
        if(uri && uri.split('/').length>3)
            return (uri.split('/')[3] == "cross");
        else 
            return false
    };

}
