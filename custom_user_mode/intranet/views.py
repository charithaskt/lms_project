from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableView 
from django_tables2.paginators import LazyPaginator 
from .models import Borrowers
from .tables import BorrowersTable

def borrowers(request):
    table = BorrowersTable(data=Borrowers.objects.all(), template_name='django_tables2/bootstrap-responsive.html')
    #table.paginate(page=request.GET.get('page',1),per_page=1)
    #the above is when not using RequestConfig
    RequestConfig(request, paginate={'per_page':1}).configure(table)
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
        'per_page': 2
    }

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

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

class FilteredBorrowersListView(SingleTableMixin, FilterView):
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
    table.export_formats = {'csv','json','latex', 'ods', 'tsv', 'xls', 'xlsx', 'yml'}
    RequestConfig(request).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, exclude_columns=('selection','patron','photo'))
        return exporter.response('borrowerstable.{}'.format(export_format))
    return render(request, 'intranet/borrowers_export.html', {
        'table': table
    })
#--------------
from django.shortcuts import render
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableView 
from django_tables2.paginators import LazyPaginator 
from .models import Biblio, Items
from .tables import BiblioTable
def biblios(request):
    table = BiblioTable(data=Biblio.objects.all(), template_name='django_tables2/bootstrap-responsive.html')
    RequestConfig(request, paginate={'per_page':1}).configure(table)
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
class BibliosTablesView(MultiTableMixin, TemplateView):
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
    exclude_columns = ('selection','biblio')
    #to export the filtered results of the table just add &_export=fmt where fmt in ['csv','json','xls']

from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport
from .models import Biblio
from .tables import BiblioTable

def biblios_table_export_view(request):
    table = BiblioTable(Biblio.objects.all())
    table.export_formats = {'csv','json','latex', 'ods', 'tsv', 'xls', 'xlsx', 'yml'}
    RequestConfig(request).configure(table)
    export_format = request.GET.get('_export', None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table, exclude_columns=('selection','biblio'))
        return exporter.response('bibliostable.{}'.format(export_format))
    return render(request, 'intranet/biblios_export.html', {
        'table': table
    })

'''
fromm djqscsv import write_csv

qs = Foo.objects.filter(bar=True).values('id', 'bar')
with open('foo.csv', 'wb') as csv_file:
  write_csv(qs, csv_file)
'''
