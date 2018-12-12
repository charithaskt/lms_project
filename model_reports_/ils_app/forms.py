from django.utils.html import format_html
from django import forms
from django.forms.models import BaseInlineFormSet

from django_jinja_knockout.widgets import DisplayText, ForeignKeyGridWidget, PrefillWidget
from django_jinja_knockout.forms import (
    RendererModelForm, WidgetInstancesMixin, DisplayModelMetaclass,
    FormWithInlineFormsets, ko_inlineformset_factory
)
from django_jinja_knockout.query import ListQuerySet
from django_jinja_knockout.tpl import format_html_attrs

from djk_sample.middleware import ContextMiddleware
from event_app.models import Action
from .models import Borrowers, Biblio, Items, Reserves
from .models import Authors, CorporateAuthor, Publisher, Genre, Language, Departments, CollectionDepartments, Designations
from .models import Categories, itemtype_choices,item_status_choices, location_choices, notforloan_choices
from intranet.models import PatronPhotos

class CategoriesForm(RendererModelForm):

    class Meta:
        model = Categories
        fields = '__all__'

class DepartmentsForm(RendererModelForm):

    class Meta:
        model = Departments
        fields = '__all__'

class DesignationsForm(RendererModelForm):

    class Meta:
        model = Designations 
        fields = '__all__'

class CategoriesDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Categories
        fields = '__all__'

class DepartmentsDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Departments
        fields = '__all__'

class DesignationsDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

   class Meta:
        model = Designations
        fields = '__all__'

class BorrowersForm(RendererModelForm):

    class Meta:
        model = Borrowers
        fields = '__all__'
        exclude = ('timestamp_updated',)
        widgets = {
            'category': ForeignKeyGridWidget(model=Categories, grid_options={
                'pageRoute': 'categories_fk_widget_grid',
            }),
            'department': ForeignKeyGridWidget(model=Departments, grid_options={
                'selectMultipleRows': True,
                'pageRoute': 'departments_fk_widget_grid',
            }),
            'designation': ForeignKeyGridWidget(model=Designations, grid_options={
                'selectMultipleRows': True,
                'pageRoute': 'designations_fk_widget_grid',
            }),
            
        }
        
    def clean(self):
        super().clean()
        cardnumber = self.cleaned_data.get('cardnumber')     

    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
           ContextMiddleware().add_action(obj, action_type)
        return obj

class BorrowersDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:

        model = Borrowers
        fields = '__all__'

class ReservesDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:

        model = Reserves
        fields = '__all__'

class CollectionDepartmentsForm(RendererModelForm):

    class Meta:
        model = CollectionDepartments
        fields = '__all__'


class LanguageForm(RendererModelForm):

    class Meta:
        model = Language
        fields = '__all__'

class AuthorsForm(RendererModelForm):

    class Meta:
        model = Authors
        fields = '__all__'

class CorporateAuthorForm(RendererModelForm):

    class Meta:
        model = CorporateAuthor
        fields = '__all__'

class GenreForm(RendererModelForm):

    class Meta:
        model = Genre
        fields = '__all__'

class PublisherForm(RendererModelForm):

    class Meta:
        model = Publisher 
        fields = '__all__'

class BiblioForm(RendererModelForm):

    class Meta(RendererModelForm.Meta):
        model = Biblio
        fields = '__all__'
        exclude = ('timestamp_updated',)
        widgets = {
            'publisher': ForeignKeyGridWidget(model=Publisher, grid_options={
                'pageRoute': 'publisher_fk_widget_grid',
            }),
            'language': ForeignKeyGridWidget(model=Language, grid_options={
                'pageRoute': 'language_fk_widget_grid',
            }),
            'first_author': ForeignKeyGridWidget(model=Authors, grid_options={
                'selectMultipleRows': True,
                'pageRoute': 'authors_fk_widget_grid',
            }),
            'corporateauthor': ForeignKeyGridWidget(model=CorporateAuthor, grid_options={
                'selectMultipleRows': True,
                'pageRoute': 'corporateauthor_fk_widget_grid',
            }),
            'subject_heading': ForeignKeyGridWidget(model=Genre, grid_options={
                'pageRoute': 'genre_fk_widget_grid',
            }),
            'itemtype': forms.RadioSelect()
        }
  
    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj

class BiblioDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta(BiblioForm.Meta):
        widgets = {
            'publisher': ForeignKeyGridWidget(model=Publisher, grid_options={
                'pageRoute': 'publisher_fk_widget_grid',
            }),
            'language': ForeignKeyGridWidget(model=Language, grid_options={
                'pageRoute': 'language_fk_widget_grid',
            }),
            'first_author': ForeignKeyGridWidget(model=Authors, grid_options={
                'selectMultipleRows': True,
                'pageRoute': 'authors_fk_widget_grid',
            }),
            'corporateauthor': ForeignKeyGridWidget(model=CorporateAuthor, grid_options={
                'selectMultipleRows': True,
                'pageRoute': 'corporateauthor_fk_widget_grid',
            }),
            'subject_heading': ForeignKeyGridWidget(model=Genre, grid_options={
                'pageRoute': 'genre_fk_widget_grid',
            }),
            'itemtype': DisplayText()
        }

class BiblioNoEditDisplayForm(RendererModelForm, metaclass=DisplayModelMetaclass):
    class Meta:
        model = Biblio
        fields = '__all__'

class PublisherDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Publisher
        fields = '__all__'

class LanguageDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Language
        fields = '__all__'

class CollectionDepartmentsDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = CollectionDepartments
        fields = '__all__'


class AuthorsDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Authors
        fields = '__all__'

class CorporateAuthorDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = CorporateAuthor
        fields = '__all__'


class GenreDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Genre
        fields = '__all__'

class ItemsForm(RendererModelForm):

    inline_template = 'inline_item_form.htm'

    class Meta:
        model = Items
        fields = '__all__'
        widgets = {
            'collectiondepartment': ForeignKeyGridWidget(model=CollectionDepartments, grid_options={
                'pageRoute': 'collectiondepartments_fk_widget_grid',
            }),
            'itemstatus': forms.RadioSelect()
        }

    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj


class ItemsDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Items
        fields = '__all__'

class HoldDisplayForm(WidgetInstancesMixin, RendererModelForm, metaclass=DisplayModelMetaclass):

    class Meta:
        model = Reserves
        fields = '__all__'

class BiblioItemsForm(ItemsForm):

    class Meta(ItemsForm.Meta):
        widgets = {
            'biblio': forms.HiddenInput(),
            'collectiondepartment': ForeignKeyGridWidget(model=CollectionDepartments, grid_options={
                'pageRoute': 'collectiondepartments_fk_widget_grid',
            }),
            'itemstatus': forms.RadioSelect()
        }

"""
class HoldForm(RendererModelForm):

    inline_template = 'inline_hold_form.htm'

    class Meta:
        model = Reserves
        fields = '__all__'
        widgets = {
            'borrower': ForeignKeyGridWidget(model=Borrowers, grid_options={
                'pageRoute': 'borrowers_fk_widget_grid',
            }),
            
        }

    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj

"""


class ReservesForm(RendererModelForm):
    class Meta:
        model = Reserves
        fields = '__all__'
        widgets = {
            'borrower': ForeignKeyGridWidget(model=Borrowers, grid_options={
                'pageRoute': 'borrowers_fk_widget_grid',
                'dialogOptions': {'size': 'size-wide'},
            }),
            
        }

    def clean(self):
        super().clean()
        
    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj

class HoldForm(RendererModelForm):

    class Meta:
        model = Reserves
        fields = '__all__'
        widgets = {
            'borrower': ForeignKeyGridWidget(model=Borrowers, grid_options={
                'pageRoute': 'borrowers_fk_widget_grid',
                'dialogOptions': {'size': 'size-wide'},
            }),
            'biblio': ForeignKeyGridWidget(model=Biblio, grid_options={
                'pageRoute': 'biblio_grid_simple',
            }),
                   
        }

    def clean(self):
        super().clean()
        
    def save(self, commit=True):
        action_type = Action.TYPE_CREATED if self.instance.pk is None else Action.TYPE_MODIFIED
        obj = super().save(commit=commit)
        if self.has_changed():
            ContextMiddleware().add_action(obj, action_type)
        return obj

class BiblioHoldForm(HoldForm):

    class Meta(HoldForm.Meta):
        widgets = {
            'biblio': forms.HiddenInput(),
            'borrower': ForeignKeyGridWidget(model=Borrowers, grid_options={
                'pageRoute': 'borrowers_fk_widget_grid',
            }),            
        }
class BiblioReservesForm(HoldForm):

    class Meta(HoldForm.Meta):
        widgets = {
            'biblio': forms.HiddenInput(),
            'borrower': ForeignKeyGridWidget(model=Borrowers, grid_options={
                'pageRoute': 'borrowers_fk_widget_grid',
            }),
        }

BiblioItemsFormSet = ko_inlineformset_factory(
    Biblio, Items, form=ItemsForm, extra=0, min_num=1, max_num=5, can_delete=True
)
BiblioItemsFormSet.template = 'biblio_item_formset.htm'

BiblioDisplayItemsFormSet = ko_inlineformset_factory(
    Biblio, Items, form=ItemsDisplayForm
)


BiblioHoldFormSet = ko_inlineformset_factory(
    Biblio, Reserves, form=HoldForm, extra=0, min_num=1, max_num=5, can_delete=True
)
BiblioHoldFormSet.template = 'biblio_hold_formset.htm'
BiblioDisplayHoldFormSet = ko_inlineformset_factory(
    Biblio, Reserves, form=HoldDisplayForm
)


class BiblioReservesFormSetCls(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Not a nice way to load widget data, but formset factories are a bit too inflexible.
        # todo: Load with AJAX calls can be implemented in cleaner way.
        request = ContextMiddleware.get_request()
        self.related_biblios_qs = ListQuerySet(
            Reserves.objects.filter(
                biblio__biblionumber=request.view_kwargs.get('biblio_id', None)
                #biblio__id=request.view_kwargs.get('biblio_id', None)
            )
        )

    def add_fields(self, form, index):
        super().add_fields(form, index)
   
    def clean(self):
        if any(self.errors):
            return
        categories = []
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                # Do not validate deleted forms.
                continue
            # Warning! May be None, thus dict.get() is used.

class BiblioHoldFormSetCls(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Not a nice way to load widget data, but formset factories are a bit too inflexible.
        # todo: Load with AJAX calls can be implemented in cleaner way.
        request = ContextMiddleware.get_request()
        self.related_biblios_qs = ListQuerySet(
            Reserves.objects.filter(
                biblio__biblionumber=request.view_kwargs.get('biblio_id', None)
                #biblio__id=request.view_kwargs.get('biblio_id', None)
            )
        )

    def add_fields(self, form, index):
        super().add_fields(form, index)
   
    def clean(self):
        if any(self.errors):
            return
        categories = []
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                # Do not validate deleted forms.
                continue
            # Warning! May be None, thus dict.get() is used.

BiblioReservesFormSet = ko_inlineformset_factory(
    Biblio, Reserves, form=ReservesForm, formset=BiblioReservesFormSetCls, extra=0, min_num=0, max_num=10, can_delete=True
)
BiblioDisplayReservesFormSet = ko_inlineformset_factory(
    Biblio, Reserves, form=BorrowersDisplayForm
)
BiblioHoldFormSet = ko_inlineformset_factory(
    Biblio, Reserves, form=HoldForm, formset=BiblioHoldFormSetCls, extra=0, min_num=0, max_num=10, can_delete=True
)
BiblioDisplayHoldFormSet = ko_inlineformset_factory(
    Biblio, Reserves, form=BorrowersDisplayForm
)
class BiblioFormWithInlineFormsets(FormWithInlineFormsets):

    FormClass = BiblioForm
    FormsetClasses = [BiblioItemsFormSet, BiblioReservesFormSet]
    prefix = 'test'


class BiblioDisplayFormWithInlineFormsets(FormWithInlineFormsets):

    FormClass = BiblioDisplayForm
    FormsetClasses = [BiblioDisplayItemsFormSet, BiblioDisplayReservesFormSet]

class BiblioDisplayFormWithNoItemsInlineFormsets(FormWithInlineFormsets):

    FormClass = BiblioNoEditDisplayForm
