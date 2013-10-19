from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from crosser_frontend.models import Scheme, Calculation

urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(
            template_name = 'crosser_frontend/index.html'),
        name='index'),
    
    url(r'^taskadmin/$', 'crosser_frontend.views.task_admin',
        name='task_admin'),

    url(r'^taskkill/(\d+)/$', 'crosser_frontend.views.kill_task',
        name='kill_task'),
       
    url(r'^scheme/(\d+)/process$', 'crosser_frontend.views.process', 
        name='process'),


    url(r'^scheme/(?P<pk>\d+)/$',
        DetailView.as_view(
            model = Scheme,
            template_name = 'crosser_frontend/scheme_detail.html'),
        name='scheme_detail'),

    url(r'^schemes/$',
        TemplateView.as_view(
            template_name = 'crosser_frontend/schemes_list.html'),
        name='schemes_list'),

    
    url(r'^calculations/$',
        ListView.as_view(
            model = Calculation,
            queryset = Calculation.objects.all().order_by('owner', 'scheme', '-version'),
            template_name = 'crosser_frontend/calcs_list.html'),
        name='calcs_list'),

    url(r'^calculation/(\d+)/dupe', 'crosser_frontend.views.dupe_scheme', 
        name='dupe_scheme'),

    url(r'^calculation/(?P<pk>\d+)/$',
        DetailView.as_view(
            model = Calculation,
            template_name = 'crosser_frontend/calc_detail.html'),
        name='calc'),

    url(r'^signup/$', 'crosser_frontend.views.signup',
        name='signup'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='site-logout'),

)
