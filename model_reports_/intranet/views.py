from django.shortcuts import render
from django.shortcuts import render
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableView 
from django_tables2.paginators import LazyPaginator 
from .models import Borrowers
from .tables import BorrowersTable
from django_tables2.export.views import ExportMixin

def borrowers(request):
    table = BorrowersTable(data=Borrowers.objects.all(), template_name='django_tables2/bootstrap-responsive.html')
    #table.paginate(page=request.GET.get('page',1),per_page=1)
    #the above is when not using RequestConfig
    RequestConfig(request, paginate={'per_page':3}).configure(table)
    return render(request, 'intranet/borrowers.html', {'table': table})

class BorrowersListView(SingleTableView):
    table_class = BorrowersTable
    table_data = Borrowers.objects.all()
    pagination_class =  LazyPaginator
    template_name='intranet/borrowers.html'
    def get_queryset(self):
       return Person.objects.all()

    #http://localhost:8001/borrowers/?per_page=1&page=2 to get pagination

def borrowers_listing(request):
    config = RequestConfig(request)
    table1 = BorrowersTable(Borrowers.objects.all(), prefix='1-')
    table2 = BorrowersTable(Borrowers.objects.all(), prefix='2-')
    config.configure(table1)
    config.configure(table2)
    return render(request, 'intranet/borrowers-listing.html', {
        'table1': table1,
        'table2': table2
    })

from django_tables2 import MultiTableMixin
from django.views.generic.base import TemplateView
class BorrowersTablesView(MultiTableMixin, TemplateView):
    template_name = 'intranet/multiTable.html'
    qs = Borrowers.objects.all()
    tables = [
        BorrowersTable(qs, 'debarred', 'debarrednote'),
        BorrowersTable(qs, exclude=('debarrednote','lost','gonenoaddress' ))
    ]
    table_pagination = {
        'per_page': 3
    }

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin

import django_filters

class BorrowersFilter(django_filters.FilterSet):
    firstname = django_filters.CharFilter(lookup_expr='icontains', label='First Name')
    surname = django_filters.CharFilter(lookup_expr='icontains', label='Last Name')
    email = django_filters.CharFilter(lookup_expr='iexact', label='Email ID')
    cardnumber = django_filters.CharFilter(lookup_expr='iexact', label='Cardnumber')
    dateenrolled = django_filters.DateFilter(lookup_expr='iexact', label='Date Enrolled')
    class Meta:
        model = Borrowers
        fields = ['id','firstname', 'surname','cardnumber','email','dateenrolled']

class FilteredBorrowersListView(SingleTableMixin,ExportMixin, FilterView):
    table_class = BorrowersTable
    model = Borrowers
    template_name = 'intranet/filtered_borrowers.html'
    filterset_class = BorrowersFilter

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from intranet.models import Borrowers
from intranet.tables import BorrowersTable

def borrowers_table_export_view(request):
    table = BorrowersTable(Borrowers.objects.all())
    table.export_formats = {'csv','json','latex', 'ods', 'tsv', 'xls'}
    RequestConfig(request).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, exclude_columns=('selection','patron','photo'))
        return exporter.response('borrowerstable.{}'.format(export_format))
    return render(request, 'intranet/borrowers_export.html', {
        'table': table
    })
from django.shortcuts import render
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableView 
from django_tables2.paginators import LazyPaginator 
from .models import Biblio, Items
from .tables import BiblioTable
def biblios(request):
    table = BiblioTable(data=Biblio.objects.all(), template_name='django_tables2/bootstrap-responsive.html')
    RequestConfig(request, paginate={'per_page':4}).configure(table)
    return render(request, 'intranet/biblios.html', {'table': table})

class BibliosListView(SingleTableView):
    table_class = BiblioTable
    table_data = Biblio.objects.all()
    pagination_class =  LazyPaginator
    template_name='intranet/biblios.html'
    def get_queryset(self):
       return Biblio.objects.all()

def biblios_listing(request):
    config = RequestConfig(request)
    table1 = BiblioTable(Biblio.objects.all(), prefix='1-')
    table2 = BiblioTable(Biblio.objects.all(), prefix='2-')
    config.configure(table1)
    config.configure(table2)
    return render(request, 'intranet/biblios-listing.html', {
        'table1': table1,
        'table2': table2
    })

from django_tables2 import MultiTableMixin
from django.views.generic.base import TemplateView
class BibliosTablesView(MultiTableMixin,TemplateView):
    template_name = 'intranet/multiTable.html'
    qs = Biblio.objects.all()
    tables = [
        BiblioTable(qs),
        BiblioTable(qs, exclude=('id','size', ))
    ]
    table_pagination = {
        'per_page': 10
    }

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.views import ExportMixin

import django_filters
from intranet.models import itemtype_choices, Genre
class BibliosFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    #copyrightdate = django_filters.CharFilter(lookup_expr='iexact', label='Year')
    copyrightdate = django_filters.RangeFilter(lookup_expr='iexact', label='Year')
    pages = django_filters.CharFilter(lookup_expr='iexact', label='Pages')
    edition = django_filters.CharFilter(lookup_expr='iexact', label='Edition')
    authors__firstname = django_filters.CharFilter(lookup_expr='icontains', label='Author First Name')
    authors__lastname = django_filters.CharFilter(lookup_expr='icontains', label='Author Last Name')
    #genre__name  = django_filters.CharFilter(lookup_expr='icontains', label='Subject')
    callnumber  = django_filters.CharFilter(lookup_expr='icontains', label='Call Number')
    #itemtype   = django_filters.ChoiceFilter(choices=itemtype_choices, empty_label='Select - Item Type')
    itemtype   = django_filters.MultipleChoiceFilter(choices=itemtype_choices)
    genre__name = django_filters.ModelChoiceFilter(queryset=Genre.objects.all(),empty_label='Select - Subject Heading')
    class Meta:
        model = Biblio
        fields = ['biblionumber','title', 'authors__firstname','authors__lastname','genre__name','copyrightdate','pages','edition','itemtype']


class FilteredBibliosListView(ExportMixin,SingleTableMixin, FilterView):
    table_class = BiblioTable
    model = Biblio
    template_name = 'intranet/filtered_biblios.html'
    #template_name = 'django_tables2/bootstrap.html'
    filterset_class = BibliosFilter
    exclude_columns = ('selection','biblio','photo')
    #to export the filtered results of the table just add &_export=fmt where fmt in ['csv','json','xls']

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from .models import Biblio
from .tables import BiblioTable

def biblios_table_export_view(request):
    table = BiblioTable(Biblio.objects.all())
    table.export_formats = {'csv','json','latex', 'ods', 'tsv', 'xls' }
    RequestConfig(request).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, exclude_columns=('selection','biblio','photo'))
        return exporter.response('bibliostable.{}'.format(export_format))
    return render(request, 'intranet/biblios_export.html', {
        'table': table
    })


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from intranet.models import SystemPreferences
from intranet.forms import EditSystemPreferenceForm
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

class SystemPreferencesListView(PermissionRequiredMixin,generic.ListView):
    permission_required = ('intranet.change_systempreference',)
    model = SystemPreferences
    template_name = 'intranet/system_preferences_list.html'
    paginate_by = 10
    def get_queryset(self):
        return SystemPreferences.objects.all()

@permission_required('intranet.change_systempreference')
def systempreference_detail_view(request, pk):
    preference = get_object_or_404(SystemPreferences, pk=pk)
    if preference.vartype in ['YesNo','Choice']:
       choices = preference.descriptive_options.split('|')
       preference.value = choices[int(preference.value)]
    return render(request, 'intranet/systempreference_detail.html', 
       context={'preference': preference})

@permission_required('intranet.change_systempreference')
def edit_system_preference(request, pk):
    preference = get_object_or_404(SystemPreferences, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = EditSystemPreferenceForm(request.POST,instance=preference, initial={'variable':preference.variable,
              'value':preference.value, 'options':preference.options, 'descriptive_options':preference.descriptive_options,
              'explanation':preference.explanation,'vartype':preference.vartype})

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            preference.value = form.cleaned_data['value']
            print('value=',preference.value)
            preference.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('system-preference-detail', args=[pk]))
    # If this is a GET (or any other method) create the default form.
    else:
       if preference:

         form = EditSystemPreferenceForm(instance=preference,initial={'variable':preference.variable,
              'value':preference.value, 'options':preference.options, 'descriptive_options':preference.descriptive_options,
              'explanation':preference.explanation,'vartype':preference.vartype} )
       else:
         form = EditSystemPreferenceForm()

    context = {
        'form': form,
        'preference': preference,
    }

    return render(request, 'intranet/edit_system_preference.html', context)


from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET

from djangoql.exceptions import DjangoQLError
from djangoql.queryset import apply_search
from djangoql.schema import DjangoQLSchema, IntField
import datetime
from django.utils import timezone
from django.db.models import Q
from accounts.models import User, Profile
from intranet.models import Borrowers
import json
class UserDateJoinedYear(IntField):
    name = 'date_joined_year'

    def get_lookup_name(self):
        return 'timestamp_added__year'

from djangoql.schema import DjangoQLSchema, IntField

class UserAgeField(IntField):
    """
    Search by given number of full years
    """
    model = User
    name = 'age'

    def get_lookup_name(self):
        """
        We'll be doing comparisons vs. this model field
        """
        return 'timestamp_added__date'

    def get_lookup(self, path, operator, value):
        """
        The lookup should support with all operators compatible with IntField
        """
        if operator == 'in':
            result = None
            for year in value:
                condition = self.get_lookup(path, '=', year)
                result = condition if result is None else result | condition
            return result
        elif operator == 'not in':
            result = None
            for year in value:
                condition = self.get_lookup(path, '!=', year)
                result = condition if result is None else result & condition
            return result

        value = self.get_lookup_value(value)
        search_field = '__'.join(path + [self.get_lookup_name()])
        year_start = self.years_ago(value + 1)
        year_end = self.years_ago(value)
        if operator == '=':
            return (
                Q(**{'%s__gt' % search_field: year_start}) &
                Q(**{'%s__lte' % search_field: year_end})
            )
        elif operator == '!=':
            return (
                Q(**{'%s__lte' % search_field: year_start}) |
                Q(**{'%s__gt' % search_field: year_end})
            )
        elif operator == '>':
            return Q(**{'%s__lt' % search_field: year_start})
        elif operator == '>=':
            return Q(**{'%s__lte' % search_field: year_end})
        elif operator == '<':
            return Q(**{'%s__gt' % search_field: year_end})
        elif operator == '<=':
            return Q(**{'%s__gte' % search_field: year_start})

    def years_ago(self, n):
        timestamp = timezone.now()
        try:
            return timestamp.replace(year=timestamp.year - n)
        except ValueError:
            # February 29
            return timestamp.replace(month=2, day=28, year=timestamp.year - n)

class UserQLSchema(DjangoQLSchema):
    include = (User,Profile,Borrowers)
    def get_fields(self, model):
        fields = super(UserQLSchema, self).get_fields(model)
        if model == User:
            fields = [UserDateJoinedYear(), UserAgeField()] + fields
        return fields


@require_GET
def user_search_query(request):
    q = request.GET.get('q', '')
    error = ''
    query = User.objects.all().order_by('email')
    if q:
        try:
            query = apply_search(query, q, schema=UserQLSchema)
        except DjangoQLError as e:
            query = query.none()
            error = str(e)
    return render_to_response('user_search_query.html', {
        'q': q,
        'error': error,
        'search_results': query,
        'introspections': json.dumps(UserQLSchema(query.model).as_dict()),
    })
