angular.module('schemecon', ['ngResource']).
    factory('Scheme', function($resource) {
        var Scheme = $resource('../../api/v1/scheme/:id/',
            {update: { method: 'PUT' }
        });
    return Scheme;
});
