import django_tables2 as tables
from .models import Borrowers, PatronPhotos
from django.db.models.functions import Length
import itertools
from django.db.models import F
from photos.models import PatronBulkPhotos
class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)


class PatronColumn(tables.Column):
    attrs = {
        'td': {
            'data-first-name': lambda record: record.firstname,
            'data-last-name': lambda record: record.surname,
            'data-card-number': lambda record: record.cardnumber,
            'data-email-id': lambda record: record.email
        }
    }
    def order(self, QuerySet, is_descending):
        QuerySet = QuerySet.annotate( 
            issues = F('totalissues')  
        ).order_by(('-' if is_descending else '') + 'issues')
        return (QuerySet,True)

    def render(self, record):
        return '{}, {}'.format(record.firstname, record.surname)

from django.utils.html import format_html
class ImageColumn(tables.Column):
    def render(self, record):
        return format_html('<img src="/static/intranet/media/images/patronimages/image_{}.jpg " width="150" />', record.id)

class ImageOneColumn(tables.Column):
    def render(self, record):
        try:
            photo_ = PatronPhotos.objects.get(patron_id=record.id)
            if photo_: 
                return format_html('<img src="/media/{}" width="150" />', photo_.imageurl)
        except:
            try:
               borr = Borrowers.objects.get(id=record.id)
               photo_= PatronBulkPhotos.objects.get(patron_id=borr)
               if photo_: 
                  return format_html('<img src="/media/{}" width="150" />', photo_.file)
            except:
               print('error encountered')
               pass
        return format_html('<img src="" />')


class CheckBoxColumnWithName(tables.CheckBoxColumn):
    @property
    def header(self):
        return self.verbose_name

class UsefulMixin(tables.Table):
    #row_number = tables.Column(footer='Total',attrs={'tf':{'class':'label label-success'}}, orderable=False, empty_values=())
    row_number = tables.Column(footer='Total',attrs={'tf':{'bgcolor':'red'}}, orderable=False, empty_values=())
class BorrowersTable(UsefulMixin,tables.Table):
    #selection = tables.CheckBoxColumn(accessor='pk',orderable=False)
    selection = tables.TemplateColumn('<input type="checkbox" value="{{ record.pk }}" />', verbose_name="Row Select", orderable=False)
    #selection = CheckBoxColumnWithName(verbose_name="Amend",accessor='pk',orderable=False)
    #row_number = tables.Column(footer='Total',orderable=False, empty_values=())
    #name = tables.Column(order_by=('firstname','surname'))
    patron = PatronColumn(orderable=False,empty_values=())
    #totalissues = tables.Column(footer=lambda table: sum([x.totalissues for x in table.data]),attrs={'tf':{'bgcolor':'red'}}) #note this is essential
    #totalissues = tables.Column(footer=lambda table: sum([x.totalissues for x in table.data])) #note this is essential
    totalissues = SummingColumn(orderable=False,attrs={'tf':{'bgcolor':'red'}}) 
    id = tables.Column(accessor='pk',localize=False)
    #photo = ImageColumn(empty_values=())
    photo = ImageOneColumn(empty_values=())
    class Meta:
        model = Borrowers
        sequence = ('selection','row_number','id','firstname','surname','email','totalissues','photo','...')
        unlocalize=('id',)
        #localize=('shirts','pants','clothing',)
        #template_name = 'django_tables2/semantic.html'
        #template_name = 'django_tables2/bootstrap4.html'
        #template_name = 'django_tables2/bootstrap.html'
        template_name = 'django_tables2/bootstrap-responsive.html'
        #attrs = {'class': 'mytable'} #table level
        attrs = {'tf':{'bgcolor':'#abdfcc'}, 'th':{'bgcolor':'#abdfcc'}} #table level
        row_attrs = {
            'data-id': lambda record: record.pk
        } #td element in tr

    def __init__(self, *args, **kwargs):
        super(BorrowersTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count() #returns a iterator object
    
    def render_row_number(self):
        return 'Row[%s]' % str(next(self.counter) + 1)

    def render_totalissues(self, record):
           totalissues = record.totalissues 
           return str(totalissues)

    def value_totaissues(self, record):
           totalissues = record.totalissues 
           return str(totalissues)


    def order_photo ( self , QuerySet, is_descending): 
        QuerySet = QuerySet .annotate(length=Length('firstname')).order_by(('-' if is_descending else '') + 'length') 
        return (QuerySet, True) 
    
#-------------
from intranet.models import Biblio, Items
class UpperColumn(tables.Column):
    def render(self, value):
        return value.upper()

    def order(self, QuerySet, is_descending):
        QuerySet = QuerySet.annotate( 
            issues = F('totalissues') 
        ).order_by(('-' if is_descending else '') + 'issues')
        return (QuerySet,True)

class CopiesColumn(tables.Column):
    def render(self, record):
        item_count = Items.objects.filter(biblionumber_id=record.biblionumber).count()
        return str(item_count) 
        
    def order(self, QuerySet, is_descending):
        QuerySet = QuerySet.annotate( 
            qty = F('copies')  
        ).order_by(('-' if is_descending else '') + 'qty')
        return (QuerySet,True)
    '''
    def render_footer(self, bound_column, table):
        #return sum(bound_column.accessor.resolve(row) for row in table.data) 
        return sum(Items.objects.filter(biblionumber_id=table.data['biblionumber']).count() for row in table.data)
        #return sum([row.copies for row in table.data]) 
    '''

class BiblioAuthorsColumn(tables.Column):
    attrs = {
        'td': {
            'data-title-name': lambda record: record.title,
            'data-authors': lambda record: record.all_authors
        }
    }

    '''
    def order(self, QuerySet, is_descending):
        QuerySet = QuerySet.annotate( 
            issues = F('totalissues') 
        ).order_by(('-' if is_descending else '') + 'issues')
        return (QuerySet,True)
    '''

    def render(self, record):
        return '{}'.format(record.all_authors)

class BiblioGenresColumn(tables.Column):
    attrs = {
        'td': {
            'data-title-name': lambda record: record.title,
            'data-genres': lambda record: record.all_genres
        }
    }
    '''
    def order(self, QuerySet, is_descending):
        QuerySet = QuerySet.annotate( 
            issues = F('totalissues') 
        ).order_by(('-' if is_descending else '') + 'issues')
    '''

    def render(self, record):
        return '{}'.format(record.all_genres)

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)

class BiblioTable(UsefulMixin,tables.Table):
    selection = CheckBoxColumnWithName(verbose_name="Amend",accessor='pk',orderable=False)
    row_number = tables.Column(footer='Total',orderable=False, empty_values=())
    id = tables.Column(accessor='pk',localize=False)
    title = UpperColumn()
    authors = BiblioAuthorsColumn(empty_values=())
    genre = BiblioGenresColumn(empty_values=())
    totalissues = SummingColumn(attrs={'tf':{'bgcolor':'red'}}) 
    copies = CopiesColumn(orderable=False,empty_values=())
    #photo = ImageOneColumn(empty_values=())
    class Meta:
        model = Biblio
        sequence = ('selection','row_number','biblionumber','title','copyrightdate','edition','pages','totalissues','authors','genre','...')
        unlocalize=('biblionumber',)
        localize=('totalissues',)
        #template_name = 'django_tables2/semantic.html'
        #template_name = 'django_tables2/bootstrap4.html'
        #template_name = 'django_tables2/bootstrap.html'
        template_name = 'django_tables2/bootstrap-responsive.html'
        #attrs = {'class': 'mytable'} #table level
        attrs = {'tf':{'bgcolor':'#abdfcc'}, 'th':{'bgcolor':'#abdfcc'}} #table level
        row_attrs = {
            'data-id': lambda record: record.pk
        } #td element in tr
    
    def __init__(self, *args, **kwargs):
        super(BiblioTable, self).__init__(*args, **kwargs)
        self.counter = itertools.count() #returns a iterator object
    
    def render_row_number(self):
        return 'Row %s' % str(next(self.counter) + 1)

    def value_copies(self, record):
        item_count = Items.objects.filter(biblionumber_id=record.biblionumber).count()
        return str(item_count)

