from django.contrib import admin
from django.urls import path,re_path, include
from django.conf.urls import url

from intranet.views import borrowers, BorrowersListView, borrowers_listing, BorrowersTablesView, FilteredBorrowersListView, borrowers_table_export_view
from intranet.views import biblios, BibliosListView, biblios_listing, BibliosTablesView, FilteredBibliosListView, biblios_table_export_view
from intranet.views import user_search_query
from intranet import views as intranet_views
from intranet.views import SystemPreferencesListView
urlpatterns = [
    #table2
    url(r'^tables/borrowers/', borrowers, name='borrower-list'),
    #url(r'^tables/borrowers/', BorrowersListView.as_view()),
    url(r'^tables/borrowers_singletable_list/', borrowers_listing,name='borrower-list-singletable'),
    url(r'^tables/borrowers_table_export/', borrowers_table_export_view, name='export-borrowers'),
    url(r'^tables/borrowers_filtered_list/', FilteredBorrowersListView.as_view(), name='filtered-borrowers'),
    url(r'^tables/borrowers_multitable_list/', BorrowersTablesView.as_view(), name='borrower-list-multitable'),
    url(r'^ql/user_search_query/', user_search_query, name='user-search-query'),
    #---tables--biblio
    url(r'^tables/biblios/', biblios, name='biblios-list'),
    #url(r'^tables/biblos/', BibliosListView.as_view()),
    url(r'^tables/biblios-list/', biblios_listing, name='biblios-list-singletable'),
    url(r'^tables/biblios-table-export/',biblios_table_export_view, name='export-biblios'),
    url(r'^tables/biblios-filtered-list/', FilteredBibliosListView.as_view(), name='filtered-biblios'),
    url(r'^tables/biblios-multitable-list/', BibliosTablesView.as_view(), name='biblios-list-multitable'),
    #systemprefs
    path('system_preferences/', SystemPreferencesListView.as_view(), name="list-system-preferences"),
    path('system_preference/<int:pk>/', intranet_views.systempreference_detail_view, name="system-preference-detail"),
    path('change_system_preference/<int:pk>/', intranet_views.edit_system_preference, name="edit-system-preference"),
    
]

