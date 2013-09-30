from django.contrib import admin
from crosser_frontend.models import Scheme, Plant, Species, Locus, Cross, Output, System, Calculation
from guardian.admin import GuardedModelAdmin


class SchemeAdmin(GuardedModelAdmin):
    pass

admin.site.register(System)
admin.site.register(Output)
admin.site.register(Scheme)
admin.site.register(Plant)
admin.site.register(Species)
admin.site.register(Locus)
admin.site.register(Cross)
admin.site.register(Calculation)
