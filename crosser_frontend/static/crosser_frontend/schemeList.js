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
                "system": {
                    "owner": "/api/v1/user/" + $scope.user_id,
                    "convergence_chunk_size": 0,
                    "convergence_tolerance": 0,
                    "convergence_fewest_plants": 100 
                } 
            }, 
        function (scheme) { 
            window.location.href = $scope.get_url(scheme);
        });        
    }; 

   $scope.remove_scheme = function (scheme) {
        id = scheme.resource_uri.split('/').pop();
        if(id)
        Scheme.delete({id: id}, function(value) { 
            $scope.schemes.objects = _.reject($scope.schemes.objects, 
                function (item) { return item.resource_uri == scheme.resource_uri}); 
            });
    };
   
}
