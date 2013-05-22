from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView, TemplateView


urlpatterns = patterns('',
    url(r'^$',
        TemplateView.as_view(
            template_name = 'crosser_frontend/index.html'),
        name='index'),

    url(r'^signup/$', 'crosser_frontend.views.signup',
        name='signup'),

    url(r'^logout/$', 'django.contrib.auth.views.logout', 
        {'next_page': '/'}, name='site-logout'),
)
