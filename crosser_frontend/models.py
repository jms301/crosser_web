from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import subprocess

# Create your models here.
class Species(models.Model):
    name = models.CharField(max_length = 100)
    chromosome_lengths = models.CommaSeparatedIntegerField(max_length = 100)

    class Meta:
        verbose_name_plural = "Species"

    def __unicode__(self): 
        return self.name

class Scheme(models.Model):
    owner = models.ForeignKey(User) 
    name = models.CharField(max_length = 100)
    species = models.ForeignKey(Species, related_name='+', null=True)
    frozen = models.BooleanField(default = False)

    def freeze(self, version): 

        # detect the current version
        # attempt to save static_dir/cross_id/version
        # attempt to create status object
        # load status object page. 
        copy = self.copy()
        print "NEW SCHEME AT:"
        print copy.id 
        return 0 

    def copy(self, freeze=True):
        new_scheme = Scheme(name = self.name, frozen=freeze, 
                            species=self.species, owner=self.owner)
        new_scheme.save()

        new_system = System(owner=self.owner, 
            scheme=new_scheme,
            frozen = freeze,
            convergence_fewest_plants = self.system.convergence_fewest_plants,
            convergence_tolerance = self.system.convergence_tolerance,
            convergence_chunk_size = self.system.convergence_chunk_size ) 
        new_system.save()



        locus_map = {}
        cross_map = {}
        plant_map = {}

        for output in self.outputs.all().order_by('id'): 
            new_output = Output(owner=output.owner, frozen=freeze, 
                scheme=new_scheme, output_type = output.output_type, 
                data = output.data)
            new_output.save()

        for plant in self.plants.all().order_by('id'):
            plant_map[plant] = Plant(owner=plant.owner, name=plant.name, 
                scheme = new_scheme, frozen = freeze)
            plant_map[plant].save()

            for locus in plant.loci.all().order_by('id'):
                locus_map[locus] = Locus(owner=locus.owner, name = locus.name,
                    locus_type = locus.locus_type, 
                    linkage_group = locus.linkage_group,
                    position = locus.position,
                    plant = plant_map[plant],
                    frozen = freeze)
                locus_map[locus].save()
      
        for cross in self.crosses.all().order_by('id'): 
            new_cross = Cross(owner=cross.owner, name = cross.name, 
                protocol_zygosity = cross.protocol_zygosity,
                scheme = new_scheme, frozen = freeze)
            new_cross.save()

            for locus in cross.loci.all():
                new_cross.loci.add(locus_map[locus])
            cross_map[cross] = new_cross
             
        for cross in self.crosses.all(): 
            if cross.left_cross_parent: 
                cross_map[cross].left_cross_parent = cross_map[cross.left_cross_parent]

            if cross.right_cross_parent:
                cross_map[cross].right_cross_parent = cross_map[cross.right_cross_parent]

            if cross.left_plant_parent:
                cross_map[cross].left_plant_parent = plant_map[cross.left_plant_parent]
            if cross.right_plant_parent:
                cross_map[cross].right_plant_parent = plant_map[cross.right_plant_parent]
            cross_map[cross].save() 

        return new_scheme

    def __unicode__(self): 
        return self.name

class SchemeStatus(models.Model):
    TO_RUN = 'TR'
    NOW_RUNNING = 'NR'
    FINISHED_ERR = 'FR' 
    FINISHED_SUCC = 'FS' 

    STATUS_CHOICES = (
        (TO_RUN, 'To Run'),
        (NOW_RUNNING, 'Now Running'),
        (FINISHED_ERR, 'Ended with Error'),
        (FINISHED_SUCC, 'Finished in Success'),
    ) 

    status = models.CharField(max_length=2,
                                   choices = STATUS_CHOICES,
                                    default = TO_RUN)

    owner = models.ForeignKey(User)
    version = models.IntegerField()
    scheme = models.ForeignKey(Scheme, related_name='statuses')
 
    def __unicode__(self):
        return self.scheme.name + " status" 


class System(models.Model):
    owner = models.ForeignKey(User) 
    convergence_chunk_size = models.IntegerField()
    convergence_tolerance = models.FloatField()
    convergence_fewest_plants = models.IntegerField()
    scheme = models.OneToOneField(Scheme, related_name='system', null=True)
    frozen = models.BooleanField(default = False)

class Output(models.Model):
    owner = models.ForeignKey(User) 
    scheme = models.ForeignKey(Scheme, related_name='outputs')
    frozen = models.BooleanField(default = False)

    LOCI_COMP = 'Lc'
    PROP_DIST = 'Pd'
    SUCC_PROB = 'Sp'
    CROS_COMP = 'Cc'

    CONT_CHOICES = (
        (CROS_COMP, 'cross_composition'),
        (SUCC_PROB, 'success_probability'),
        (LOCI_COMP, 'loci_composition'),
        (PROP_DIST, 'proportion_distribution'),
    ) 

    output_type = models.CharField(max_length=2,
                                    choices = CONT_CHOICES,
                                    default = CROS_COMP)

    data = models.CharField(max_length=200, null=True)

    def __unicode__(self): 
        return self.scheme.name + " : output"  

class Plant(models.Model):
    owner = models.ForeignKey(User) 
    name = models.CharField(max_length = 100)
    scheme = models.ForeignKey(Scheme, related_name='plants')
    frozen = models.BooleanField(default = False)

    def __unicode__(self): 
        return self.name

class Locus(models.Model):
    owner = models.ForeignKey(User) 
    TRAIT = 'Tr'
    MARKER = 'Ma'
    TYPE_CHOICES = (
        (TRAIT, 'Trait'),
        (MARKER, 'Marker'),
    )
    name = models.CharField(max_length = 100)
    locus_type = models.CharField(max_length=2, 
                                choices = TYPE_CHOICES, 
                                default=TRAIT)
    linkage_group = models.IntegerField(null=True)
    position = models.IntegerField(null=True)
    
    plant =  models.ForeignKey(Plant, related_name='loci')
    frozen = models.BooleanField(default = False)

    def __unicode__(self): 
        return self.name

    class Meta:
        verbose_name_plural = "Loci"

class Cross(models.Model):
    owner = models.ForeignKey(User) 
    HETEROZYGOUS = 'He'
    HOMOZYGOUS = 'Ho' 
    ZYGOSITY_CHOICES = (
        (HETEROZYGOUS, 'Heterozygous'),
        (HOMOZYGOUS, 'Homozygous'),
    )

    name = models.CharField(max_length = 100)
    loci = models.ManyToManyField(Locus, null=True, related_name='crosses')
    scheme =  models.ForeignKey(Scheme, related_name='crosses')
    frozen = models.BooleanField(default = False)

    left_plant_parent = models.ForeignKey(Plant, related_name='+', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    left_cross_parent = models.ForeignKey('Cross', related_name='+', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    right_plant_parent = models.ForeignKey(Plant, related_name='+', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    right_cross_parent = models.ForeignKey('Cross', related_name='+', null=True, blank=True, default=None, on_delete=models.SET_NULL)
    protocol_zygosity = models.CharField(max_length=2, 
                                choices = ZYGOSITY_CHOICES, 
                                default=HOMOZYGOUS)
    def __unicode__(self): 
        return self.name

    class Meta:
        verbose_name_plural = "Crosses"

   
#TODO: 
# How long can the species cromosome length comma seperated list be? 
#( what is 4 x max chromosome number??)
#
