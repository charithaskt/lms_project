from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from opac.forms import RenewBookForm, StartCollectFineForm
from django.urls import reverse
from django.db import IntegrityError
import json
import re
from datetime import tzinfo, timedelta, datetime
from datetime import date
from django.utils import timezone
import pytz
today = date.today()

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

utc = UTC()

# Create your views here.
#from ils_app.models import Biblio, Authors, Items, Genre, Publisher, Language, Reserves 
from intranet.models import Biblio, Authors, Items, Genre, Publisher, Language, Reserves 
from intranet.models import IssuingRules, Borrowers, Statistics, Issues, Quotations, EntryExitLogs
from intranet.models import Categories, Departments, Designations
from intranet.models import AccountLines, AccountOffsets, ActionLogs,PatronPhotos
from photos.models import PatronBulkPhotos

import random
def home(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books_titles = Biblio.objects.filter(itemtype__iexact='BK').count()
    num_books_volumes = Items.objects.filter(biblionumber__itemtype__iexact='BK').count()
    num_ref_books = Biblio.objects.filter(itemtype__iexact='RB').count()
    num_theses = Biblio.objects.filter(itemtype__iexact='TD').count()
    num_proj = Biblio.objects.filter(itemtype__iexact='PR').count()
    num_other = Biblio.objects.filter(itemtype__iexact='XM').count()
    # Available books (itemstatus = 'AV')
    num_books_available = Items.objects.filter(biblionumber__itemtype__iexact='BK').filter(itemstatus__iexact='AV').count()
    # The 'all()' is implied by default.    
    num_authors = Authors.objects.count()
    num_genres = Genre.objects.count()
    num_publishers = Publisher.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    quotes_count = Quotations.objects.all().count()
    query = "select * from intranet_quotations limit {},{}".format(random.randint(0,quotes_count-1),1)
    quotation = Quotations.objects.raw(query)
    context = {
        'num_books_titles': num_books_titles,
        'num_books_volumes': num_books_volumes,
        'num_ref_books': num_ref_books,
        'num_authors': num_authors,
        'num_publishers': num_publishers,
        'num_genres' : num_genres,
        'num_books_available' : num_books_available,
        'num_visits' : num_visits,
        'quote' : quotation[0],
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'opac/home.html', context=context)

from django.views import generic

class AuthorListView(generic.ListView):
    model = Authors
    template_name = 'opac/authors_list.html'
    def get_queryset(self):
        #return Author.objects.filter(lastname__icontains='someword')[:5]
        return Authors.objects.all()
    paginate_by = 3
#to display subsequent pages localhost:8000/catalog/authors/?page=[1..n]   

class AuthorDetailView(generic.DetailView):
    #model = get_user_model()
    model = Authors
    slug_field = "id" 
    template_name = "opac/authors_detail.html"

    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(AuthorDetailView, self).get_context_data(**kwargs)
        context['biblios'] = Biblio.objects.filter(authors=self.get_object())
        return context

class BookListView(generic.ListView):
    model = Biblio
    template_name = 'opac/books_list.html'
    def get_queryset(self):
        #return Book.objects.filter(title__icontains='wind')[:5] # Get 5 books containing the title wind
        return Biblio.objects.filter(itemtype__in=['BK','RB'])
    paginate_by = 3

#to display subsequent pages localhost:8000/catalog/books/?page=[1..n]   
'''copyrightdate <= 2017
class BookDetailView(generic.DetailView):
    model = Biblio
    template_name = 'opac/book_detail.html'

'''

def book_detail_view(request, pk):
    book = get_object_or_404(Biblio, pk=pk)
    return render(request, 'opac/book_detail.html', context={'book': book,
        'nfl_status':['DM','LO','LP','MI','WD','BD']})

class QuotesListView(generic.ListView):
    model = Quotations
    template_name = 'opac/quotes_list.html'
    def get_queryset(self):
        #return Quotations.objects.filter(text__icontains='someword')[:5]
        return Quotations.objects.all()
    paginate_by = 25

class QuoteDetailView(generic.DetailView):
    model = Quotations
    slug_field = "id" 
    template_name = "opac/quotes_detail.html"

    def get_context_data(self, **kwargs):
        context = super(QuoteDetailView, self).get_context_data(**kwargs)
        return context

class EntryExitLogsListView(generic.ListView):
    model = EntryExitLogs
    template_name = 'opac/entryexitlogs_list.html'
    def get_queryset(self):
        return EntryExitLogs.objects.filter(timeofentry__contains=today)
    paginate_by = 10

class EntryExitLogDetailView(generic.DetailView):
    model = EntryExitLogs
    slug_field = "id" 
    template_name = "opac/entryexitlog_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EntryExitLogDetailView, self).get_context_data(**kwargs)
        return context

#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
class LoanedBooksByUserListView(PermissionRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    permission_required = 'accounts.can_borrow'
    model = Issues
    template_name ='opac/issues_list_borrowedby_user.html'
    paginate_by = 2

    def get_issuing_rule(self):
        borrower = Borrowers.objects.get(borrower=self.request.user.profile)
        if borrower:
           category = borrower.category
           try:
              policy = IssuingRules.objects.get(categorycode=category,itemtype='BK')
              if policy:
                 return policy
           except:
              pass
        return None
    
    def get_context_data(self, **kwargs):
        # xxx will be available in the template as the related objects
        context = super(LoanedBooksByUserListView, self).get_context_data(**kwargs)
        policy = self.get_issuing_rule()
        if policy is None:
           context['renewalsallowed'] = 0
           context['issuelength'] = 0
        else:
           context['renewalsallowed'] = policy.renewalsallowed
           context['issuelength'] = policy.issuelength
        return context

    def get_queryset(self):
        return Issues.objects.filter(borrower__borrower=self.request.user.profile).filter(returned=False).order_by('date_due')

class IssuedBooksListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'accounts.can_circulate_place_holds'
    # Or multiple permissions
    #permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!

    model = Issues
    template_name ='opac/books_issued_to_users.html'
    paginate_by = 10
    #ordering = ['borrowernumber']

    def get_queryset(self):
        return Issues.objects.filter(returned=False).order_by('date_due','borrower__cardnumber')

from django.db import transaction
from django.contrib.auth.mixins import PermissionRequiredMixin
def renew_book_self(request,pk):
    permission_required = 'accounts.can_borrow'
    issue_instance = get_object_or_404(Issues, pk=pk)
    loggedin_borrower = Borrowers.objects.get(borrower=request.user.profile)
    issued_borrower = issue_instance.borrower
    def get_issuing_rule():
        if issued_borrower and (loggedin_borrower==issued_borrower):
           category = issued_borrower.category
           try:
              policy = IssuingRules.objects.get(categorycode=category,itemtype='BK')
              if policy:
                 return policy
           except:
              pass
        return None
    
    policy = get_issuing_rule()
    if not policy is None: 
        renewalsallowed = policy.renewalsallowed
        issuelength = policy.issuelength
        if renewalsallowed > issue_instance.renewals:
           issue_instance.date_due = issue_instance.date_due + timedelta(days=issuelength)
           issue_instance.renewals = issue_instance.renewals + 1
           item = issue_instance.item
           biblio = item.biblionumber
           if item.totalissues:
              item.totalissues = item.totalissues + 1 
           else:
              item.totalissues = 1 
           biblio.totalissues = biblio.totalissues + 1
           try:
               with transaction.atomic():
                   issue_instance.save()
                   item.save()
                   biblio.save()
                   stats=Statistics.objects.create(borrower=issue_instance.borrower, item=issue_instance.item, 
                       usercardnumber = issue_instance.borrower.cardnumber, typecode="RENEW", value=0)
                   al = ActionLogs.objects.create(usercode=loggedin_borrower,module='CIRCULATION',action='RENEWSELF')
           except IntegrityError:
              return HttpResponse({"message":"Database integrity error has occured"})
    return HttpResponseRedirect(reverse('my-borrowed'))




#@permission_required('accounts.can_self_renew')
def renew_book_librarian(request, pk, loanlength):
    issue_instance = get_object_or_404(Issues, pk=pk)
    permission_required = 'accounts.can_circulate_place_holds'
    # If this is a POST request then process the Form data
        
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if book_renewal_form.is_valid():
            item = issue_instance.item
            biblio = item.biblionumber
            if item.totalissues:
               item.totalissues = item.totalissues + 1 
            else:
               item.totalissues = 1 
            biblio.totalissues = biblio.totalissues + 1
            try:
               loggedin_user = Borrowers.objects.get(borrower=request.user.profile)
               # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
               try:
                  with transaction.atomic():
                      issue_instance.date_due = book_renewal_form.cleaned_data['renewal_date']
                      issue_instance.renewals = issue_instance.renewals + 1
                      issue_instance.save()
                      item.save()
                      biblio.save()
                      stats=Statistics.objects.create(borrower=issue_instance.borrower, item=issue_instance.item, 
                         usercardnumber = loggedin_user.cardnumber, typecode="RENEW", value=0) 
                      al = ActionLogs.objects.create(usercode=loggedin_user,module='CIRCULATION',action='RENEW')    
               except IntegrityError:
                  print("Database integrity error has occured")
                  return HttpResponse("Database integrity error has occured")
            except:
               return HttpResponse("The loggedin user is not library borrower")
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('renew-book-librarian-init') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = issue_instance.date_due + datetime.timedelta(days=int(loanlength))
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': book_renewal_form,
        'book_instance': issue_instance,
    }
    return render(request, 'intranet/book_renew_librarian.html', context)


from opac.forms import StartRenewBookForm
def get_issuing_rule(issue_instance):
    issued_borrower = issue_instance.borrower
    if issued_borrower:
       category = issued_borrower.category
       try:
          policy = IssuingRules.objects.get(categorycode=category,itemtype='BK')
          if policy:
             return policy
       except:
          pass
    return None

#@permission_required('accounts.can_self_renew')
def renew_book_librarian_init(request):
    permission_required = 'accounts.can_circulate_place_holds'
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_renewal_form = StartRenewBookForm(request.POST)
        message = ""
        # Check if the form is valid:
        if book_renewal_form.is_valid():
            barcode = book_renewal_form.cleaned_data['barcode']
            barcode = barcode.strip(" ")
            try:
               item = Items.objects.get(barcode=barcode)
               if item:
                   try:
                      issue_instance = Issues.objects.get(item=item,returned=False)
                      if issue_instance:
                         policy = get_issuing_rule(issue_instance)
                         if not policy is None: 
                            renewalsallowed = policy.renewalsallowed
                            issuelength = policy.issuelength
                            if renewalsallowed > issue_instance.renewals:
                               return HttpResponseRedirect(reverse('renew-book-librarian', args=(issue_instance.pk,issuelength,)))
                            else:
                               message = "Can't exceeded your renewal limit of : {}".format(renewalsallowed)
                         else:
                            message = "No issuing rule for your category for the itemtype 'BK'"
                   except:
                     message = "No issue record matching the barcode '{}' exists".format(barcode)
            except:
               message = "No item record exists with that barcode : '{}'".format(barcode)
    # If this is a GET (or any other method) create the default form.
    else:
        book_renewal_form = StartRenewBookForm()
        message = ""           
    context = {
        'form': book_renewal_form,
        'message' : message
    }

    return render(request, 'intranet/book_renew_librarian_init.html', context)


from datetime import datetime, timedelta
from collections import Counter
def dates_between(start, end):
    while start <= end:
        yield start
        start += timedelta(1)

def count_weekday(start, end):
    counter = Counter()
    for date in dates_between(start, end):
        counter[date.strftime('%a')] += 1
    return counter

def count_weekendhdays(start, end, hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%a') in  [hday.strftime('%a') for hday in hdays]:
              counter += 1
    return counter

def count_yrlyhdays(start,end, hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%m%d') in  [hday.strftime('%m%d') for hday in hdays]:
              counter += 1
    return counter

def count_adhochdays(start,end,hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%Y%m%d') in  [hday.strftime('%Y%m%d') for hday in hdays]:
              counter += 1
    return counter

def get_holidays():
    yearly=[]
    weekend=[]
    adhoc=[]
    hqs = Holidays.objects.all()
    if hqs:
       i=0
       while i<hqs.count():
          if hqs[i].isexception:
             if hqs[i].holiday_type=='WEEKEND':
                weekend.append(hqs[i].date)
             elif hqs[i].holiday_type=='YEARLY':
                yearly.append(hqs[i].date)
             elif hqs[i].holiday_type=='ADHOC':
                adhoc.append(hqs[i].date)
          i+=1
    return {'yearly':yearly, 'adhoc':adhoc, 'weekend':weekend}

def return_book_librarian(request, pk, fineamount, overdue):
    issue_instance = get_object_or_404(Issues, pk=pk)
    permission_required = 'accounts.can_circulate_place_holds'
    # If this is a POST request then process the Form data
        
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        item = issue_instance.item
        biblio = item.biblionumber
        loggedin_user = Borrowers.objects.get(borrower=request.user.profile)
        try:
            with transaction.atomic():
                issue_instance.returned = True
                issue_instance.returndate = datetime.now(tz=timezone.utc)
                issue_instance.save()
                stats=Statistics.objects.create(borrower=issue_instance.borrower, item=issue_instance.item, 
                    usercardnumber = loggedin_user.cardnumber, typecode="RETURN", value=0)                   
                fineamount = int(fineamount)
                if fineamount>0:
                    al = AccountLines.objects.create(borrower=issue_instance.borrower, itemnumber = issue_instance.item,
                         amount=fineamount, description="Overdue fine",accountype="FU", manager_id=loggedin_user.pk)
                    ac = AccountOffsets.objects.get(borrower=issue_instance.borrower)
                    if ac:
                         ac.amountoutsanding = ac.amountoutsanding + fineamount 
                         ac.save()
                    else:
                         ac = AccountOffsets.objects.create(borrower=issue_instance.borrower, amountoutstanding = fineamount)
                al = ActionLogs.objects.create(usercode=loggedin_user,module='CIRCULATION',action='RETURN')
        except IntegrityError:
           print("Database integrity error has occured")
           return HttpResponse("Database integrity error has occured")
        else:
           # redirect to a new URL:
           return HttpResponseRedirect(reverse('return-book-librarian-init') )

    context = {
        'book_instance': issue_instance,
        'fineamount' : fineamount,
        'is_fine'    : True if int(fineamount)>0 else False,
        'is_overdue' : True if int(overdue)>0 else False,
 
    }
    return render(request, 'intranet/book_return_librarian.html', context)

from opac.forms import StartReturnBookForm

def return_book_librarian_init(request):
    permission_required = 'accounts.can_circulate_place_holds'
    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        book_return_form = StartReturnBookForm(request.POST)
        message = ""
        # Check if the form is valid:
        if book_return_form.is_valid():
          barcode = book_return_form.cleaned_data['barcode']
          barcode = barcode.strip(" ")
          try:
            item = Items.objects.get(barcode=barcode)
            if item:
              try:
                issue_instance = Issues.objects.get(item=item,returned=False)
                if issue_instance:
                   fineamount = 0
                   today = datetime.now(utc)
                   date_due = issue_instance.date_due
                   overdue = (today - date_due).days
                   print('overdue days: ',overdue)
                   if overdue>0:
                       policy = get_issuing_rule(issue_instance)
                       if not policy is None:
                          overduefinescap = policy.overduefinescap
                          fine =  policy.fine
                          finedays = policy.finedays
                          chargeperiod = policy.chargeperiod
                          if fine and fine>0:
                              hdays=get_holidays()
                              weekend_holidays = count_weekendhdays(date_due,today,hdays['weekend'])
                              yearly_holidays = count_yrlyhdays(date_due,today,hdays['yearly'])
                              adhoc_holidays = count_adhochdays(date_due,today,hdays['adhoc'])
                              total_holidays = yearly_holidays + weekend_holidays + adhoc_holidays
                              overdue_ = (datetime.now(utc) - issue_instance.date_due).days + finedays - total_holidays
                              if overdue_ > 0:
                                 fineamount = (overdue_//chargeperiod)*fine 
                                 fineamount = fineamount if fine<=overduefinescap else overduefinescap
              
                   return HttpResponseRedirect(reverse('return-book-librarian', args=(issue_instance.pk,fineamount,overdue)))
              except:
                   message = "Book with that barcode {} is not in circulation".format(barcode)
          except:
              message = "No item record exists with that barcode : {}".format(barcode)
    # If this is a GET (or any other method) create the default form.
    else:
        book_return_form = StartReturnBookForm()
        message = ""           
    context = {

        'form': book_return_form,
        'message' : message
    }

    return render(request, 'intranet/book_return_librarian_init.html', context)


from django.http import JsonResponse
from django.views.generic.edit import CreateView
#from intranet.models import Authors
from ils_app.models import Authors 
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        raise ValidationError(_('Duplicate author - That author record already exists'))
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        lastname = str(form['lastname'])
        firstname = str(form['firstname'])
        lastname = re.search(r'value="([^"]+)"',lastname).group(1)
        firstname = re.search(r'value="([^"]+)"',firstname).group(1)
        firstname = firstname.strip()
        lastname = lastname.strip()
        print(lastname)
        print(firstname)
        authors = ""
        try:
           authors = Authors.objects.get(lastname__iexact=lastname, firstname__iexact=firstname)
        except:
           pass
        if authors:
            raise ValidationError(_('Duplicate Author: Author "{} {}" already exists'.format(lastname, firstname)))
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data, status=201)
        else:
            return response

class AuthorCreate(AjaxableResponseMixin, CreateView):
    model = Authors
    fields = ['firstname','lastname']
    template_name = 'intranet/authors_form.html'
    def form_invalid(self, form):
     
        return super().form_valid(form)

from django.shortcuts import render_to_response
from django.views.decorators.http import require_GET

from djangoql.exceptions import DjangoQLError
from djangoql.queryset import apply_search
from djangoql.schema import DjangoQLSchema

class AjaxableQuoteResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        raise ValidationError(_('Duplicate quotation - That quote already exists'))
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        source = str(form['source'])
        text = str(form['text'])
        source = re.search(r'value="([^"]+)"',source).group(1)
        text = re.search(r'value="([^"]+)"',text).group(1)
        source = source.strip()
        text = text.strip()
        quotes = Quotations.objects.filter(text__iexact=text, source__iexact=source).first()
        if quotes:
            raise ValidationError(_('Duplicate Quote: Quotation "{} - {}" already exists'.format(text, source)))
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }            
            return JsonResponse(data, status=201)
        else:
            return response

class QuoteCreate(AjaxableQuoteResponseMixin, CreateView):
    model = Quotations
    fields = ['text','source']
    template_name = 'intranet/quotes_form.html'
    def form_invalid(self, form):
        return super().form_valid(form)

class BiblioQLSchema(DjangoQLSchema):
    include = (Biblio,Authors,Publisher,Genre,Language)

@require_GET
def catalog_search(request):
    q = request.GET.get('q', '')
    error = ''
    query = Biblio.objects.all().order_by('title')
    if q:
        try:
            query = apply_search(query, q, schema=BiblioQLSchema)
        except DjangoQLError as e:
            query = query.none()
            error = str(e)
    return render_to_response('opac/search/catalog_search.html', {
        'q': q,
        'error': error,
        'search_results': query,
        'introspections': json.dumps(BiblioQLSchema(query.model).as_dict()),
    })

def issue_item_librarian(request, borrower_pk,item_pk, held_self, renewal,loan_length):
    item = get_object_or_404(Items, pk=item_pk)
    borrower = get_object_or_404(Borrowers, pk=borrower_pk)
    permission_required = 'accounts.can_circulate_place_holds'
    loggedin_user = Borrowers.objects.get(borrower=request.user.profile)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        try:
            with transaction.atomic():
                typecode="ISSUE"
                if renewal==True:
                  typecode="RENEW"
                  issue_record = Issues.objects.filter(borrower=borrower, item=item, returned=False).first()
                  if issue_record:
                     issue_record.renewals+=1
                     issue_record.save()
                else:
                  issue = Issues.objects.create(borrower=borrower,item=item,issuedate=datetime.now(utc), date_due=datetime.now(utc)+
                      timedelta(days=int(loan_length)))  
                  if held_self==True:
                     hold_record = Reserves.objects.filter(borrower=borrower, item=item, found=False,priority=0).first()
                     hold_record.priority=-1 #reserve filled                    
                     hold_record.save()
                if item.totalissues and item.totalissues>=0:
                   item.totalissues+=1
                else:
                   item.totalissues=1
                item.itemstatus='OL' #on loan
                item.save()
                biblio = item.biblionumber
                if biblio.totalissues and biblio.totalissues>=0:
                   biblio.totalissues+=1
                else:
                   biblio.totalissues=1
                biblio.save()     
                stats=Statistics.objects.create(borrower=borrower, item=item, 
                    usercardnumber = loggedin_user.cardnumber, typecode=typecode, value=0)   
                al = ActionLogs.objects.create(usercode=loggedin_user,module='CIRCULATION',action=typecode)
        except IntegrityError:
           return HttpResponse("Database integrity error has occured")
        else:
           # redirect to a new URL:
           message = "Successfully issued {} to {}".format(item.barcode,borrower.cardnumber)
           print(message)
           return HttpResponseRedirect(reverse('issue-item-librarian-init'))
          
    date_due= (datetime.now(utc) + timedelta(days=int(loan_length))).strftime("%d-%m-%Y")

    context = {
        'borrower_instance': borrower,
        'item_instance': item,
        'renewal' : True if renewal=="True" else False,
        'held_self' : True if held_self=="True" else False,
        'date_due': date_due,
    }
    return render(request, 'intranet/item_issue_librarian.html', context)

from opac.forms import StartIssueItemForm

def issue_item_librarian_init(request):
    permission_required = 'accounts.can_circulate_place_holds'
    if request.method == 'POST':
        item_issue_form = StartIssueItemForm(request.POST)
        message = ""
        # Check if the form is valid:
        if item_issue_form.is_valid():
          can_issue = False
          held_self = False
          renewal = False
          barcode = item_issue_form.cleaned_data['barcode']
          cardnumber = item_issue_form.cleaned_data['cardnumber']
          barcode = barcode.strip(" ")
          cardnumber = cardnumber.strip(" ")
          item = Items.objects.filter(barcode__iexact=barcode).first()
          borrower = Borrowers.objects.filter(cardnumber__iexact=cardnumber,gonenoaddress=False, lost=False, debarred=None).first()
          if not borrower:
              message = "Invalid card, either reported lost or patron is inactive"
          else:
             if item and (item.itemstatus in ["AV","OL"] and not item.notforloan):
                policy = IssuingRules.objects.filter(itemtype=item.biblionumber.itemtype, categorycode=borrower.category).first()
                #check if the item is on loan
                issue_record = Issues.objects.filter(item=item, returned=False).first()
                if issue_record:
                   date_issued = issue_record.issuedate.strftime("%d-%m-%Y")
                   curr_date = datetime.now(utc).strftime("%d-%m-%Y")
                   if issue_record.borrower == borrower and date_issued != curr_date:
                      #this is renewal - verify renewal limit
                      allowed_renewals=policy.renewalsallowed
                      already_renewed = issue_record.renewals
                      if already_renewed >= allowed_renewals:
                         message = "You have exceeded your renewal limit for this item type. Can't Issue."
                      else:
                         # verify reserved?
                         renewal = True
                         held_item = Reserves.objects.filter(item=item, priority=0,borrowernumber=borrower).first()
                         if held_item:
                            held_self = True
                            loan_limit = policy.issuelength
                            already_issued = Issues.objects.filter(borrower=borrower, returned=False, 
                               item__biblionumber__itemtype=item.biblionumber.itemtype).count()
                            if already_issued >= loan_limit:
                               message = "You have exceeded your loan limit for this item type."
                            else:
                               can_issue=True
                   elif issue_record.borrower == borrower:
                       message = "You have already borrowed this item."                 
                   else:
                       message = "This item is in circulation."                 
                else:
                   #No body already issued this item
                   if policy:
                      loan_limit = policy.issuelength
                   else:
                      loan_limit=0
                   already_issued = Issues.objects.filter(borrower=borrower, returned=False, 
                      item__biblionumber__itemtype=item.biblionumber.itemtype).count()
                   if already_issued >= loan_limit:
                      message = "You have exceeded your loan limit for this item type."
                   else:
                      can_issue=True
             else:
                NFL="For Loan"
                if item.notforloan and item.notforloan=='1':
                     NFL = "Not For Loan"
                if item.notforloan and item.notforloan=='2':
                     NFL="Staff Copy"
                message = "Item not for loan:- item status : {} / {}".format(item.itemstatus,NFL)         

             if can_issue==True:
                return HttpResponseRedirect(reverse('issue-item-librarian', args=(borrower.pk,item.pk,held_self, renewal, policy.issuelength)))      
          
    # If this is a GET (or any other method) create the default form.
    else:
        item_issue_form = StartIssueItemForm()
        message=""
    context = {
        'form': item_issue_form,
        'message' : message
    }

    return render(request, 'intranet/item_issue_librarian_init.html', context)


class AjaxableQuoteResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        raise ValidationError(_('Duplicate quotation - That quote already exists'))
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).

        source = str(form['source'])
        text = str(form['text'])
        source = re.search(r'value="([^"]+)"',source).group(1)
        text = re.search(r'value="([^"]+)"',text).group(1)
        source = source.strip()
        text = text.strip()
        quotes = Quotations.objects.filter(text__iexact=text, source__iexact=source).first()
        if quotes:
            raise ValidationError(_('Duplicate Quote: Quotation "{} - {}" already exists'.format(text, source)))
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }            
            return JsonResponse(data, status=201)
        else:
            return response


def days_hours_minutes_seconds(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "%02d days %02dh:%02dm:%02ds"%(days, hours, minutes, seconds)

def hours_minutes_seconds(td):
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "%02d:%02d:%02d"%(hours, minutes, seconds)


class AjaxableVisitorsResponseMixin:
    def get(self, request):
       q = request.GET.get('q', '')
       error = ''
       query = EntryExitLogs.objects.filter(timeofentry__contains=today).order_by('-id')
       if q:
          try:
            query = apply_search(query, q, schema=EntryExitLogsQLSchema)
          except DjangoQLError as e:
            query = query.none()
            error = str(e)
       return render_to_response('opac/search/entryexitlogs_search.html', {
          'q': q,
          'error': error,
          'search_results': query,
          'introspections': json.dumps(EntryExitLogsQLSchema(query.model).as_dict()),
       })

    def form_invalid(self, form):
        raise ValidationError(_('Duplicate entry - That user already logged-in'))
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        cardnumber = str(form['cardnumber'])
        cardnumber = re.search(r'value="([^"]+)"',cardnumber).group(1)
        cardnumber = cardnumber.strip()
        pk=None
        
        current_borrower = Borrowers.objects.filter(cardnumber__iexact=cardnumber).first()
        already_visited = EntryExitLogs.objects.filter(cardnumber__iexact=cardnumber, 
           timeofexit=None, timeofentry__contains=today).first()
        if already_visited:
           already_visited.timeofexit=timezone.now()
           entry_time = timedelta(hours=already_visited.timeofentry.hour,minutes=already_visited.timeofentry.minute,seconds=already_visited.timeofentry.second)
           exit_time = timedelta(hours=already_visited.timeofexit.hour,minutes=already_visited.timeofexit.minute,seconds=already_visited.timeofexit.second)
           already_visited.timespent = hours_minutes_seconds(exit_time-entry_time)

           already_visited.save()    
           pk=already_visited.pk       
        else:
           response = super().form_valid(form)
           current_visitor = EntryExitLogs.objects.filter(cardnumber__iexact=cardnumber, 
                  timeofentry=None).first()
           if current_visitor:
              if current_borrower:
                 current_visitor.borrower=current_borrower
                 has_photo = PatronPhotos.objects.filter(patron_id=current_visitor.borrower.id).first()
                 has_bulkphoto = PatronBulkPhotos.objects.filter(patron_id=current_visitor.borrower.id).first()
                 if has_photo:
                       current_visitor.imageurl=has_photo.imageurl
                 elif has_bulkphoto:
                       current_visitor.imageurl=has_bulkphoto.file
              current_visitor.timeofentry=timezone.now()           
              current_visitor.save()
              pk=current_visitor.pk
        
        query = EntryExitLogs.objects.filter(timeofentry__contains=today).order_by('-id')
        return render_to_response('opac/search/entryexitlogs_search.html', {
          'q': '',
          'error': '',
          'search_results': query,
          'introspections': json.dumps(EntryExitLogsQLSchema(query.model).as_dict()),
        })
        
        #return JsonResponse(data, status=201)
        #return HttpResponseRedirect(reverse('entryexitlog-detail', kwargs={'pk':pk,}))      

class EntryExitLogCreate(AjaxableVisitorsResponseMixin, CreateView):
    model = EntryExitLogs
    fields = ['cardnumber']
    template_name = 'opac/search/entryexitlogs_search.html'

    def form_invalid(self, form):
        return super().form_valid(form)
    """ 
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super(EntriExitLogCreate, self).dispatch(request, *args, **kwargs)
    """

from djangoql.schema import DjangoQLSchema, IntField, StrField

class EntryExitLogsQLSchema(DjangoQLSchema):
    include = (EntryExitLogs,Borrowers,Categories,Departments,Designations)
    

@require_GET
def entryexitlog_search(request):
    q = request.GET.get('q', '')
    error = ''
    query = EntryExitLogs.objects.filter(timeofentry__contains=today).order_by('-timeofentry')
    if q:
        try:
            query = apply_search(query, q, schema=EntryExitLogsQLSchema)
        except DjangoQLError as e:
            query = query.none()
            error = str(e)
    return render_to_response('opac/search/entryexitlogs_searchql.html', {
        'q': q,
        'error': error,
        'search_results': query,
        'introspections': json.dumps(EntryExitLogsQLSchema(query.model).as_dict()),
    })

def fine_collect_librarian(request, borrower_pk, account_pk,fine):
    borrower = get_object_or_404(Borrowers, pk=borrower_pk)
    account = get_object_or_404(AccountOffsets, pk=account_pk)
    permission_required = 'accounts.can_circulate_place_holds'
    loggedin_user = Borrowers.objects.get(borrower=request.user.profile)
    fine = int(fine)
    message = ""
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        try:
            with transaction.atomic():
                typecode="PAYMENT"
                action_type = "FINE"
                account_type = "PAY"
                module="FINES"
                amount_outstanding = account.amountoutstanding
                if fine<=amount_outstanding:
                   account.amountoutstanding-=fine
                   account.save()
                   acclines = AccountLines.objects.create(borrower=borrower,amount=-fine,description="Fine payment",
                        accounttype=account_type,manager_id=loggedin_user)
                   stats=Statistics.objects.create(borrower=borrower, 
                       usercardnumber = loggedin_user.cardnumber, typecode=typecode, value=fine)   
                   al = ActionLogs.objects.create(usercode=loggedin_user,module=module,action=action_type)
        except IntegrityError:
           return HttpResponse("Database integrity error has occured")
        else:
           # redirect to a new URL:
           message = "Successfully collected fine {} from  {}".format(fine,borrower.cardnumber)
           print(message)
           return HttpResponseRedirect(reverse('fine-collection-librarian-init'))
    context = {
        'borrower': borrower,
        'fine' : fine,
        'outstanding' : account.outstanding,        
        'message': message,
    }
    return render(request, 'intranet/fine_collection_librarian.html', context)


def fine_collect_librarian_init(request):
    permission_required = 'accounts.can_circulate_place_holds'
    message=""
    if request.method == 'POST':
        fine_collection_form = StartCollectFineForm(request.POST)
        
        # Check if the form is valid:
        if fine_collection_form.is_valid():
          cardnumber = fine_collection_form.cleaned_data['cardnumber']
          fine = fine_collection_form.cleaned_data['fine']
          print(fine)
          print(cardnumber)
          cardnumber = cardnumber.strip(" ")
          borrower = Borrowers.objects.filter(cardnumber__iexact=cardnumber).first()
          outstanding = 0
          account = AccountOffsets.objects.filter(borrower=borrower).first()
          if account:
             outstanding = account.amountoutstanding
          if not borrower:
              message = "Invalid card, either reported lost or patron is inactive"
          elif not account:
              message = "There seems to be no fine. No account record"
          elif not (fine>0 and fine<=outstanding):
              message = "Fine amount can't excced the amount outstanding."
          #else:
          #return HttpResponseRedirect(reverse('fine-collect-librarian', args=(borrower.pk,account.pk,fine)))      
          
    # If this is a GET (or any other method) create the default form.
    fine_collect_form = StartCollectFineForm()
    context = {
        'form': fine_collect_form,
        'message' : message,
    }

    return render(request, 'intranet/fine_collect_librarian_init.html', context)

def pay_fine(request):
    #user = request.POST['USER]
    fine_amount = request.POST['FINEAMOUNT']
    cust_ID = request.POST['CUST_ID']

    context = {
        #'USER': user,
        'FINEAMOUNT': fine_amount,
        'CUST_ID': cust_ID
    }

    return render(request,'payment:pay' ,context)
