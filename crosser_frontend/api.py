from tastypie import fields
from tastypie.resources import ModelResource 
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from crosser_frontend.auth import UserAuthorization
from models import Scheme, Species, Cross, Plant, Locus
from django.contrib.auth.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        list_allowed_methods = ['get']
        fields = ['username']
    
class SpeciesResource(ModelResource):
    class Meta:
        queryset = Species.objects.all()
        list_allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = ReadOnlyAuthorization()
        resource_name = 'species'

class SchemeResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    plants = fields.ToManyField('crosser_frontend.api.PlantResource', 'plants', full=True, related_name='scheme')
    species = fields.ForeignKey(SpeciesResource, 'species')
    crosses = fields.ToManyField('crosser_frontend.api.CrossResource', 'crosses', full=True, related_name='scheme')

    class Meta:
        queryset = Scheme.objects.all()
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'scheme'
        always_return_data=True

class PlantResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci', full=True, related_name='plant')
    scheme = fields.ForeignKey(SchemeResource, 'scheme')
    class Meta:
        queryset = Plant.objects.all()
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'plant'
        always_return_data=True

class LocusResource(ModelResource): 
    owner = fields.ForeignKey(UserResource, 'owner')    
    plant = fields.ForeignKey(PlantResource, 'plant', null=True)
    crosses = fields.ToManyField('crosser_frontend.api.CrossResource', 'crosses' , null=True)

    class Meta:
        queryset = Locus.objects.all()
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'locus'
        always_return_data=True


class CrossResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci')
    left_plant_parent = fields.ForeignKey(PlantResource, 'left_plant_parent', null=True, blank=True)
    right_plant_parent = fields.ForeignKey(PlantResource, 'right_plant_parent', null=True, blank=True)

    left_cross_parent = fields.ForeignKey('self', 'left_cross_parent', null=True, blank=True)

    right_cross_parent = fields.ForeignKey('self', 'right_cross_parent', null=True, blank=True)
    scheme = fields.ForeignKey(SchemeResource, 'scheme')
    
    class Meta: 
        queryset = Cross.objects.all()
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'cross'
        always_return_data=True
 
