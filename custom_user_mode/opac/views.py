from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
import json
import re
from datetime import tzinfo, timedelta, datetime

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
from intranet.models import Biblio, Authors, Items, Genre, Publisher, Issues, IssuingRules, Borrowers, Statistics
from intranet.models import AccountLines, AccountOffsets, ActionLogs
def index(request):
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
    context = {
        'num_books_titles': num_books_titles,
        'num_books_volumes': num_books_volumes,
        'num_ref_books': num_ref_books,
        'num_authors': num_authors,
        'num_publishers': num_publishers,
        'num_genres' : num_genres,
        'num_books_available' : num_books_available,
        'num_visits' : num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'opac/index.html', context=context)

from django.views import generic

class AuthorListView(generic.ListView):
    model = Authors
    template_name = 'opac/authors_list.html'
    def get_queryset(self):
        #return Author.objects.filter(lastname__icontains='someword')[:5]
        return Authors.objects.all()
    paginate_by = 2
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
    paginate_by = 1
#to display subsequent pages localhost:8000/catalog/books/?page=[1..n]   
'''
class BookDetailView(generic.DetailView):
    model = Biblio
    template_name = 'opac/book_detail.html'

'''

def book_detail_view(request, pk):
    book = get_object_or_404(Biblio, pk=pk)
    return render(request, 'opac/book_detail.html', context={'book': book,
        'nfl_status':['DM','LO','LP','MI','WD','BD']})

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

from django.db import transaction
from django.contrib.auth.mixins import PermissionRequiredMixin
def renew_book_self(request,pk):
    permission_required = 'accounts.can_borrow'
    issue_instance = get_object_or_404(Issues, pk=pk)
    def get_issuing_rule():
        loggedin_borrower = Borrowers.objects.get(borrower=request.user.profile)
        issued_borrower = issue_instance.borrower
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
                   al = ActionLogs.objects.create(usercode=loggedin_user,module='CIRCULATION',action='RENEWSELF')
           except IntegrityError:
              return HttpResponse({"message":"Database integrity error has occured"})
    return HttpResponseRedirect(reverse('my-borrowed'))


from opac.forms import RenewBookForm

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
                issue_instance.returndate = datetime.now()
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


'''
class Authors(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    def __str__(self):
        return "{}, {}".format(self.firstname, self.lastname)
    def get_absolute_url(self):
        return reverse('authors-detail', args=[self.id])

'''
from django.http import JsonResponse
from django.views.generic.edit import CreateView
from intranet.models import Authors
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

    def form_invalid(self, form):
        
        return super().form_valid(form)
