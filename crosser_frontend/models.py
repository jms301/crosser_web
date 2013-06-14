from django.db import models

# Create your models here.

class Species(models.Model):
    name = models.CharField(max_length = 100)
    chromosome_lengths = models.CommaSeparatedIntegerField(max_length = 100)


class Plan(models.Model):
    conf_chunk_size = models.IntegerField( )
    conf_recombination_prob = models.IntegerField( )
    conf_tolerance = models.IntegerField( )
    name = models.CharField(max_length = 100)
    species = models.ForeignKey(Species, related_name='+')
    def __unicode__(self): 
        return self.name

class Plant(models.Model):
    name = models.CharField(max_length = 100)
    output = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan)

class Loci(models.Model):
    TRAIT = 'Tr'
    MARKER = 'Ma'
    TYPE_CHOICES = (
        (TRAIT, 'Trait'),
        (MARKER, 'Marker'),
    )
    name = models.CharField(max_length = 100)
    loci_type = models.CharField(max_length=2, 
                                choices = TYPE_CHOICES, 
                                default=TRAIT)
    linkageGroup = models.IntegerField()
    position = models.IntegerField()
    plant =  models.ForeignKey(Plant)

class Cross(models.Model):
    HETEROZYGOUS = 'He'
    HOMOZYGOUS = 'Ho' 
    ZYGOSITY_CHOICES = (
        (HETEROZYGOUS, 'Heterozygous'),
        (HOMOZYGOUS, 'Homozygous'),
    )
    name = models.CharField(max_length = 100)

    plan =  models.ForeignKey(Plan)
    left_parent = models.ForeignKey(Plant, related_name='+')
    right_parent = models.ForeignKey(Plant, related_name='+')
    protocol_zygosity = models.CharField(max_length=2, 
                                choices = ZYGOSITY_CHOICES, 
                                default=HOMOZYGOUS)

class CrossLoci(models.Model):
    cross = models.ForeignKey(Cross)
    loci = models.ForeignKey(Loci)
    class Meta:
        unique_together = ('cross', 'loci')
    
#TODO: 
# How long can the species cromosome length comma seperated list be? 
#( what is 4 x max chromosome number??)
#
