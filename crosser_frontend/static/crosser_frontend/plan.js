angular.module('plan', []).
    config(function($interpolateProvider){
        $interpolateProvider.startSymbol('{[{').endSymbol('}]}')
    });

function PlanCtrl($scope) { 
    $scope.plan = {};  

    $scope.plan.plants = [
    {
      "name": "PreferredVariety",
      "loci": [
        
      ]
    },
    {
      "name": "Donor",
      "loci": [
        {
          "name": "DonorTrait",
          "type": "Trait",
          "linkageGroup": 2,
          "position": 100
        },{
          "name": "DonorTrait2",
          "type": "Trait",
          "linkageGroup": 4,
          "position": 30
        },{
          "name": "DonorTrait",
          "type": "Trait",
          "linkageGroup": 5,
          "position": 20
        }

        ]
        }
    ];

    $scope.addLoci =   function ( plant ) {
        plant.loci.push({"name": null, "type": null, "linkageGroup": null});
        console.log(plant);
    };
}
