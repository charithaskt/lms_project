from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'home/', views.home, name='reg-home'),
    url(r'^signup/$', views.signup, name='reg-signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^login/$', views.login, name='login'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.reset, name='reset'),
    url(r'^logout/$', views.logout, name='logout'),
]
