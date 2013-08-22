angular.module('schemeList', ['schemecon']).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });
   
function SchemeListCtrl($scope, Scheme, $location) {

    /**********************************************************
        HOUSE KEEPING  - load schemes 

    **********************************************************/
    // get schemes 
    $scope.schemes = Scheme.get();
    $scope.user_id = document.getElementsByName('userid')[0].value;

    $scope.get_url = function(scheme) { 
        return "/cross/" + scheme.id + '/';
    }; 

    $scope.new_scheme = function() { 

        Scheme.save(
            {
                "name": null,
                "owner": "/api/v1/user/" + $scope.user_id,
                "chunk_size": 0,
                "recombination_prob": 0,
                "tolerance": 0
            }, 
        function (scheme) { 
            window.location.href = $scope.get_url(scheme);
        });        
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
                owner: value.owner,
                scheme: scheme.resource_uri,
                loci: [],
                resource_uri: value.resource_uri
            });
            // re-calculate the local data possible parents list 
            $scope.generate_parents();
        });
    };

}
