from django.contrib import admin
from django.urls import path,re_path, include
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token
from .settings import JWTAUTH
from django.conf.urls.static import static
from django.views.generic import TemplateView
from intranet.views import borrowers, BorrowersListView, borrowers_listing, BorrowersTablesView, FilteredBorrowersListView, borrowers_table_export_view

from intranet.views import biblios, BibliosListView, biblios_listing, BibliosTablesView, FilteredBibliosListView, biblios_table_export_view

urlpatterns = [
    path('explorer/', include('explorer.urls')),
    path('catalog/', include('opac.urls')),
    path('', RedirectView.as_view(url='/catalog/',permanent=True)), 
    #url(r'^$', views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    #url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='ils-login'),
    #url(r'^logout/$', auth_views.logout, {'next_page': 'ils-login'}, name='ils-logout'),

    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'), 
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')),
    #url(r'^accounts/update/(?P<pk>[\-\w]+)/$', views.edit_user, name='account_update'),
    #re_path(r'^accounts/update/(?P<pk>[\-\w]+)/$', views.edit_user, name='account_update'),
    path('accounts/update/', views.edit_user, name='account_update'),
    path('accounts/profiles/', views.profiles_list, name='account_profiles'),
    path('accounts/profile/', views.profile_detail, name='profile_detail'),
    #table2
    url(r'^tables/borrowers/', borrowers),
    #url(r'^tables/borrowers/', BorrowersListView.as_view()),
    url(r'^tables/borrowers-list/', borrowers_listing),
    url(r'^tables/borrowers-table-export/', borrowers_table_export_view),
    url(r'^tables/borrowers-filtered-list/', FilteredBorrowersListView.as_view()),
    url(r'^tables/borrowers-multitable-list/', BorrowersTablesView.as_view()),

    #---tables--biblio
    url(r'^tables/biblios/', biblios),
    #url(r'^tables/biblos/', BibliosListView.as_view()),
    url(r'^tables/biblios-list/', biblios_listing),
    url(r'^tables/biblios-table-export/',biblios_table_export_view),
    url(r'^tables/biblios-filtered-list/', FilteredBibliosListView.as_view()),
    url(r'^tables/biblios-multitable-list/', BibliosTablesView.as_view()),
    #rest api
    #path('api-token-auth/', obtain_jwt_token, name='create-token'),
    #re_path('api/(?P<version>(v1|v2))/', include('ilsapi.urls')),
    path('api/v1/', include('ilsapi.urls')),

    #patron bulk photos_upload
    url(r'^photos-home/', TemplateView.as_view(template_name='photos-home.html'), name='photos-home'),
    url(r'^photos/', include(('photos.urls', 'photos'), namespace='photos')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if JWTAUTH:
   urlpatterns +=  [path('api-token-auth/', obtain_jwt_token, name='create-token'),]
else:
   #urlpatterns +=  [path('api-auth/', include('rest_auth.urls'))]
   urlpatterns +=  [path('api-auth/', include('rest_framework.urls'))]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
