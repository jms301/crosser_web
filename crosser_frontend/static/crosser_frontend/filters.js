angular.module('crosserFilters', [])
//Filter to remove un-viable parents from cross parents dropdowns
//TODO remove the option to set the parent as a child/grandchild etc
.filter('parents', function(){
    return function(parents, current_cross) {
        return _.reject(parents, function(item){return item.resource_uri == current_cross}); 
    };
});
//.filter('loci', function() {
    //return function(plants, locus_url) {
        //var result = _.map(plants, function(plant){return plant.loci;});
        //result = [].concat.apply([], result);
        //result = _.reduce(result, function(out, locus){
            //return (locus.resource_uri == locus_url) ? locus.name : out;}
            //, "???");
        //return result;
    //};
//});
