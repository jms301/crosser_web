from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication
from models import Plan

class PlanResource(ModelResource):
    class Meta:
        queryset = Plan.objects.all()
        authentication = SessionAuthentication()
