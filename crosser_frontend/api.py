from tastypie import fields
from tastypie.resources import ModelResource 
from tastypie.authentication import SessionAuthentication
from models import Plan, Species

class SpeciesResource(ModelResource):
    class Meta:
        queryset = Species.objects.all()
        authentication = SessionAuthentication()
        resource_name = 'species'

class PlanResource(ModelResource):
    species = fields.ForeignKey(SpeciesResource, 'species', full=True)

    class Meta:
        queryset = Plan.objects.all()
        authentication = SessionAuthentication()
        resource_name = 'plan'

