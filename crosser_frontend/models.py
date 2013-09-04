from django.db import models
from django.contrib.auth.models import User

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

    def __unicode__(self): 
        return self.name


class System(models.Model):
    owner = models.ForeignKey(User) 
    convergence_chunk_size = models.IntegerField()
    convergence_tolerance = models.FloatField()
    scheme = models.OneToOneField(Scheme, related_name='system', null=True)

class Output(models.Model):
    owner = models.ForeignKey(User) 
    scheme = models.ForeignKey(Scheme, related_name='outputs')

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
