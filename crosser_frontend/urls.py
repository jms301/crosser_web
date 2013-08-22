from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from crosser_frontend.models import Scheme

urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(
            template_name = 'crosser_frontend/index.html'),
        name='index'),
        
    url(r'^cross/(?P<pk>\d)/$',
        TemplateView.as_view(
            template_name = 'crosser_frontend/scheme_detail.html'),
        name='scheme_detail'),
    url(r'^crosses/$',
        TemplateView.as_view(
            template_name = 'crosser_frontend/schemes_list.html'),
        name='schemes_list'),

    url(r'^signup/$', 'crosser_frontend.views.signup',
        name='signup'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='site-logout'),

)
