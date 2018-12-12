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
from rssfeed import feeds as myfeed

from idapp import views as idapp_views
urlpatterns = [
    path('djk/', include('djk_sample.urls')),
    path('reg/', include('reg.urls')),
    path('pay/', include('payment.urls')),
    path('explorer/', include('explorer.urls'), name='reports'),
    path('catalog/', include('opac.urls')),
    path('intranet/', include('intranet.urls')),
    path('', RedirectView.as_view(url='/catalog/',permanent=True)), 
    url(r'^login/$', auth_views.LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'), 
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/update/', views.edit_user, name='account_update'),
    path('accounts/profiles/', views.profiles_list, name='account_profiles'),
    path('accounts/profile/', views.profile_detail, name='profile_detail'),
    #rest api
    path('api/v1/', include('ilsapi.urls')),
    #barcode id app
    path('idapp/', include('idapp.urls')),
    path('barcode/<str:userid>', idapp_views.barcode,name='barcode_id'),
    #ASE templates
    url(r'^ase-home/', TemplateView.as_view(template_name='ASE/main.html'), name='ase-home'),
    url(r'^absc_home/', TemplateView.as_view(template_name='ABSC/home.html'), name='absc-home'),
    #patron bulk photos_upload
    url(r'^photos-home/', TemplateView.as_view(template_name='photos-home.html'), name='photos-home'),
    #rss feeds
    url(r'^photos/', include(('photos.urls', 'photos'), namespace='photos')),
    path('biblio_feeds/', myfeed.LatestBibliosFeed(), name='biblio-feeds'),
    path('biblio_feed/<int:pk>/', myfeed.LatestBiblioDetailFeed(), name='bibliofeed_detail'),
]

if JWTAUTH:
   urlpatterns +=  [path('api-token-auth/', obtain_jwt_token, name='create-token'),]
else:
   urlpatterns +=  [path('api-auth/', include('rest_framework.urls'))]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
