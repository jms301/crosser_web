angular.module('crosserFilters', []).filter('loci', function() {
    return function(scheme, locus_url) {
        var result = _.map(scheme.plants, function(plant){return plant.loci;});
        result = [].concat.apply([], result);
        result = _.reduce(result, function(out, locus){
            return (locus.resource_uri == locus_url) ? locus.name : out;}
            , "???");
        return result;
    };
});
