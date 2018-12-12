from django.conf import settings
from django.conf.urls import include, url
# from django.contrib import admin

from djk_sample.views import renderer_test, UserChangeView
from ils_app.views import (
    BiblioCreate, BiblioCreateDTL, BiblioUpdate, BiblioDetail,
    BiblioList, BiblioListWithComponent, BiblioListDTL,
    ItemDetail, HoldDetail,ReserveDetail, PublisherDetail, AuthorDetail, GenreDetail, LanguageDetail, 
    CorporateAuthorDetail, CollectionDepartmentDetail, DepartmentDetail, DesignationDetail, CategoryDetail 
)
from ils_app.views import main_page
from ils_app.views_ajax import (
    SimpleBiblioGrid, SimpleBiblioGridDTL, EditableBiblioGrid, BiblioGridRawQuery,
    BiblioGridWithVirtualField, BiblioGridWithActionLogging,
    BiblioItemsGrid, ItemsGrid,HoldGrid, BiblioHoldGrid, 
    ReservesGrid, BiblioReservesGrid,
    CollectionDepartmentsFkWidgetGrid, BorrowersFkWidgetGrid, AuthorsFkWidgetGrid, GenreFkWidgetGrid, PublisherFkWidgetGrid,
    CorporateAuthorFkWidgetGrid, CategoriesFkWidgetGrid, DepartmentsFkWidgetGrid, DesignationsFkWidgetGrid,
    LanguageFkWidgetGrid, EditableBorrowersGrid,SimpleBorrowersGrid
)

from event_app.views import ActionList
from event_app.views_ajax import UserFkWidgetGrid, ActionGrid

urlpatterns = [
    # url(r'^admin/', include(admin.site.urls)),
]

# Allauth views.
"""
if settings.ALLAUTH_DJK_URLS:
    # More pretty-looking bootstrap forms but possibly are not compatible with arbitrary allauth version:
    urlpatterns.append(
        url(r'^accounts/', include('django_jinja_knockout._allauth.urls'))
    )
else:
    # Standard allauth DTL templates working with Jinja2 templates via {% load jinja %} template tag library.
    urlpatterns.append(
        url(r'^accounts/', include('allauth.urls'))
    )
"""
urlpatterns += [
    url(r'^renderer-test/$', renderer_test, name='renderer_test',
        kwargs={'view_title': 'Renderer test', 'allow_anonymous': True}),

    url(r'^user-change(?P<action>/?\w*)/$', UserChangeView.as_view(), name='user_change'),

    # Biblio
    url(r'^$', main_page, name='biblio_main_page',
        kwargs={'view_title': 'Main page', 'allow_anonymous': True}),
    url(r'^biblio-create/$', BiblioCreate.as_view(), name='biblio_create',
        kwargs={'view_title': 'Add new biblio'}),
    url(r'^biblio-create-perms-check/$', BiblioCreate.as_view(), name='biblio_create_perms_check',
        kwargs={'view_title': 'Add new biblio with Django permissions check', 'permission_required': 'ils_app.add_biblio'}),
    url(r'^biblio-create-dtl/$', BiblioCreateDTL.as_view(), name='biblio_create_dtl',
        kwargs={'view_title': 'Add new biblio (Django Template Language)'}),
    url(r'^biblio-update-(?P<biblionumber>\d+)/$', BiblioUpdate.as_view(), name='biblio_update',
        kwargs={'view_title': 'Edit biblio "{}"'}),
    url(r'^biblio-detail-(?P<biblionumber>\d+)/$', BiblioDetail.as_view(), name='biblio_detail',
        kwargs={'view_title': '{}'}),
    url(r'^publisher-detail-(?P<publisher_id>\d+)/$', PublisherDetail.as_view(), name='publisher_detail',
        kwargs={'view_title': '{}'}),
    url(r'^author-detail-(?P<authors_id>\d+)/$', AuthorDetail.as_view(), name='author_detail',
        kwargs={'view_title': '{}'}),
    url(r'^language-detail-(?P<language_id>\d+)/$', LanguageDetail.as_view(), name='language_detail',
        kwargs={'view_title': '{}'}),
    url(r'^corporateauthor-detail-(?P<corporateauthor_id>\d+)/$', CorporateAuthorDetail.as_view(), name='corporateauthor_detail',
        kwargs={'view_title': '{}'}),
    url(r'^genre-detail-(?P<genre_id>\d+)/$', GenreDetail.as_view(), name='genre_detail',
        kwargs={'view_title': '{}'}),
    url(r'^department-detail-(?P<departments_id>\d+)/$', DepartmentDetail.as_view(), name='department_detail',
        kwargs={'view_title': '{}'}),
    url(r'^collectionpartment-detail-(?P<collectiondepartments_id>\d+)/$', CollectionDepartmentDetail.as_view(), name='collectiondepartment_detail',
        kwargs={'view_title': '{}'}),
    url(r'^desingation-detail-(?P<designations_id>\d+)/$', DesignationDetail.as_view(), name='designation_detail',
        kwargs={'view_title': '{}'}),
    url(r'^category-detail-(?P<categories_id>\d+)/$', CategoryDetail.as_view(), name='category_detail',
        kwargs={'view_title': '{}'}),    
    url(r'^biblio-list/$', BiblioList.as_view(), name='biblio_list',
        kwargs={'view_title': 'List of collection biblios', 'allow_anonymous': True}),
    url(r'^biblio-list-with-component/$', BiblioListWithComponent.as_view(), name='biblio_list_with_component',
        kwargs={'view_title': 'List of collection biblios with their reserves as App.GridDialog component'}),
    url(r'^biblio-list-dtl/$', BiblioListDTL.as_view(), name='biblio_list_dtl',
        kwargs={'view_title': 'List of collection biblios (Django Template Language)', 'allow_anonymous': True}),

    # Action
    url(r'^action-list/$', ActionList.as_view(), name='action_list',
        kwargs={'view_title': 'Log of actions'}),
    url(r'^action-grid(?P<action>/?\w*)/$', ActionGrid.as_view(), name='action_grid',
        kwargs={'view_title': 'Grid with the list of performed actions'}),

    # Item
    url(r'^item-detail-(?P<itemnumber>\d+)/$', ItemDetail.as_view(), name='item_detail',
        kwargs={'view_title': '{}'}),
    url(r'^hold-detail-(?P<reserveid>\d+)/$', HoldDetail.as_view(), name='hold_detail',
        kwargs={'view_title': '{}'}),
    url(r'^item-grid(?P<action>/?\w*)/$', ItemsGrid.as_view(), name='item_grid',
        kwargs={'view_title': 'Grid with the available item'}),
    url(r'^hold-grid(?P<action>/?\w*)/$', HoldGrid.as_view(), name='hold_grid',
        kwargs={'view_title': 'Grid with the hold priority'}),

    # Reserve
    url(r'^reserve-detail-(?P<reserve_id>\d+)/$', ReserveDetail.as_view(), name='reserve_detail',
        kwargs={'view_title': '{}'}),

    # Foreign key widgets.
    url(r'^user-fk-widget-grid(?P<action>/?\w*)/$', UserFkWidgetGrid.as_view(),
        name='user_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'auth.change_user'}),
        kwargs={'ajax': True}),
    url(r'^categories-fk-widget-grid(?P<action>/?\w*)/$', CategoriesFkWidgetGrid.as_view(),
        name='categories_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'auth.change_categories'}),
        kwargs={'ajax': True}),
    url(r'^collectiondepartments-fk-widget-grid(?P<action>/?\w*)/$', CollectionDepartmentsFkWidgetGrid.as_view(),
        name='collectiondepartments_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_collectiondepartments'}),
        kwargs={'ajax': True}),
    url(r'^departments-fk-widget-grid(?P<action>/?\w*)/$', DepartmentsFkWidgetGrid.as_view(),
        name='departments_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_departments'}),
        kwargs={'ajax': True}),
    url(r'^designations-fk-widget-grid(?P<action>/?\w*)/$', DesignationsFkWidgetGrid.as_view(),
        name='designations_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_designations'}),
        kwargs={'ajax': True}),
    url(r'^publisher-fk-widget-grid(?P<action>/?\w*)/$', PublisherFkWidgetGrid.as_view(),
        name='publisher_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_publisher'}),
        kwargs={'ajax': True}),
    url(r'^language-fk-widget-grid(?P<action>/?\w*)/$', LanguageFkWidgetGrid.as_view(),
        name='language_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_language'}),
        kwargs={'ajax': True}),
    url(r'^authors-fk-widget-grid(?P<action>/?\w*)/$', AuthorsFkWidgetGrid.as_view(),
        name='authors_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_authors'}),
        kwargs={'ajax': True}),
    url(r'^corporateauthor-fk-widget-grid(?P<action>/?\w*)/$', CorporateAuthorFkWidgetGrid.as_view(),
        name='corporateauthor_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_corporateauthor'}),
        kwargs={'ajax': True}),
    url(r'^genre-fk-widget-grid(?P<action>/?\w*)/$', GenreFkWidgetGrid.as_view(),
        name='genre_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_genre'}),
        kwargs={'ajax': True}),
    url(r'^borrowers-fk-widget-grid(?P<action>/?\w*)/$', BorrowersFkWidgetGrid.as_view(),
        name='borrowers_fk_widget_grid',
        # kwargs={'ajax': True, 'permission_required': 'ils_app.change_borrowers'}),
        kwargs={'ajax': True}),

    # AJAX grids.
    # Collection biblio.
    url(r'^biblio-grid-simple(?P<action>/?\w*)/$', SimpleBiblioGrid.as_view(), name='biblio_grid_simple',
        kwargs={'view_title': 'Simple biblio grid'}),
    url(r'^borrowers-grid-simple(?P<action>/?\w*)/$', SimpleBorrowersGrid.as_view(), name='borrowers_grid_simple',
        kwargs={'view_title': 'Simple borrowers grid'}),
    url(r'^biblio-grid-simple-dtl(?P<action>/?\w*)/$', SimpleBiblioGridDTL.as_view(), name='biblio_grid_simple_dtl',
        kwargs={'view_title': 'Simple biblio grid (Django Template Language)'}),
    url(r'^biblio-grid-editable(?P<action>/?\w*)/$', EditableBiblioGrid.as_view(), name='biblio_grid_editable',
        # kwargs={'view_title': 'Editable biblio grid', 'permission_required': 'ils_app.change_biblio'}),
        kwargs={'view_title': 'Editable biblio grid'}),
    url(r'^borrowers-grid-editable(?P<action>/?\w*)/$', EditableBorrowersGrid.as_view(), name='borrowers_grid_editable',
        # kwargs={'view_title': 'Editable borrowers grid', 'permission_required': 'ils_app.change_borrowers'}),
        kwargs={'view_title': 'Editable borrowers grid'}),
    url(r'^biblio-grid-raw-query(?P<action>/?\w*)/$', BiblioGridRawQuery.as_view(), name='biblio_grid_raw_query',
        kwargs={'view_title': 'Biblio grid raw query'}),
    url(r'^biblio-grid-with-virtual-field(?P<action>/?\w*)/$', BiblioGridWithVirtualField.as_view(), name='biblio_grid_with_virtual_field',
        kwargs={'view_title': 'Biblio grid with virtual field'}),
    url(r'^biblio-grid-with-action-logging(?P<action>/?\w*)/$', BiblioGridWithActionLogging.as_view(),
        name='biblio_grid_with_action_logging',
        kwargs={'view_title': 'Biblio grid with virtual field'}),
    url(r'^biblio-item-grid(?P<action>/?\w*)/$', BiblioItemsGrid.as_view(),
        name='biblio_item_grid',
        kwargs={'view_title': 'Biblio item grid'}),
    
    url(r'^biblio-hold-grid(?P<action>/?\w*)/$', BiblioHoldGrid.as_view(),
        name='biblio_hold_grid',
        kwargs={'view_title': 'Biblio hold grid'}),

    # Collection biblio reserve.
    url(r'^reserve-grid(?P<action>/?\w*)/$', ReservesGrid.as_view(), name='reserve_grid',
        kwargs={'view_title': 'Biblio reserves grid'}),
    url(r'^biblio-reserve-grid-(?P<biblio_id>\w*)(?P<action>/?\w*)/$', BiblioReservesGrid.as_view(), name='biblio_reserve_grid',
        kwargs={'view_title': '"{}" reserves'}),
]

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('djk_sample',),
}

try:
    from django.views.i18n import JavaScriptCatalog
    urlpatterns.append(
        url(r'^jsi18n/$', JavaScriptCatalog.as_view(**js_info_dict), name='javascript-catalog'),
    )
except ImportError:
    from django.views.i18n import javascript_catalog
    urlpatterns.append(
        url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='javascript-catalog')
    )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()

