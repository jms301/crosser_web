from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

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
    pref_var = models.ForeignKey('Plant', related_name='+', null=True)


    def freeze(self): 
        # create a frozen copy 
        # attempt to create calc object (auto versioned) 
        # save the new calculation.
        copy = self.copy()
        calculation = Calculation(owner = self.owner, scheme = self,
                        frozen_scheme = copy) 
        calculation.save()

        return calculation

    def copy(self, freeze=True, owner=None):
        if owner is None:
            owner = self.owner
        new_scheme = Scheme(name = self.name, frozen=freeze, 
                    pref_var = self.pref_var, species=self.species, owner=owner)
        new_scheme.save()

        new_system = System(owner=owner, 
            scheme=new_scheme,
            frozen = freeze,
            convergence_fewest_plants = self.system.convergence_fewest_plants,
            convergence_tolerance = self.system.convergence_tolerance,
            convergence_chunk_size = self.system.convergence_chunk_size ) 
        new_system.save()


        #dicts mapping the old model to the new model. ie
        #cross_map[old_cross] = new_cross 
        locus_map = {}
        cross_map = {}
        plant_map = {}

        for output in self.outputs.all().order_by('id'): 
            new_output = Output(owner=owner, frozen=freeze, 
                scheme=new_scheme, output_type = output.output_type, 
                data = output.data)
            new_output.save()

        for plant in self.plants.all().order_by('id'):
            plant_map[plant] = Plant(owner=owner, name=plant.name, 
                scheme = new_scheme, frozen = freeze)
            plant_map[plant].save()

            for locus in plant.loci.all().order_by('id'):
                locus_map[locus] = Locus(owner=owner, name = locus.name,
                    locus_type = locus.locus_type, 
                    linkage_group = locus.linkage_group,
                    position = locus.position,
                    plant = plant_map[plant],
                    frozen = freeze)
                locus_map[locus].save()
      
        for cross in self.crosses.all().order_by('id'): 
            new_cross = Cross(owner=owner, name = cross.name, 
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

        if self.pref_var:
            new_scheme.pref_var = plant_map[self.pref_var]
            new_scheme.save()

        return new_scheme

    def __unicode__(self): 
        if self.frozen:
            return self.name + " (f)"
        else:
            return self.name

class Calculation(models.Model):


    owner = models.ForeignKey(User)
    version = models.IntegerField(default = 0)
    scheme = models.ForeignKey(Scheme, related_name='calculations', on_delete=models.PROTECT)
    frozen_scheme = models.ForeignKey(Scheme, related_name='calculation')
    task_id = models.CharField(max_length=255) 
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
  
    @property 
    def show_status(self):
        status = process_scheme.AsyncResult(self.task_id).state  
        if status == "STARTED":
            status = "RUNNING"
        elif status == "FAILURE":
            status = "ERROR"
        elif status == "REVOKED":
            status = "CANCELLED"
        return status

    @property 
    def backend_url(self):
        domain = Site.objects.get_current().domain
        return "http://" + domain + "/api/backend/scheme/" + str(self.frozen_scheme.id) + "?format=json"

    @property 
    def output_dir(self):
        return "calcs/" + str(self.id) + "/" 

    def __unicode__(self):
        return self.scheme.name + " calculation v:" + str(self.version)

    def save(self, force_insert=False, force_update=False):
        # Only modify number if creating for the first time (is default 0)
        if self.version == 0:
            # Grab the highest current index (if it exists)
            try:
                recent = Calculation.objects.filter(scheme=self.scheme).order_by('-version')[0]
                self.version = recent.version + 1
            except IndexError:
                self.version = 1
        # Call the "real" save() method
        super(Calculation, self).save(force_insert, force_update)


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

    output_type = models.CharField(max_length=100, null=True)

    data = models.CharField(max_length=2000, null=True)

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
from crosser_frontend.tasks import process_scheme
