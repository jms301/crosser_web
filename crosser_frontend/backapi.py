from tastypie import fields
from tastypie.resources import ModelResource 
from tastypie.authorization import ReadOnlyAuthorization
from models import Scheme, Species, Cross, Plant, Locus, System, Output

class BackSchemeResource(ModelResource):

    species = fields.ToOneField('crosser_frontend.backapi.BackSpeciesResource', 'species', full=True, related_name='scheme', null=True)
    system = fields.ToOneField('crosser_frontend.backapi.BackSystemResource', 'system', full=True, related_name='scheme', null=True)
    plants = fields.ToManyField('crosser_frontend.backapi.BackPlantResource', 'plants', full=True, related_name='scheme', null=True)
    crosses = fields.ToManyField('crosser_frontend.backapi.BackCrossResource', 'crosses', full=True, related_name='scheme', null=True)
    outputs = fields.ToManyField('crosser_frontend.backapi.BackOutputResource', 
        'outputs', full=True, related_name='scheme', null=True)

    class Meta:
        queryset = Scheme.objects.filter(frozen=True)
        authorization = ReadOnlyAuthorization()
        resource_name = 'scheme'
        always_return_data=True

    def dehydrate(self, bundle): 
        crosses = {} 
        plants = {} 
        loci = {} 

        #setup hashes that map from resource_uri to name so that we can
        #convert the output to use names instead of resource_uri (dirty but
        #it's the requeted feature) 

        for plant in bundle.data['plants']:
            plants[plant.data['resource_uri']] = plant.data['name']
            for locus in plant.data['loci']:
                loci[locus.data['resource_uri']] = locus.data['name']
                if locus.data['locus_type'] == Locus.TRAIT:
                    locus.data['type'] = 'Trait'
                elif locus.data['locus_type'] == Locus.MARKER:
                    locus.data['type'] = 'Marker'
                del locus.data['locus_type']
 
        for cross in bundle.data['crosses']:
            crosses[cross.data['resource_uri']] = cross.data['name']

        for cross in bundle.data['crosses']:
            val = cross.data['right_plant_parent'] 
            if val != None: 
                cross.data['right_plant_parent'] = plants[cross.data['right_plant_parent']]

            val = cross.data['left_plant_parent'] 
            if val != None: 
                cross.data['left_plant_parent'] = plants[cross.data['left_plant_parent']]

            val = cross.data['left_cross_parent'] 
            if val != None: 
                cross.data['left_cross_parent'] = crosses[cross.data['left_cross_parent']]

            val = cross.data['right_cross_parent'] 
            if val != None: 
                cross.data['right_cross_parent'] = crosses[cross.data['right_cross_parent']]
            crosses[cross.data['resource_uri']] = cross.data['name']
            for i, locus in enumerate(cross.data['loci']):
                cross.data['loci'][i] = loci[locus]
        
        # map the left_cross_parent and left_plant_parent fields into a single 
        # left_parent field & Expand the Zygosity field
        for cross in bundle.data['crosses']:
            if cross.data['left_plant_parent']:
                cross.data['left_parent'] = cross.data['left_plant_parent']
            else:
                cross.data['left_parent'] = cross.data['left_cross_parent']

            if cross.data['right_plant_parent']:
                cross.data['right_parent'] = cross.data['right_plant_parent']
            else:
                cross.data['right_parent'] = cross.data['right_cross_parent']

            del cross.data['right_plant_parent']
            del cross.data['left_plant_parent']
            del cross.data['right_cross_parent']
            del cross.data['left_cross_parent']

            if cross.data['protocol_zygosity'] == Cross.HETEROZYGOUS:
                cross.data['protocol_zygosity'] = 'Heterozygous'
            elif cross.data['protocol_zygosity'] == Cross.HOMOZYGOUS:
                cross.data['protocol_zygosity'] = 'Homozygous'
                

        #output an array of numbers rather than a string of comma seperated
        # numbers.    
        if bundle.data['species']: 
            bundle.data['species'].data['chromosome_lengths'] = map(
                int, bundle.data['species'].data['chromosome_lengths'].
                split(','))
        
        return bundle    


class BackSpeciesResource(ModelResource): 
    class Meta: 
        queryset = Species.objects.all()
        authorization = ReadOnlyAuthorization()
        resource_name = 'scheme' 
        always_return_data=True
 
class BackSystemResource(ModelResource):
    scheme = fields.ForeignKey(BackSchemeResource, 'scheme')
    class Meta:
        queryset = System.objects.filter(frozen=True)
        authorization = ReadOnlyAuthorization()
        resource_name = 'system'
        always_return_data=True


class BackOutputResource(ModelResource):
    scheme = fields.ForeignKey(BackSchemeResource, 'scheme')

    class Meta: 
        queryset = Output.objects.filter(frozen=True)
        authorization = ReadOnlyAuthorization()
        resource_name = 'output'
        always_return_data=True

class BackPlantResource(ModelResource):
    loci = fields.ToManyField('crosser_frontend.backapi.BackLocusResource', 'loci', full=True, related_name='plant', null=True)
    class Meta:
        queryset = Plant.objects.filter(frozen=True)
        authorization = ReadOnlyAuthorization()
        resource_name = 'plant'
        always_return_data=True

class BackLocusResource(ModelResource): 

    class Meta:
        queryset = Locus.objects.filter(frozen=True)
        authorization = ReadOnlyAuthorization()
        resource_name = 'locus'
        always_return_data=True

class BackCrossResource(ModelResource):
    loci = fields.ToManyField('crosser_frontend.backapi.BackLocusResource', 'loci', null=True)
    left_plant_parent = fields.ForeignKey(BackPlantResource, 'left_plant_parent', null=True, blank=True)
    right_plant_parent = fields.ForeignKey(BackPlantResource, 'right_plant_parent', null=True, blank=True)

    left_cross_parent = fields.ForeignKey('self', 'left_cross_parent', null=True, blank=True)

    right_cross_parent = fields.ForeignKey('self', 'right_cross_parent', null=True, blank=True)
    
    class Meta: 
        queryset = Cross.objects.filter(frozen=True)
        authorization = ReadOnlyAuthorization()
        resource_name = 'cross'
        always_return_data=True


