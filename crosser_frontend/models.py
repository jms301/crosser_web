from django.db import models

# Create your models here.
class Species(models.Model):
    name = models.CharField(max_length = 100)
    chromosome_lengths = models.CommaSeparatedIntegerField(max_length = 100)
    
class Scheme(models.Model):
    conf_chunk_size = models.IntegerField( )
    conf_recombination_prob = models.IntegerField( )
    conf_tolerance = models.IntegerField( )
    name = models.CharField(max_length = 100)
    species = models.ForeignKey(Species, related_name='+')
    def __unicode__(self): 
        return self.name

class Plant(models.Model):
    name = models.CharField(max_length = 100)
    scheme = models.ForeignKey(Scheme, related_name='plants')

class Locus(models.Model):
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
    linkageGroup = models.IntegerField()
    position = models.IntegerField()
    plant =  models.ForeignKey(Plant, related_name='loci')

class Cross(models.Model):
    HETEROZYGOUS = 'He'
    HOMOZYGOUS = 'Ho' 
    ZYGOSITY_CHOICES = (
        (HETEROZYGOUS, 'Heterozygous'),
        (HOMOZYGOUS, 'Homozygous'),
    )
    name = models.CharField(max_length = 100)

    loci = models.ManyToManyField(Locus)

    scheme =  models.ForeignKey(Scheme, related_name='crosses')
    left_plant_parent = models.ForeignKey(Plant, related_name='+', null=True, blank=True, default=None)
    left_cross_parent = models.ForeignKey('Cross', related_name='+', null=True, blank=True, default=None)
    right_plant_parent = models.ForeignKey(Plant, related_name='+', null=True, blank=True, default=None)
    right_cross_parent = models.ForeignKey('Cross', related_name='+', null=True, blank=True, default=None)
    protocol_zygosity = models.CharField(max_length=2, 
                                choices = ZYGOSITY_CHOICES, 
                                default=HOMOZYGOUS)

class OutputSubject(models.Model):
    PREFVAR = 'Pv'
    FOOBAR = 'Fb'
    CONT_CHOICES = (
        (PREFVAR, 'PreferredVariety'),
        (FOOBAR, 'foobar'),
    ) 
    contribution = models.CharField(max_length=2,
                                    choices = CONT_CHOICES,
                                    default = PREFVAR)
    scheme  = models.ForeignKey(Scheme)
    subject = models.ForeignKey(Cross)

   
#TODO: 
# How long can the species cromosome length comma seperated list be? 
#( what is 4 x max chromosome number??)
#
