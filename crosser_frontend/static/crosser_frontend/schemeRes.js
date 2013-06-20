angular.module('schemecon', ['ngResource']).
    factory('Scheme', function($resource) {
        var Scheme = $resource('../../api/v1/scheme/:id/', {},
            {update: { method: 'PUT'}});

        Scheme.prototype.update = function(cb) {
            return Scheme.update({id: this.id},
            angular.extend({}, this, {}), cb);
        };

        return Scheme;
    });
