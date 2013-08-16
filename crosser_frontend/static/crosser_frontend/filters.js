angular.module('crosserFilters', [])
//Filter to remove un-viable parents from cross parents dropdowns
.filter('parents', function(){
    return function(parents, current_cross, descendants) {
        exclude = descendants.concat([current_cross]);
        value =  _.reject(parents, function(item){

            return _.contains(exclude, item.resource_uri);
        }); 
        return value;
    };
})
.filter('without_loci', function() {
    return function(loci_list, cross_loci) {
        return _.reject(loci_list, function(loci){
            return _.contains(cross_loci, loci.resource_uri);
        });
    };
});
