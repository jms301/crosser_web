angular.module('crosserFilters', [])
//Filter to remove un-viable parents from cross parents dropdowns
//TODO remove the option to set the parent as a child/grandchild etc
.filter('parents', function(){
    return function(parents, current_cross) {
        return _.reject(parents, function(item){return item.resource_uri == current_cross}); 
    };
});
