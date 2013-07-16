angular.module('schemecon', ['ngResource']).
    config(["$httpProvider", function(provider) {
        provider.defaults.headers.common['X-CSRFToken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    }]).
    config(["$httpProvider", function(provider) {
        provider.defaults.headers.patch = provider.defaults.headers.put;
    }]).
    factory('Scheme', function($resource) {
        var Scheme = $resource('../../api/v1/scheme/:id/', {},
            {update: { method: 'PUT'},
            patch: {method: 'PATCH'}});

        Scheme.prototype.update = function(cb) {
            return Scheme.update({id: this.id},this,cb);
        };

        Scheme.prototype.patch = function(cb) {
            return Scheme.patch({},cb);
        };

        return Scheme;
    })
    .factory('Cross', function($resource) { 
        var Crosses = $resource('../../api/v1/crosses/', {},
        {patch: {method: 'PATCH'}});
    }
    .factory('Locus', function($resource) { 
        var Crosses = $resource('../../api/v1/locus/', {},
        {patch: {method: 'PATCH'}});
    }
    .factory('Plant', function($resource) { 
        var Crosses = $resource('../../api/v1/plant/', {},
        {patch: {method: 'PATCH'}});
    }
    .factory('Species', function($resource) {
        var Species = $resource('../../api/v1/species/', {},
            {});
        return Species;
    });
