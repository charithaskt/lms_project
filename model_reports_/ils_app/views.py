from django.utils.html import format_html, mark_safe
from django.shortcuts import render

from django_jinja_knockout.utils.sdv import call_prop
from django_jinja_knockout.tpl import format_local_date, reverse, format_html_attrs, add_css_classes_to_dict
from django_jinja_knockout.views import (
    FormDetailView, InlineCreateView, InlineDetailView, InlineCrudView, ListSortingView, BsTabsMixin, ContextDataMixin
)

from djk_sample.middleware import ContextMiddleware

from .models import Biblio, Items, Reserves
from .models import Authors, Publisher, CorporateAuthor, CollectionDepartments,Genre, Language
from .models import Departments, Designations, Categories, Borrowers
from .forms import ItemsDisplayForm, BorrowersDisplayForm, BiblioFormWithInlineFormsets, BiblioDisplayFormWithInlineFormsets 
from .forms import PublisherForm, AuthorsForm, CorporateAuthor, GenreForm, BiblioDisplayForm, BiblioDisplayFormWithNoItemsInlineFormsets
from .forms import PublisherDisplayForm, AuthorsDisplayForm, CorporateAuthorDisplayForm, GenreDisplayForm, ReservesDisplayForm
from .forms import CategoriesDisplayForm, DepartmentsDisplayForm, DesignationsDisplayForm, CollectionDepartmentsDisplayForm
from .forms import CategoriesForm, DepartmentsForm, DesignationsForm, CollectionDepartmentsForm, LanguageForm, LanguageDisplayForm
from .models import itemtype_choices, item_status_choices, location_choices, notforloan_choices
from .forms import HoldDisplayForm,HoldForm 

def main_page(request):
    if request.method == 'GET':
        return render(request, 'main.htm')


class BiblioNavsMixin(BsTabsMixin):

    def get_main_navs(self, request, object_id=None):
        main_navs = [
            {'url': reverse('biblio_list'), 'text': 'List of biblios'},
            {'url': reverse('biblio_create'), 'text': 'Create new biblio'}
        ]
        if object_id is not None:
            main_navs.extend([
                {
                    'url': reverse('biblio_detail', kwargs={'biblionumber': object_id}),
                    'text': format_html('View "{}"', self.object.title)
                },
                {
                    'url': reverse('biblio_update', kwargs={'biblionumber': object_id}),
                    'text': format_html('Edit "{}"', self.object.title)
                }
            ])
        return main_navs


class BiblioEditMixin(BiblioNavsMixin):
    client_routes = {
        'authors_fk_widget_grid',
        'publisher_fk_widget_grid',
        'language_fk_widget_grid',
        'corporateauthor_fk_widget_grid',
        'genre_fk_widget_grid',
        'collectiondepartments_fk_widget_grid',
        'categories_fk_widget_grid',
        'departments_fk_widget_grid',
        'designations_fk_widget_grid',
        'borrowers_fk_widget_grid'
    }
    template_name = 'biblio_edit.htm'
    form_with_inline_formsets = BiblioFormWithInlineFormsets


class BiblioCreate(BiblioEditMixin, InlineCreateView):

    def get_bs_form_opts(self):
        return {
            'class': 'biblio',
            'title': 'Create collection biblio',
            'submit_text': 'Save collection biblio'
        }

    def get_success_url(self):
        return reverse('biblio_detail', kwargs={'biblionumber': self.object.pk})


class BiblioCreateDTL(BiblioCreate):

    template_name = 'biblio_create.html'


class BiblioUpdate(BiblioEditMixin, InlineCrudView):

    format_view_title = True
    pk_url_kwarg = 'biblionumber'

    def get_success_url(self):
        return reverse('biblio_detail', kwargs={'biblionumber': self.object.pk})

    def get_bs_form_opts(self):
        return {
            'class': 'biblio',
            'title': format_html('Edit "{}"', self.object),
            'submit_text': 'Save collection biblio'
        }


class BiblioDetail(BiblioNavsMixin, InlineDetailView):

    format_view_title = True
    pk_url_kwarg = 'biblionumber'
    template_name = 'biblio_edit.htm'
    form_with_inline_formsets = BiblioDisplayFormWithNoItemsInlineFormsets

    def get_bs_form_opts(self):
        return {
            'class': 'biblio',
            'title': format_html('"{}"', self.object),
        }

class PublisherDetail(FormDetailView):

    pk_url_kwarg = 'publisher_id'
    model = Publisher
    form_class = PublisherDisplayForm
    format_view_title = True

class AuthorDetail(FormDetailView):

    pk_url_kwarg = 'authors_id'
    model = Authors
    form_class = AuthorsDisplayForm
    format_view_title = True

class LanguageDetail(FormDetailView):

    pk_url_kwarg = 'language_id'
    model = Language
    form_class = LanguageDisplayForm
    format_view_title = True

class GenreDetail(FormDetailView):

    pk_url_kwarg = 'genre_id'
    model = Genre
    form_class = GenreDisplayForm
    format_view_title = True

class CorporateAuthorDetail(FormDetailView):

    pk_url_kwarg = 'corporateauthor_id'
    model = CorporateAuthor
    form_class = CorporateAuthorDisplayForm
    format_view_title = True

class DepartmentDetail(FormDetailView):

    pk_url_kwarg = 'departments_id'
    model = Departments
    form_class = DepartmentsDisplayForm
    format_view_title = True

class CollectionDepartmentDetail(FormDetailView):

    pk_url_kwarg = 'collectiondepartments_id'
    model = CollectionDepartments
    form_class = CollectionDepartmentsDisplayForm
    format_view_title = True

class DesignationDetail(FormDetailView):

    pk_url_kwarg = 'designations_id'
    model = Designations
    form_class = DesignationsDisplayForm
    format_view_title = True

class CategoryDetail(FormDetailView):

    pk_url_kwarg = 'categories_id'
    model = Categories
    form_class = CategoriesDisplayForm
    format_view_title = True


class BiblioList(ContextDataMixin, BiblioNavsMixin, ListSortingView):

    model = Biblio
    allowed_sort_orders = '__all__'
    extra_context_data = {
        'format_local_date': format_local_date
    }
    highlight_mode = 'linearRows'
    allowed_filter_fields = {
        'itemtype': None,
        #'publisher':None,
    }
    
    grid_fields = [
        'title',
        'first_author',
        'publisher',
        'subject_heading',
        'itemtype',        
        'totalissues',       
    ]

    def get_title_links(self, obj):
        links = [format_html(
            '<div><a href="{}">{}</a></div>',
            reverse('biblio_detail', kwargs={'biblionumber': obj.pk}),
            obj.title
        )]
        # is_authenticated is not callable in Django 2.0.
        if call_prop(ContextMiddleware.get_request().user.is_authenticated):
            links.append(format_html(
                '<a href="{}"><span class="glyphicon glyphicon-edit"></span></a>',
                reverse('biblio_update', kwargs={'biblionumber': obj.pk})
            ))
            links.append(format_html(
                '<a href="{}"><span class="glyphicon glyphicon-user"></span></a>',
                reverse('biblio_reserve_grid', kwargs={'action': '', 'biblio_id': obj.pk})
            ))
        return links

    def get_display_value(self, obj, field):
        if field == 'title':
            links = self.get_title_links(obj)
            return mark_safe(''.join(links))
        elif field == 'totalissues':
            return "{} issues & {} holds".format(super().get_display_value(obj,field), Reserves.objects.filter(biblio_id = obj.biblionumber).count())
        else:
            return super().get_display_value(obj, field)


class BiblioListWithComponent(BiblioList):

    client_routes = {
        'biblio_reserve_grid',
        'borrowers_fk_widget_grid',
    }
    template_name = 'biblio_list_with_component.htm'
    highlight_mode = 'cycleColumns'

    def get_table_attrs(self):
        table_attrs = super().get_table_attrs()
        add_css_classes_to_dict(table_attrs, 'rows-strong-border')
        return table_attrs

    def get_title_links(self, obj):
        links = super().get_title_links(obj)
        links.append(format_html_attrs(
            ' <button {attrs}>'
            '<span class="glyphicon glyphicon-user"></span> See inline'
            '</button>',
            attrs={
                'class': 'component btn btn-sm btn-info',
                'data-event': 'click',
                'data-component-class': 'App.GridDialog',
                'data-component-options': {
                    'filterOptions': {
                        'pageRoute': 'biblio_reserve_grid',
                        'pageRouteKwargs': {'biblio_id': obj.pk},
                        'fkGridOptions': {
                            'borrower': 'borrowers_fk_widget_grid',
                        }
                    }
                }
            }
        ))
        return links


class BiblioListDTL(BiblioList):
    template_name = 'biblio_list.html'


class ItemDetail(FormDetailView):

    pk_url_kwarg = 'itemnumber'
    model = Items
    form_class = ItemsDisplayForm
    format_view_title = True

class HoldDetail(FormDetailView):

    pk_url_kwarg = 'reserveid'
    model = Items
    form_class = HoldDisplayForm
    format_view_title = True


class ReserveDetail(FormDetailView):

    pk_url_kwarg = 'reserve_id'
    model = Reserves
    form_class = ReservesDisplayForm
    format_view_title = True
