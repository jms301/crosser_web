from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView, TemplateView
from crosser_frontend.models import Plan

urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(
            template_name = 'crosser_frontend/index.html'),
        name='index'),
    
    url(r'^cross/(?P<pk>\d)/$',
        DetailView.as_view(
            model = Plan,
            template_name = 'crosser_frontend/plan_detail.html'),
        name='cross_detail'),
    url(r'^crosses/$',
        ListView.as_view(
            queryset = Plan.objects.all(),
            template_name = 'crosser_frontend/plans_list.html'),
        name='crosses_list'),

    url(r'^signup/$', 'crosser_frontend.views.signup',
        name='signup'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='site-logout'),

)
