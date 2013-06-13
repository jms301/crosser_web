window.TastypieModel = Backbone.Model.extend({
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
    "name":  "Plan Name",
    "entree":     "ravioli",
    "dessert":    "cheesecake"
  }
});

cunning_plan = new Plan();

cunning_plan.set("id", 1);
//cunning_plan.set("name", 'bibble');
cunning_plan.fetch();

