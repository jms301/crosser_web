window.TastypieModel = Backbone.RelationalModel.extend({
    base_url: function() {
      var temp_url = Backbone.Model.prototype.url.call(this);
      return (temp_url.charAt(temp_url.length - 1) == '/' ? temp_url : temp_url+'/');
    },

    url: function() {
      return this.base_url();
    }
});

window.TastypieCollection = Backbone.Collection.extend({
    parse: function(response) {
        this.recent_meta = response.meta || {};
        return response.objects || response;
    }
});

var Plan = TastypieModel.extend({
    initialize: function() { },
    urlRoot: '/api/v1/plan/',
    name: function() { },

    defaults: {
        "name":  "Plan Name"
    },
    
    relations: [{
        type: Backbone.HasOne, 
        key: 'species',
        relatedModel: 'Species',
        autoFetch: true,
        reverseRelation: {
            key: 'plan',
            includeInJSON: 'id',
            type: Backbone.HasOne
            // 'relatedModel' is automatically set to 'Zoo'; the 'relationType' to 'HasOne'.
        }
    }]
});

var Species = TastypieModel.extend({
    initializse: function() { },
    urlRoot: '/api/v1/species/',
    name: function() { },

  defaults: {
    "name":  "Species Name"
  }
});

// TESTING FETCHING
cunning_plan = new Plan();
cunning_plan.set("id", 1);
cunning_plan.set("name", 'bibble');
cunning_plan.fetch();
console.log(cunning_plan);
// TESTING RELATIONS
//cunning_plan = new Plan({name: 'test plan', conf_recombination_prob: 13, conf_tolerance: 24, conf_chunk_size: 10});
//console.log(cunning_plan.get('name') );
//beantype = new Species({name: 'tasty bean', arrayofshit: "11,22,44,22,11,10", plan: cunning_plan});
//console.log(cunning_plan.get('species').get('name'));
//console.log(beantype.get('plan').get('name'));



