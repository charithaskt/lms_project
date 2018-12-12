from collections import OrderedDict
from copy import copy
import json

from django.utils import timezone
from django.utils.translation import gettext as _
from django.template.defaultfilters import pluralize
from django.db.models import Count

from django_jinja_knockout.query import FilteredRawQuerySet
from django_jinja_knockout.views import KoGridView, KoGridInline, FormatTitleMixin, ContextDataMixin
from django_jinja_knockout.viewmodels import vm_list
from django_jinja_knockout.utils.sdv import get_choice_str, nested_update

from .models import Biblio, Supplier, Patron, Reserve, Item
from .models import Author, Publisher, Genre
from .forms import (
    BiblioForm, BiblioFormWithInlineFormsets,
    SupplierForm, PatronForm, BiblioItemForm, ReserveForm,
    PublisherForm, AuthorForm, GenreForm, 
    PublisherDisplayForm, AuthorDisplayForm, GenreDisplayForm
)

class SimpleBiblioGrid(KoGridView):

    model = Biblio
    grid_fields = '__all__'
    # Remove next line to disable columns sorting:
    allowed_sort_orders = '__all__'
    
    @classmethod
    def get_grid_options(cls):
        return {
            'selectMultipleRows': True,
            'highlightMode': 'linearRows',
            'fkGridOptions': {
                'author': {
                    'pageRoute': 'author_fk_widget_grid',
                    'dialogOptions': {'size': 'size-wide'},
                },
                'genre': {
                     'pageRoute': 'genre_fk_widget_grid',
                    'dialogOptions': {'size': 'size-wide'},
                },
                'publisher': {
                     'pageRoute': 'publisher_fk_widget_grid',
                    'dialogOptions': {'size': 'size-wide'},
                }
            },
            
        }
     
class SimpleBiblioGridDTL(ContextDataMixin, SimpleBiblioGrid):
    template_name = 'biblio_grid.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['biblio_grid_options'] = {
            'pageRoute': self.request.url_name
        }
        return context_data


class EditableBiblioGrid(KoGridInline, SimpleBiblioGrid):

    search_fields = [
        ('title', 'icontains')
    ]
    client_routes = {
        'publisher_fk_widget_grid',
        'author_fk_widget_grid',
        'genre_fk_widget_grid',
        'supplier_fk_widget_grid',
        'patron_fk_widget_grid'
    }
    enable_deletion = True
    form_with_inline_formsets = BiblioFormWithInlineFormsets


class BiblioGridRawQuery(SimpleBiblioGrid):

    template_name = 'cbv_grid_breadcrumbs.htm'
    grid_fields = [
        'reserve__patron__first_name',
        'reserve__patron__last_name',
        'category',
        'reserve__priority',
        'title',
        'publisher__name',
        'author',
        'genre__name',
        'totalissues',
        'itemtype',
    ]

    allowed_filter_fields = OrderedDict([
        ('itemtype', None),
        ('category', None),
        
    ])

    def get_model_meta(self, key):
        if key == 'verbose_name_plural':
            # Override grid title.
            return 'Collection biblios and their reserves'
        else:
            return super().get_model_meta(key)

    def get_field_verbose_name(self, field_name):
        if field_name == 'category':
            return 'Reserve Category'
        elif field_name == 'publisher':
            return 'Biblio Publisher'
        elif field_name == 'author':
            return 'Biblio Author(s)'
        elif field_name == 'genre':
            return 'Biblio Topical Term(s)'
        elif field_name == 'totalissues':
            return 'Biblio Total Issues'
        else:
            return super().get_field_verbose_name(field_name)

    def get_field_validator(self, fieldname):
        if fieldname == 'category':
            return self.__class__.field_validator(self, fieldname, model_class=Patron)
        else:
            return super().get_field_validator(fieldname)

    def get_row_str_fields(self, obj, row=None):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of manually JOINed field.
        str_fields['category'] = get_choice_str(Patron.CATEGORIES, row['category'])
        return str_fields

    def get_base_queryset(self):
        # Mostly supposed to work with LEFT JOIN. Might produce wrong results with arbitrary queries.
        raw_qs = self.model.objects.raw(
            'SELECT ils_app_biblio.*, ils_app_patron.category,ils_app_reserve.priority, '
            'ils_app_patron.first_name, ils_app_patron.last_name FROM ils_app_biblio '
            'LEFT JOIN ils_app_reserve ON ils_app_biblio.id = ils_app_reserve.biblio_id '
            'LEFT JOIN ils_app_patron ON ils_app_patron.id = ils_app_reserve.patron_id ' ,
            #'LEFT JOIN ils_app_author ON ils_app_author.id = ils_app_biblio.author_id ',
            #'LEFT JOIN ils_app_publisher ON ils_app_publisher.id = ils_app_biblio.publisher_id ',
            #'LEFT JOIN ils_app_genre ON ils_app_genre.id = ils_app_biblio.genre_id ',
        )
        fqs = FilteredRawQuerySet.clone_raw_queryset(
            raw_qs=raw_qs, relation_map={
                'category': 'reserve__patron',
                'priority' : 'reserve',
                'first_name': 'reserve__patron',
                'last_name': 'reserve__patron'
            }
        )
        return fqs


class BiblioGridWithVirtualField(SimpleBiblioGrid):

    grid_fields = [
        'title',
        'author',
        'publisher',
        'genre',
        'itemtype',
        'total_items',
        'total_holds',
        'totalissues',
    ]

    def get_base_queryset(self):
        return super().get_base_queryset().annotate(total_items=Count('item', distinct=True), total_holds=Count('reserve', distinct=True))

    def get_field_verbose_name(self, field_name):
        if field_name == 'total_items':
            # Add annotated field.
            return 'Total items'
        elif field_name == 'total_holds':
            return 'Total holds'
        elif field_name == 'totalissues':
            return 'Total issues'

        else:
            return super().get_field_verbose_name(field_name)

    def get_related_fields(self, query_fields=None):
        query_fields = super().get_related_fields(query_fields)
        # Remove virtual field from queryset values().
        #query_fields.remove('exists_days')
        return query_fields

    def get_model_fields(self):
        model_fields = copy(super().get_model_fields())
        # Remove annotated field which is unavailable when creating / updating single object which does not use
        # self.get_base_queryset()
        # Required only because current grid is editable.
        model_fields.remove('total_items')
        model_fields.remove('total_holds')
        return model_fields

    def postprocess_row(self, row, obj):
        # Add virtual field value.
        #row['exists_days'] = (timezone.now().date() - obj.foundation_date).days
        if 'total_items' not in row:
            # Add annotated field value which is unavailable when creating / updating single object which does not use
            # self.get_base_queryset()
            # Required only because current grid is editable.
            row['total_items'] = obj.item_set.count()
        if 'total_holds' not in row:
            row['total_holds'] = obj.reserve_set.count()
        row['itemtype']=obj.get_itemtype_display()
        row = super().postprocess_row(row, obj)
        return row

    # Optional formatting of virtual field (not required).
    def get_row_str_fields(self, obj, row=None):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of virtual field.
        #is_plural = pluralize(row['exists_days'], arg='days')
        #str_fields['exists_days'] = '{} {}'.format(row['exists_days'], 'day' if is_plural == '' else is_plural)
        #return str_fields


class BiblioGridWithActionLogging(BiblioGridWithVirtualField, EditableBiblioGrid):

    template_name = 'biblio_grid_with_action_logging.htm'
    client_routes = {
        'user_fk_widget_grid',
        'supplier_fk_widget_grid',
        'patron_fk_widget_grid',
        'action_grid',
        'author_fk_widget_grid',
        'publisher_fk_widget_grid',
        'genre_fk_widget_grid',
    }
    grid_options = {
        # Note: 'classPath' is not required for standard App.ko.Grid.
        'classPath': 'App.ko.BiblioGrid',
    }


class BiblioItemGrid(EditableBiblioGrid):

    client_routes = {
        # Injected in djk_sample.context_processors.TemplateContextProcessor.CLIENT_ROUTES,
        # just for the test of global route injection.
        # 'item_grid',
        'biblio_grid_simple',
        'supplier_fk_widget_grid',
    }
    template_name = 'biblio_item.htm'
    form = BiblioForm
    form_with_inline_formsets = None

    def get_actions(self):
        actions = super().get_actions()
        actions['built_in']['save_item'] = {}
        actions['glyphicon']['add_item'] = {
            'localName': _('Add biblio item'),
            'css': 'glyphicon-wrench',
        }
        return actions

    # Creates AJAX BiblioItemForm bound to particular Biblio instance.
    def action_add_item(self):
        biblio = self.get_object_for_action()
        if biblio is None:
            return vm_list({
                'view': 'alert_error',
                'title': 'Error',
                'message': 'Unknown instance of Biblio'
            })
        item_form = BiblioItemForm(initial={'biblio': biblio.pk})
        # Generate item_form viewmodel
        vms = self.vm_form(
            item_form, form_action='save_item'
        )
        return vms

    # Validates and saves the Item model instance via bound BiblioItemForm.
    def action_save_item(self):
        form = BiblioItemForm(self.request.POST)
        if not form.is_valid():
            form_vms = vm_list()
            self.add_form_viewmodels(form, form_vms)
            return form_vms
        item = form.save()
        biblio = item.biblio
        biblio.last_update = timezone.now()
        biblio.save()
        # Instantiate related ItemGrid to use it's .postprocess_qs() method
        # to update it's row via grid viewmodel 'prepend_rows' key value.
        item_grid = ItemGrid()
        item_grid.request = self.request
        item_grid.init_class()
        return vm_list({
            'update_rows': self.postprocess_qs([biblio]),
            # return grid rows for client-side ItemGrid component .updatePage(),
            'item_grid_view': {
                'prepend_rows': item_grid.postprocess_qs([item])
            }
        })


class ItemGrid(KoGridView):
    model = Item
    form = BiblioItemForm
    enable_deletion = True
    grid_fields = [
        'biblio',
        'supplier__company_name',
        'supplier__direct_shipping',
        'barcode',
        'status',
    ]
    search_fields = [
        ('barcode', 'iexact')
    ]
    allowed_sort_orders = [
        'supplier__company_name',
        'barcode',
        'status'
    ]
    allowed_filter_fields = OrderedDict([
        ('biblio', {
            'pageRoute': 'biblio_grid_simple',
            # Optional setting for BootstrapDialog:
            'dialogOptions': {'size': 'size-wide'},
        }),
        ('supplier', {
            'pageRoute': 'supplier_fk_widget_grid'
        }),
        ('supplier__direct_shipping', None),
        ('status', None)
    ])
    grid_options = {
        'searchPlaceholder': 'Search barcode',
    }

    def get_actions(self):
        # Disable adding new Item because BiblioItemForm is incomplete (has no Biblio) for action 'create_form'.
        # BiblioItemGrid.action_add_item is used instead.
        actions = super().get_actions()
        actions['button']['create_form']['enabled'] = False
        return actions


class ReserveGrid(KoGridView):

    client_routes = {
        'reserve_grid',
        'patron_fk_widget_grid',
        'biblio_grid_simple'
    }
    template_name = 'reserve_grid.htm'
    model = Reserve
    grid_fields = [
        'patron', #---modified
        'biblio',
        # Compound columns:
        [
            # Will join 'temtype' field from related 'Biblio' table automatically via Django ORM.
            'biblio__itemtype',
            'biblio__author',
            'biblio__publisher',
            'reserved_on',
            'patron__category',
            'patron__cardnumber',
        ],
        #'patron__note',
        #'patron__is_active'
    ]
    search_fields = [
        ('biblio__title', 'icontains'),
        ('patron__first_name', 'icontains'),
        ('patron__last_name', 'icontains'),
        ('patron__cardnumber', 'icontains'),
    ]
    allowed_sort_orders = [
        'biblio', # -- modified
        # Will join 'category' field from related 'Biblio' table automatically via Django ORM.
        'biblio__itemtype',
        'biblio__author',
        'biblio__publisher',
        'reserved_on',
        'patron__cardnumber',
        #'patron__is_active'
    ]
    
    allowed_filter_fields = OrderedDict([
        ('biblio', None),
        ('reserved_on', None),
        ('biblio__itemtype', None),
        #('biblio__author',None),
        #('biblio__publisher', None),
        ('patron__category', None),
        #('patron__cardnumber', None), #--modified
        #('patron__is_active', None),
    ])

    def get_field_verbose_name(self, field_name):
        if field_name == 'itemtype':
            return 'Biblio itemtype'
        else:
            return super().get_field_verbose_name(field_name)

    @classmethod
    def get_grid_options(cls):
        return {
            # Note: 'classPath' is not required for standard App.ko.Grid.
            #'classPath': 'App.ko.ReserveGrid',
            'searchPlaceholder': 'Search for biblio or reserve patron',
            'fkGridOptions': {
                'patron': {
                    'pageRoute': 'patron_fk_widget_grid'
                },
                'biblio': {
                    'pageRoute': 'biblio_grid_simple',
                    # Optional setting for BootstrapDialog:
                    'dialogOptions': {'size': 'size-wide'},
                },
                'biblio__author': {
                    'pageRoute': 'author_fk_widget_grid'                    
                },
                'biblio__publisher': {
                    'pageRoute': 'publisher_fk_widget_grid'
                },
                
            }
        }

    # Overriding get_base_queryset() is not required, but is used to reduce number of queries.
    def get_base_queryset(self):
        return self.__class__.model.objects.select_related('biblio').all()


class BiblioReserveGrid(FormatTitleMixin, ReserveGrid):
    
    format_view_title = True
    grid_fields = [
        'patron', #modified
        [
            'patron__first_name',   
            'patron__last_name',
            'patron__cardnumber',
            'patron__category',
        ],
        [
            'reserved_on',
            'priority', 
            'is_found',
        ],
        #'patron__note',
    ]
    search_fields = [
        ('patron__first_name', 'icontains'),
        ('patron__last_name', 'icontains'),
        ('patron__cardnumber','iexact'),        
    ]
    allowed_filter_fields = OrderedDict([
        #('patron', None),
        ('reserved_on', None),
        ('patron__category', None),
        ('priority',None),
        ('is_found', None),
    ])

    def get_base_queryset(self):
        return super().get_base_queryset().filter(biblio_id=self.kwargs['biblio_id'])

    def get(self, request, *args, **kwargs):
        biblio = Biblio.objects.filter(pk=self.kwargs['biblio_id']).first()
        if biblio is not None:
            self.format_title(biblio)
        return super().get(request, *args, **kwargs)


class SupplierFkWidgetGrid(KoGridView):

    model = Supplier
    form = SupplierForm
    enable_deletion = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    allowed_filter_fields = OrderedDict([
        ('direct_shipping', None)
    ])
    search_fields = [
        ('company_name', 'icontains'),
    ]

class PublisherFkWidgetGrid(KoGridView):

    model = Publisher
    form = PublisherForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    search_fields = [
        ('name', 'icontains'),
    ]

class AuthorFkWidgetGrid(KoGridView):

    model = Author
    form = AuthorForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = ['first_name', 'last_name']
    allowed_sort_orders = '__all__'
    search_fields = [
        ('first_name', 'icontains'),
        ('last_name', 'icontains'),              
    ]

class GenreFkWidgetGrid(KoGridView):

    model = Genre
    form = GenreForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    search_fields = [
        ('name', 'icontains'),
    ]

class PatronFkWidgetGrid(KoGridView):

    model = Patron
    form = PatronForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = ['first_name', 'last_name','cardnumber']
    allowed_sort_orders = '__all__'
    search_fields = [
        ('first_name', 'icontains'),
        ('last_name', 'icontains'),
        ('cardnumber','iexact'),        
    ]


