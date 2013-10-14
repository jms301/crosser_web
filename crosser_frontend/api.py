from tastypie import fields
from tastypie.resources import ModelResource 
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import ReadOnlyAuthorization
from crosser_frontend.auth import UserAuthorization
from models import Scheme, Species, Cross, Plant, Locus, System, Output
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
    species = fields.ForeignKey(SpeciesResource, 'species', null=True)
    owner = fields.ForeignKey(UserResource, 'owner')    
 
    system = fields.ToOneField('crosser_frontend.api.SystemResource', 'system', full=True, related_name='scheme', null=True)
    plants = fields.ToManyField('crosser_frontend.api.SPlantResource', 'plants', full=True, related_name='scheme', null=True)
    crosses = fields.ToManyField('crosser_frontend.api.SCrossResource', 'crosses', full=True, related_name='scheme', null=True)
    outputs = fields.ToManyField('crosser_frontend.api.SOutputResource', 
        'outputs', full=True, related_name='scheme', null=True)

    class Meta:
        queryset = Scheme.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'scheme'
        always_return_data=True

class SystemResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    

    class Meta:
        queryset = System.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'system'
        always_return_data=True

class SOutputResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    

    class Meta: 
        queryset = Output.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'output'
        always_return_data=True

class OutputResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    scheme = fields.ForeignKey(SchemeResource, 'scheme')

    class Meta: 
        queryset = Output.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'output'
        always_return_data=True

#Dupe of the plant resource to allow faster saving of whole schemes.
class SPlantResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci', full=True, related_name='plant', null=True)
    class Meta:
        queryset = Plant.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'plant'
        always_return_data=True

class PlantResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci', full=True, related_name='plant', null=True)
    scheme = fields.ForeignKey(SchemeResource, 'scheme')

    class Meta:
        queryset = Plant.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'plant'
        always_return_data=True

#Dupe of the locus resource to allow faster saving of whole schemes.
class SLocusResource(ModelResource): 
    owner = fields.ForeignKey(UserResource, 'owner')    

    class Meta:
        queryset = Locus.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'locus'
        always_return_data=True


class LocusResource(ModelResource): 
    owner = fields.ForeignKey(UserResource, 'owner')    
    plant = fields.ForeignKey(PlantResource, 'plant', null=True)

    class Meta:
        queryset = Locus.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'locus'
        always_return_data=True

#Dupe of the cross resource to allow faster saving of whole schemes.
class SCrossResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci', null=True)
    left_plant_parent = fields.ForeignKey(PlantResource, 'left_plant_parent', null=True, blank=True)
    right_plant_parent = fields.ForeignKey(PlantResource, 'right_plant_parent', null=True, blank=True)

    left_cross_parent = fields.ForeignKey('self', 'left_cross_parent', null=True, blank=True)

    right_cross_parent = fields.ForeignKey('self', 'right_cross_parent', null=True, blank=True)
    
    class Meta: 
        queryset = Cross.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'cross'
        always_return_data=True


class CrossResource(ModelResource):
    owner = fields.ForeignKey(UserResource, 'owner')    
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci', null=True)
    left_plant_parent = fields.ForeignKey(PlantResource, 'left_plant_parent', null=True, blank=True)
    right_plant_parent = fields.ForeignKey(PlantResource, 'right_plant_parent', null=True, blank=True)

    left_cross_parent = fields.ForeignKey('self', 'left_cross_parent', null=True, blank=True)

    right_cross_parent = fields.ForeignKey('self', 'right_cross_parent', null=True, blank=True)
    scheme = fields.ForeignKey(SchemeResource, 'scheme')
    
    class Meta: 
        queryset = Cross.objects.filter(frozen=False)
        authentication = SessionAuthentication()
        authorization = UserAuthorization()
        resource_name = 'cross'
        always_return_data=True


