from tastypie import fields
from tastypie.resources import ModelResource 
from tastypie.authentication import SessionAuthentication
from models import Scheme, Species, Cross, Plant, Locus

class LocusResource(ModelResource): 
    class Meta:
        queryset = Locus.objects.all()
        authentication = SessionAuthentication()
        resource_name = 'locus'
    def dehydrate_locus_type(self, bundle):
        return bundle.obj.get_locus_type_display()

class PlantResource(ModelResource):
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci', full=True)
    class Meta:
        queryset = Plant.objects.all()
        authentication = SessionAuthentication()
        resource_name = 'plant'

class CrossResource(ModelResource):
    loci = fields.ToManyField('crosser_frontend.api.LocusResource', 'loci' )
    left_plant_parent = fields.ForeignKey(PlantResource, 'left_plant_parent', null=True, blank=True)
    right_plant_parent = fields.ForeignKey(PlantResource, 'right_plant_parent', null=True, blank=True)
    left_cross_parent = fields.ForeignKey(PlantResource, 'left_cross_parent', null=True, blank=True)
    right_cross_parent = fields.ForeignKey(PlantResource, 'right_cross_parent', null=True, blank=True)
    

    class Meta: 
        queryset = Cross.objects.all()
        authentication = SessionAuthentication()
        resource_name = 'cross'
 
    def dehydrate_protocol_zygosity(self, bundle):
        return bundle.obj.get_protocol_zygosity_display()


class SpeciesResource(ModelResource):
    class Meta:
        queryset = Species.objects.all()
        authentication = SessionAuthentication()
        resource_name = 'species'

class SchemeResource(ModelResource):
    plants = fields.ToManyField('crosser_frontend.api.PlantResource', 'plants', full=True)
    species = fields.ForeignKey(SpeciesResource, 'species', full=True)
    crosses = fields.ToManyField('crosser_frontend.api.CrossResource', 'crosses', full=True)

    class Meta:
        queryset = Scheme.objects.all()
        authentication = SessionAuthentication()
        resource_name = 'scheme'

