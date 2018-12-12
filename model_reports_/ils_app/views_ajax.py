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

from .models import Biblio, CollectionDepartments, Borrowers, Reserves, Items, Language 
from .models import Authors, CorporateAuthor, Publisher, Genre, Departments, Designations, Categories
from .models import itemtype_choices, item_status_choices, location_choices, notforloan_choices
from .forms import (
    BiblioForm, BiblioFormWithInlineFormsets,
    CollectionDepartmentsForm, BorrowersForm, BiblioItemsForm, ReservesForm,BiblioHoldForm, HoldForm, 
    PublisherForm, AuthorsForm, GenreForm, CorporateAuthorForm,
    DepartmentsForm, DesignationsForm, CategoriesForm,LanguageForm, LanguageDisplayForm,  
    PublisherDisplayForm, AuthorsDisplayForm, GenreDisplayForm, CorporateAuthorDisplayForm,
    DepartmentsDisplayForm, CollectionDepartmentsDisplayForm,DesignationsDisplayForm, CategoriesDisplayForm,
    BiblioReservesForm
)

class SimpleBiblioGrid(KoGridView):

    model = Biblio
    grid_fields = ['itemtype','title','first_author','publisher','copyrightdate','subject_heading']
    # Remove next line to disable columns sorting:
    allowed_sort_orders = '__all__'
    
    @classmethod
    def get_grid_options(cls):
        return {
            'selectMultipleRows': True,
            'highlightMode': 'linearRows',
            'fkGridOptions': {
                'language': {
                    'pageRoute': 'language_fk_widget_grid',
                    'dialogOptions': {'size': 'size-wide'},
                },
                'first_author': {
                    'pageRoute': 'authors_fk_widget_grid',
                    'dialogOptions': {'size': 'size-wide'},
                },
                'corporateauthor': {
                    'pageRoute': 'corporateauthor_fk_widget_grid',
                    'dialogOptions': {'size': 'size-wide'},
                },
                'subject_heading': {
                     'pageRoute': 'genre_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                'publisher': {
                     'pageRoute': 'publisher_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                'category': {
                     'pageRoute': 'categories_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                'department': {
                     'pageRoute': 'departments_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                'designation': {
                     'pageRoute': 'designations_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                

            },
            
        }
class SimpleBorrowersGrid(KoGridView):

    model = Borrowers
    grid_fields = ['firstname','surname','cardnumber','email']
    # Remove next line to disable columns sorting:
    allowed_sort_orders = '__all__'
    
    @classmethod
    def get_grid_options(cls):
        return {
            'selectMultipleRows': True,
            'highlightMode': 'linearRows',
            'fkGridOptions': {
                
                'category': {
                     'pageRoute': 'categories_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                'department': {
                     'pageRoute': 'departments_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                'designation': {
                     'pageRoute': 'designations_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
                
                'user': {
                     'pageRoute': 'user_fk_widget_grid',
                     'dialogOptions': {'size': 'size-wide'},
                },
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
        'language_fk_widget_grid',
        'authors_fk_widget_grid',
        'corporateauthor_fk_widget_grid',
        'genre_fk_widget_grid',
        'collectiondepartments_fk_widget_grid',
        'departments_fk_widget_grid',
        'designations_fk_widget_grid',
        'categories_fk_widget_grid',
        'borrowers_fk_widget_grid'
    }
    enable_deletion = True
    form_with_inline_formsets = BiblioFormWithInlineFormsets

class EditableBorrowersGrid(SimpleBorrowersGrid):

    search_fields = [
        ('firstname', 'icontains'),
        ('surname', 'icontains'),
        ('cardnumber', 'iexact'),
    ]
    client_routes = {
        'departments_fk_widget_grid',
        'designations_fk_widget_grid',
        'categories_fk_widget_grid',
        'user_fk_widget_grid',
    }
    enable_deletion = True
    form = BorrowersForm    

class BiblioGridWithVirtualField(SimpleBiblioGrid):

    grid_fields = [
        'title',
        'first_author__firstname',
        'first_author__lastname',
        'corporateauthor__name',
        'publisher__name',
        'language__name',
        'subject_heading__name',
        'itemtype',
        'total_items',
        'total_holds',
        'totalissues',
    ]

    def get_base_queryset(self):
        return super().get_base_queryset().annotate(total_items=Count('items', distinct=True), total_holds=Count('reserves', distinct=True))

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
            row['total_items'] = obj.items_set.count()
        if 'total_holds' not in row:
            row['total_holds'] = obj.reserves_set.count()
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
        'collectiondepartments_fk_widget_grid',
        #'borrowers_fk_widget_grid',
        'action_grid',
        'authors_fk_widget_grid',
        'language_fk_widget_grid',
        'corporateauthor_fk_widget_grid',
        'publisher_fk_widget_grid',
        'genre_fk_widget_grid',
    }
    grid_options = {
        # Note: 'classPath' is not required for standard App.ko.Grid.
        'classPath': 'App.ko.BiblioGrid',
    }

#------------Biblio_Hold_grid-------------
class BiblioHoldGrid(EditableBiblioGrid):
    client_routes = {
        #'hold_grid',
        'biblio_grid_simple',        
        'categories_fk_widget_grid',
        'departments_fk_widget_grid',  
        'designations_fk_widget_grid',
        'borrowers_fk_widget_grid',        
    }
    template_name = 'biblio_hold.htm'
    form = BiblioForm
    form_with_inline_formsets = None
    search_fields = [
        ('copyrightdate', 'iexact'),
        ('authors__firstname', 'icontains'),
        ('authors__lastname', 'icontains'),
        ('publisher__name', 'icontains'),
        ('genre__name', 'icontains'),
        ('pages', 'iexact'),
        ('callnumber', 'istartswith'),
    ]
    def get_actions(self):
        actions = super().get_actions()
        actions['built_in']['save_item'] = {}
        actions['glyphicon']['add_item'] = {
            'localName': _('Add biblio hold'),
            'css': 'glyphicon-wrench',
        }
        return actions
         
    # Creates AJAX BiblioHoldForm bound to particular Biblio instance.
    def action_add_item(self):
        biblio = self.get_object_for_action()
        if biblio is None:
            return vm_list({
                'view': 'alert_error',
                'title': 'Error',
                'message': 'Unknown instance of Biblio'
            })
        hold_form = ReservesForm(initial={'biblio': biblio.pk})
        #hold_form = BiblioReservesForm(initial={'biblionumber': biblio.pk})
        # Generate hold_form viewmodel
        vms = self.vm_form(
            hold_form, form_action='save_item'
        )
        return vms
    # Validates and saves the Hold model instance via bound BiblioHoldForm.
    def action_save_item(self):
        #form = BiblioHoldForm(self.request.POST)
        form = ReservesForm(self.request.POST)
        if not form.is_valid():
            form_vms = vm_list()
            self.add_form_viewmodels(form, form_vms)
            return form_vms
        hold = form.save()
        biblio = hold.biblio
        if biblio.totalholds:
           biblio.totalholds+=1
        else:
           biblio.totalholds=1
        biblio.timestamp_updated = timezone.now()
        biblio.save()
        # Instantiate related HoldGrid to use it's .postprocess_qs() method
        # to update it's row via grid viewmodel 'prepend_rows' key value.
        hold_grid = HoldGrid()
        hold_grid.request = self.request
        hold_grid.init_class()
        return vm_list({
            'update_rows': self.postprocess_qs([biblio]),
            # return grid rows for client-side HoldGrid component .updatePage(),
            'hold_grid_view': {
                'prepend_rows': hold_grid.postprocess_qs([hold])
            }
        })     

class HoldGrid(KoGridView):
    model = Reserves
    form = BiblioHoldForm
    enable_deletion = True
    grid_fields = [
        'biblio__title',
        'borrower__firstname',
        'borrower__surname',
        'borrower__cardnumber',
        'borrower__email',
        'priority',
        'reservedate',
        'found',
        'waitingdate',
        'biblio__totalholds'
    ]
    allowed_sort_orders = [
        'biblio__id',
        'biblio__title',
        'priority',
        'reservedate',
        'biblio__totalholds',        
    ]
    search_fields = [
        ('biblio__title','icontains'),
        ('biblio__authors__firstname','icontains'),
        ('biblio__authors__lastname','icontains'),
        ('biblio__copyrightdate', 'iexact'),
        ('biblio__publisher__name', 'icontains'),
        ('biblio__genre__name', 'icontains'),
        ('biblio_id__callnumber', 'istartswith'),
        ('borrower__cardnumber', 'istartswith'),
        ('borrower__firstname', 'icontains'),
        ('borrower__surname', 'icontains'),
    ]
    allowed_filter_fields = OrderedDict([
        ('biblio', {
            'pageRoute': 'biblio_grid_simple',
            # Optional setting for BootstrapDialog:
            'dialogOptions': {'size': 'size-wide'},
        }),
        ('borrower', {
            'pageRoute': 'borrowers_fk_widget_grid'
        }),
        ('borrower__cardnumber', None)
    ])
    grid_options = {
        'searchPlaceholder': 'Search barrower',
    }

    def get_actions(self):
        # Disable adding new hold because BiblioHoldForm is incomplete (has no Biblio) for action 'create_form'.
        # BiblioHoldGrid.action_add_hold is used instead.
        actions = super().get_actions()
        actions['button']['create_form']['enabled'] = False
        return actions


#------------Biblio_Hold_grod-------------

class BiblioItemsGrid(EditableBiblioGrid):

    client_routes = {
        # Injected in djk_sample.context_processors.TemplateContextProcessor.CLIENT_ROUTES,
        # just for the test of global route injection.
        # 'item_grid',
        'biblio_grid_simple',
        'collectiondepartments_fk_widget_grid',
    }
    template_name = 'biblio_item.htm'
    form = BiblioForm
    form_with_inline_formsets = None
    search_fields = [
        ('title', 'icontains'),
        ('first_author__firstname', 'icontains'),
        ('first_author__lastname', 'icontains'),
        ('copyrightdate', 'iexact'),
        ('authors__firstname', 'icontains'),
        ('authors__lastname', 'icontains'),
        ('publisher__name', 'icontains'),
        ('genre__name', 'icontains'),
        ('pages', 'iexact'),
        ('items__barcode', 'iexact'),
        ('callnumber', 'istartswith'),
    ]

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
        item_form = BiblioItemsForm(initial={'biblionumber': biblio.pk})
        # Generate item_form viewmodel
        vms = self.vm_form(
            item_form, form_action='save_item'
        )
        return vms

    # Validates and saves the Item model instance via bound BiblioItemForm.
    def action_save_item(self):
        form = BiblioItemsForm(self.request.POST)
        if not form.is_valid():
            form_vms = vm_list()
            self.add_form_viewmodels(form, form_vms)
            return form_vms
        item = form.save()
        biblio = item.biblionumber
        #biblio.timestamp_updated = timezone.now()
        #biblio.save()
        # Instantiate related ItemGrid to use it's .postprocess_qs() method
        # to update it's row via grid viewmodel 'prepend_rows' key value.
        item_grid = ItemsGrid()
        item_grid.request = self.request
        item_grid.init_class()
        return vm_list({
            'update_rows': self.postprocess_qs([biblio]),
            # return grid rows for client-side ItemGrid component .updatePage(),
            'item_grid_view': {
                'prepend_rows': item_grid.postprocess_qs([item])
            }
        })


class ItemsGrid(KoGridView):
    model = Items
    form = BiblioItemsForm
    enable_deletion = True
    grid_fields = [
        'biblionumber',
        'collectiondepartment__deptcode',
        'barcode',
        'itemstatus',
    ]
    """
    search_fields = [
        ('barcode', 'iexact')
    ]
    """
    allowed_sort_orders = [
        'collectiondepartment__deptcode',
        'barcode',
        'itemstatus'
    ]
    search_fields = [
        ('collectiondepartment__deptcode','icontains'),
        ('barcode','iexact'),
        ('itemstatus','icontains'),
        ('biblionumber_id__title', 'icontains'),
        ('biblionumber_id__first_author__firstname', 'icontains'),
        ('biblionumber_id__first_author__lastname', 'icontains'),
        ('biblionumber_id__copyrightdate', 'iexact'),
        ('biblionumber_id__authors__firstname', 'icontains'),
        ('biblionumber_id__authors__lastname', 'icontains'),
        ('biblionumber_id__publisher__name', 'icontains'),
        ('biblionumber_id__genre__name', 'icontains'),
        ('biblionumber_id__pages', 'iexact'),
        ('biblionumber_id__callnumber', 'istartswith'),
    ]

    allowed_filter_fields = OrderedDict([
        ('biblionumber', {
            'pageRoute': 'biblio_grid_simple',
            # Optional setting for BootstrapDialog:
            'dialogOptions': {'size': 'size-wide'},
        }),
        ('collectiondepartment', {
            'pageRoute': 'collectiondepartments_fk_widget_grid'
        }),
        ('itemstatus', None)
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


class ReservesGrid(KoGridView):

    client_routes = {
        'reserve_grid',
        'biblio_grid_simple'
    }
    template_name = 'reserve_grid.htm'
    model = Reserves
    grid_fields = [
        'borrower', #---modified
        'biblio',
        # Compound columns:
        [
            # Will join 'temtype' field from related 'Biblio' table automatically via Django ORM.
            'biblio__itemtype',
            'biblio__language',
            'biblio__first_author',
            'biblio__publisher',
            'reservedate',
            #'borrower__category',
            #'borrower__cardnumber',
        ],
        #'patron__note',
        #'patron__is_active'
    ]
    search_fields = [
        ('biblio__title', 'icontains'),
        ('borrower__firstname', 'icontains'),
        ('borrower__surname', 'icontains'),
        ('borrower__cardnumber', 'icontains'),
    ]
    allowed_sort_orders = [
        'biblio', # -- modified
        # Will join 'category' field from related 'Biblio' table automatically via Django ORM.
        'biblio__itemtype',
        'biblio__first_author',
        'biblio__publisher',
        'reservedate',
        'borrower__cardnumber',
        #'patron__is_active'
    ]
    
    allowed_filter_fields = OrderedDict([
        ('biblio', None),
        ('reservedate', None),
        ('biblio__itemtype', None),
        #('biblio__author',None),
        #('biblio__publisher', None),
        #('borrower__category', None),
        #('borrower__cardnumber', None), #--modified
        #('borrower__is_active', None),
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
                'borrower': {
                    'pageRoute': 'borrowers_fk_widget_grid'
                },
                'biblio': {
                    'pageRoute': 'biblio_grid_simple',
                    # Optional setting for BootstrapDialog:
                    'dialogOptions': {'size': 'size-wide'},
                },
                'biblio__first_author': {
                    'pageRoute': 'authors_fk_widget_grid'                    
                },
                'biblio__language': {
                    'pageRoute': 'language_fk_widget_grid'                    
                },
                'biblio__corporateauthor': {
                    'pageRoute': 'corporateauthor_fk_widget_grid'                    
                },
                'biblio__publisher': {
                    'pageRoute': 'publisher_fk_widget_grid'
                },
                'biblio__subject_heading': {
                    'pageRoute': 'genre_fk_widget_grid'                    
                },
                
            }
        }

    # Overriding get_base_queryset() is not required, but is used to reduce number of queries.
    def get_base_queryset(self):
        return self.__class__.model.objects.select_related('biblio').all()
    
class BiblioReservesGrid(FormatTitleMixin, ReservesGrid):
    
    format_view_title = True
    grid_fields = [
        'borrower', #modified
        [
            'borrower__firstname',   
            'borrower__surname',
            'borrower__cardnumber',
            'borrower__category',
        ],
        [
            'reservedate',
            'priority', 
            'found',
        ],
        #'borrower__note',
    ]
    search_fields = [
        ('borrower__firstname', 'icontains'),
        ('borrower__surname', 'icontains'),
        ('borrower__cardnumber','iexact'),        
        ('borrower__category__categorycode','iexact'),        
    ]
    allowed_filter_fields = OrderedDict([
        #('patron', None),
        ('reservedate', None),
        ('priority',None),
        ('found', None),
    ])

    def get_base_queryset(self):
        return super().get_base_queryset().filter(biblio_id=self.kwargs['biblio_id'])

    def get(self, request, *args, **kwargs):
        biblio = Biblio.objects.filter(pk=self.kwargs['biblio_id']).first()
        if biblio is not None:
            self.format_title(biblio)
        return super().get(request, *args, **kwargs)


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

class AuthorsFkWidgetGrid(KoGridView):

    model = Authors
    form = AuthorsForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = ['firstname', 'lastname']
    allowed_sort_orders = '__all__'
    search_fields = [
        ('firstname', 'icontains'),
        ('lastname', 'icontains'),              
    ]

class CorporateAuthorFkWidgetGrid(KoGridView):

    model = CorporateAuthor
    form = CorporateAuthorForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = ['name']
    allowed_sort_orders = '__all__'
    search_fields = [
        ('name','icontains'),        
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

class LanguageFkWidgetGrid(KoGridView):

    model = Language
    form = LanguageForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    search_fields = [
        ('name', 'icontains'),
    ]

class BorrowersFkWidgetGrid(KoGridView):

    model = Borrowers
    form = BorrowersForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = ['firstname', 'surname','cardnumber']
    allowed_sort_orders = '__all__'
    search_fields = [
        ('firstname', 'icontains'),
        ('surname', 'icontains'),
        ('cardnumber','iexact'),        
    ]

class DepartmentsFkWidgetGrid(KoGridView):

    model = Departments
    form = DepartmentsForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    search_fields = [
        ('dept', 'icontains'),
        ('description', 'icontains'),
    ]
class CollectionDepartmentsFkWidgetGrid(KoGridView):

    model = CollectionDepartments
    form = CollectionDepartmentsForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    search_fields = [
        ('dept', 'icontains'),
        ('description', 'icontains'),
    ]

class DesignationsFkWidgetGrid(KoGridView):

    model = Designations
    form = DesignationsForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    search_fields = [
        ('designation', 'icontains'),
        ('description', 'icontains'),
    ]

class CategoriesFkWidgetGrid(KoGridView):

    model = Categories
    form = CategoriesForm
    enable_deletion = True
    force_str_desc = True
    grid_fields = '__all__'
    allowed_sort_orders = '__all__'
    search_fields = [
        ('categorycode', 'icontains'),
        ('description', 'icontains'),
    ]


class BiblioGridRawQuery(SimpleBiblioGrid):

    template_name = 'cbv_grid_breadcrumbs.htm'
    grid_fields = [
        'reserves__borrower__firstname',
        'reserves__borrower__surname',
        'reserves__borrower__category_id__categorycode',
        'reserves__priority',
        'title',
        'publisher__name',
        'first_author',
        'subject_heading__name',
        'totalissues',
        'itemtype',
    ]

    allowed_sort_orders = [
        #'reserves__borrower_category','publisher__name','subject_heading__name','first_author' 
        'reserves__borrower__firstname',
        'reserves__borrower__surname',
        'reserves__priority',
        'title',
        'totalissues',
        'itemtype',
    ]

    allowed_filter_fields = OrderedDict([
        ('itemtype', None),
        #('category', None),
        
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
        elif field_name == 'totalissues':
            return 'Biblio Total Issues'
        else:
            return super().get_field_verbose_name(field_name)

    def get_field_validator(self, fieldname):
        if fieldname == 'category':
            return self.__class__.field_validator(self, fieldname, model_class=Borrowers)
        else:
            return super().get_field_validator(fieldname)
    """
    def get_row_str_fields(self, obj, row=None):
        str_fields = super().get_row_str_fields(obj, row)
        if str_fields is None:
            str_fields = {}
        # Add formatted display of manually JOINed field.
        str_fields['category'] = get_choice_str(Categories.objects.all(), row['category'])
        return str_fields
    """
    def get_base_queryset(self):
        # Mostly supposed to work with LEFT JOIN. Might produce wrong results with arbitrary queries.
        raw_qs = self.model.objects.raw(
            'SELECT ils_app_biblio.*, ils_app_categories.categorycode,ils_app_reserves.priority, '            
            'ils_app_borrowers.firstname, ils_app_borrowers.surname FROM ils_app_biblio ' 
            'LEFT JOIN ils_app_reserves ON ils_app_biblio.biblionumber = ils_app_reserves.biblio_id '
            'LEFT JOIN ils_app_borrowers ON ils_app_borrowers.id = ils_app_reserves.borrower_id '
            'LEFT JOIN ils_app_categories on ils_app_categories.id = ils_app_borrowers.category_id '

            #'LEFT JOIN ils_app_author ON ils_app_author.id = ils_app_biblio.author_id ',
            #'LEFT JOIN ils_app_publisher ON ils_app_publisher.id = ils_app_biblio.publisher_id ',
            #'LEFT JOIN ils_app_genre ON ils_app_genre.id = ils_app_biblio.genre_id ',
        )
        fqs = FilteredRawQuerySet.clone_raw_queryset(
            raw_qs=raw_qs, relation_map={
                'category': 'reserves__borrower',
                'priority' : 'reserves',
                'firstname': 'reserves__borrower',
                'suranme': 'reserves__borrower',
                
            }
        )
        return fqs

