import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from intranet.models import Borrowers, Items
from intranet.models import Issues, IssuingRules, Items, AccountOffsets
class IssueBookForm(forms.Form):
    cardnumber = forms.CharField(max_length=10,help_text="Enter borrower cardnumber")
    barcode    = forms.CharField(max_length=7,help_text="Enter the item barcode")
    #due_date = forms.DateField(help_text="Enter due date")
    
    def clean_cardnumber(self):
        data = self.cleaned_data['cardnumber']
        try:
          borrower = Borrowers.objects.get(cardnumber=data)
          # Check if a date is not in the past. 
          if borrower is None:
            raise ValidationError(_('Invalid borrower - no borrower with cardnumber "{}" exists'.format(data)))
        except:
          raise ValidationError(_('Invalid borrower - no borrower with thcardnumber "{}" exists'.format(data)))
        return data

    def clean_barcode(self):
        data = self.cleaned_data['barcode']
        try:
           item = Items.objects.get(barcode=data)
           # Check if a date is not in the past. 
           if item is None:
              raise ValidationError(_('Invalid barcode - no book with barcode "{}" exists'.format(data)))
        except:
           raise ValidationError(_('Invalid barcode - no itemr with barcode "{}" exists'.format(data)))
           
        return data


class StartRenewBookForm(forms.Form):
    barcode = forms.CharField(max_length=7,help_text="Enter the item barcode")
    #loanlength = forms.IntegerField()  #{{ form.field.as_hidden }}
    #forms.CharField(widget = forms.HiddenInput(), required = False)
    def get_issuing_rule(self,issue_instance):
        issued_borrower = issue_instance.borrower
        if (issued_borrower):
           category = issued_borrower.category
           try:
              policy = IssuingRules.objects.get(categorycode=category,itemtype='BK')
              if policy:
                 return policy
           except:
              raise ValidationError(_('No Issuing Rule exists for the user with category "{}"'.format(category)))
               
        return None
   
    def clean_barcode(self):
        data = self.cleaned_data['barcode']
        try:
           item = Items.objects.get(barcode=data)
           # Check if a date is not in the past. 
           if item is None:
              raise ValidationError(_('Invalid barcode - no book with barcode "{}" exists'.format(data)))
           else:
              iqs = Issues.objects.filter(item=item).filter(returned=False) 
              if iqs is None:
                 raise ValidationError(_('Not in circulation - no issue record  with barcode "{}" exists'.format(data)))
              else:
                 issue_instance = iqs[0]
                 policy = self.get_issuing_rule(issue_instance)
                 if not policy is None: 
                    renewalsallowed = policy.renewalsallowed
                    issuelength = policy.issuelength
                    if renewalsallowed <= issue_instance.renewals:
                       raise ValidationError(_('No more nenewals allowed.'))
                 else:
                    raise ValidationError(_('No issuing rule to permit renewal.'))
        except:
           raise ValidationError(_('Invalid barcode - no book with barcode "{}" exists'.format(data)))
        return data

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Accept or enter a date between now and 30 days")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        
        # Check if a date is not in the past. 
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        #if data > datetime.date.today() + datetime.timedelta(days=30):
        #    raise ValidationError(_('Invalid date - renewal more than 30 days'))

        # Remember to always return the cleaned data.
        return data

class StartReturnBookForm(forms.Form):
    barcode = forms.CharField(max_length=7,help_text="Enter the item barcode")
 
    def clean_barcode(self):
        data = self.cleaned_data['barcode']
        try:
           item = Items.objects.get(barcode=data)
           # Check if a date is not in the past. 
           if item is None:
              raise ValidationError(_('Invalid barcode - no book with barcode {} exists'.format(data)))
           else:
              iqs = Issues.objects.filter(item=item).filter(returned=False) 
              if iqs is None:
                raise ValidationError(_('Not in circulation - no issue record  with barcode {} exists'.format(data)))
        except:
              raise ValidationError(_("Invalid barcode - no book with barcode '{}' exists".format(data)))

        return data

class StartIssueItemForm(forms.Form):
    cardnumber = forms.CharField(label="Card Number    ",max_length=10,help_text="Enter borrower cardnumber")
    barcode    = forms.CharField(label="Item Barcode  ",max_length=7,help_text="Enter item barcode")
        
    def clean_cardnumber(self):
        data = self.cleaned_data['cardnumber']
        data = data.strip(" ")
        try:
          borrower = Borrowers.objects.get(cardnumber__iexact=data)
          # Check if a date is not in the past. 
          if borrower is None:
            raise ValidationError(_('Invalid borrower - no borrower with cardnumber "{}" exists'.format(data)))
        except:
          raise ValidationError(_('Invalid borrower - no borrower with cardnumber "{}" exists'.format(data)))
        return data

    def clean_barcode(self):
        data = self.cleaned_data['barcode']
        data.strip(" ")
        try:
           item = Items.objects.get(barcode__iexact=data)
           # Check if a date is not in the past. 
           if item is None:
              raise ValidationError(_('Invalid barcode - no item with barcode "{}" exists'.format(data)))
        except:
           raise ValidationError(_('Invalid barcode - no item with barcode "{}" exists'.format(data)))
           
        return data

class StartCollectFineForm(forms.Form):
    cardnumber = forms.CharField(label="Card Number",max_length=10, help_text="Enter borrower cardnumber")
    fine = forms.DecimalField(decimal_places=2,max_digits=7,label="Fine Amount")
    
    def clean_cardnumber(self):
        data = self.cleaned_data['cardnumber']
        data = data.strip(" ")
        try:
          borrower = Borrowers.objects.get(cardnumber__iexact=data)
          if not borrower:
            raise ValidationError(_('Invalid borrower - no borrower with cardnumber "{}" exists'.format(data)))
        except:
          raise ValidationError(_('Invalid borrower - no borrower with cardnumber "{}" exists'.format(data)))
        account = AccountOffsets.objects.filter(borrower=borrower).first()
        if not account:
            raise ValidationError(_('No Account Record Found with some outstanding fine amount.')) 
        elif account.amountoutstanding <=0:
            raise ValidationError(_('No outstanding fine amount to be paid.'))        
                         
        return data

    def clean_fine(self):
        data = self.cleaned_data['fine']
        
        try:
           if not fine>0:
              raise ValidationError(_('Invalid fine amount.'))
        except:
           raise ValidationError(_('Invalid fine amount.'))
        return data
