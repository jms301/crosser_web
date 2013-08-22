angular.module('schemecon', ['ngResource']).
    config(["$httpProvider", function(provider) {
        provider.defaults.headers.common['X-CSRFToken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }]).
    factory('Scheme', function($resource) {
        var Scheme = $resource('../../api/v1/scheme/:id/', {},
            {update: { method: 'PUT'}});

        Scheme.prototype.update = function(cb) {
           return Scheme.update({id: this.id},this);
        };

        return Scheme;
    })
    .factory('Cross', function($resource) { 
        var Cross = $resource('../../api/v1/cross/:id', {},
        {});
        return Cross;
    })
    .factory('Locus', function($resource) { 
        var Locus = $resource('../../api/v1/locus/:id', {},
        {});
        return Locus;
    })
    .factory('Plant', function($resource) { 
        var Plant = $resource('../../api/v1/plant/:id', {},
        {});
        return Plant;
    }).factory('Output', function($resource) { 
        var Output = $resource('../../api/v1/output/:id', {},
        {});
        return Output;
    }).factory('Species', function($resource) {
        var Species = $resource('../../api/v1/species/', {},
        {});
        return Species;
    });
