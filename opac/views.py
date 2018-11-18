from datetime import datetime, timedelta
from collections import Counter

from django.shortcuts import get_object_or_404

from intranet.models import Holidays, Borrowers
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import IntegrityError
import json
import re
from datetime import tzinfo, timedelta, datetime

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
        if date.strftime('%a') in [hday.strftime('%a') for hday in hdays]:
            counter += 1
    return counter


def count_yrlyhdays(start, end, hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%m%d') in [hday.strftime('%m%d') for hday in hdays]:
            counter += 1
    return counter


def count_adhochdays(start, end, hdays):
    counter = 0
    for date in dates_between(start, end):
        if date.strftime('%Y%m%d') in [hday.strftime('%Y%m%d') for hday in hdays]:
            counter += 1
    return counter


def get_holidays():
    yearly = []
    weekend = []
    adhoc = []
    hqs = Holidays.objects.all()
    if hqs:
        i = 0
        while i < hqs.count():
            if hqs[i].isexception:
                if hqs[i].holiday_type == 'WEEKEND':
                    weekend.append(hqs[i].date)
                elif hqs[i].holiday_type == 'YEARLY':
                    yearly.append(hqs[i].date)
                elif hqs[i].holiday_type == 'ADHOC':
                    adhoc.append(hqs[i].date)
            i += 1
    return {'yearly': yearly, 'adhoc': adhoc, 'weekend': weekend}






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
