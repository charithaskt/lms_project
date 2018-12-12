from django.db import models
from django.urls import reverse #Used to generate urls by reversing the URL patterns
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Profile
from django.utils import timezone
from datetime import datetime
from django.utils.html import format_html
from djangoql.queryset import DjangoQLQuerySet
itemtype_choices = ( 
       ('BK', 'Book'),
       ('PR', 'Project Report'),
       ('TD', 'Theses'),
       ('XM', 'Xerox Material'),
       ('RB', 'Reference Book'),
)

item_status_choices = (
       ('AV', 'Available'),
       ('OL', 'On Loan'),
       ('DM', 'Damaged'),
       ('LO', 'Lost'),
       ('LP', 'Lost and Paid for'),
       ('MI', 'Missing'),
       ('WD', 'Withdrawn'),
       ('BD', 'In Bindery'),
)
location_choices = (
        ('GEN', 'General Shelf'),
        ('REF', 'Reference Shelf'),
        ('OD' , 'On-Display'),
        ('PROC','Processing Center'),
        ('SO',  'Staff Office'),
        ('BC',  'Book Cart'),
        ('NMS', 'New Materials Shelf'),
)
notforloan_choices = (
        ('1', 'Not for loan'),
        ('2', 'Staff Copy'),
        ('3', 'Ordered'),
)
typecode_choices = (
       ('ISSUE',  'issue'),
       ('RETURN', 'return'),
       ('RENEW',  'renew'),
       ('PAYMENT','payment'),
)
accounttype_choices = (
       ('F', 'Fine levied'),
       ('FU', 'Overdue Fine'),
       ('N', 'New Card'),
       ('FOR','Forgiven'),
       ('FFOR', 'Forgiven Overdue Fine'),
       ('M', 'Sundry'),
       ('PAY', 'Payment'),
       ('REP', 'Replacement Charge'),
       ('RES', 'Reserve Charge'),
       ('W', 'Written off'), 
       ('RENT', 'Rental Charge'),
)
module_choices = (
   ('CATALOGING', 'Cataloguing'),
   ('CIRCULATION', 'Circulation'),
   ('PATRONS', 'Patrons'),
   ('SYSTEMPREFERENCES', 'System Preferences'),
   ('FINES', 'Fines'), 
   ('REPORT', 'Report'),
   ('TOOLS', 'Tools'), #bulk import/export, backup/restore, global modiffs
   ('CALENDAR', 'Holiday Calendar'),
)

action_choices = (
  ('CREATE', 'Create'),
  ('ADDCHILD', 'Add child record'),
  ('MODCHILD', 'Modify child record'),
  ('DELCHILD', 'Delete child record'),
  ('MODIFY', 'Modify or edit record'),
  ('ISSUE', 'Issue'),
  ('RETURN', 'Return'),
  ('RENEW', 'Renew'),
  ('DELETE', 'Delete'),
  ('CHANGE PASS', 'Change Password Through OPAC'),
  ('RESERVE', 'Reserve'),
  ('FINE', 'Collect fine'),
  ('WRITEOFF', 'Write off fine'),
  ('RUN', 'Run report'),
  ('RENEWSELF', 'Renew self'),
  ('RESERVESELF', 'Reserve self'),
)

"""
Sample reasons:
moderator_reason_choices = (
  ('1',  'No author mentioned'),
  ('2',  'Library already has enough copies'),
  ('3',  'Expensive'),
  ('4',  'Not relevant for the course'),
  ('5',  'Institution policies do not permit the purchase'),
  ('6',  'Will be purchased soon'),
  ('7',  'Will be purchased later'),
  ('8',  'Out of print'),
  ('9',  'Can not get immediately as it has to be imported'),
  ('10', 'Single copy will be purchased'),
  ('11', 'Few copies will be purchased'),
  ('12', 'Publisher not known'),
  ('13', 'No such title'),
  ('14', 'Not immediately required'),
)
"""

suggestions_status_choices = (
   ('ASKED', 'User asked'),
   ('ACCEPTED', 'Suggestion has been accepted'),
   ('REJECTED', 'Suggestion has been rejected'),
) 

holiday_type_choices = (
   ('WEEKEND', 'Weekend holiday'), # Sundays and (Saturdays if all are holidays)
   ('YEARLY', 'Yearly holidays on the same day'),
   ('ADHOC', 'Adhoc holidays'),
)

"""
Sample category codes. Individual library may like have their
own choices here.
This category is used for setting circulation rules
categorycode_choices = (
        ('SU' , 'Student - UG'),
        ('SP' , 'Student - PG'),
        ('SR' , 'Student - Research Scholar'),
        ('FT'   , 'Teaching Staff'),
        ('NT'   , 'Non-Teaching Staff'),
        ('LS'   , 'Library Staff'), #may be removed and categorized under 'NT'
        ('HA'   , 'Higher Authority'),
)

"""
#when a user self registers he will automatically become member of the library.
#But the user can't start borrowing untill categorized into one of the above 
#mentioned groups. 

class Categories(models.Model):
    categorycode = models.CharField(max_length=10,unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.categorycode)

class Departments(models.Model):
    deptcode = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.deptcode)

class CollectionDepartments(models.Model):
    deptcode = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.deptcode)

class Designations(models.Model):
    designation = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return "{} ({})".format(self.description, self.designation)

class Borrowers(models.Model):
   borrower = models.ForeignKey(
      Profile,
      on_delete=models.SET_NULL,
      null=True
   )
   email = models.EmailField(max_length=255,
      unique=True,
   )
   cardnumber = models.CharField(max_length=16, unique=True) #should be unique field
   surname = models.CharField(max_length=100) #should be unique field
   firstname = models.CharField(max_length=100) #should be unique field
   mobile = models.CharField(max_length=32,blank=True,null=True)
   dateenrolled = models.DateField(auto_now_add=True)
   dateexpiry = models.DateField()
   gonenoaddress = models.BooleanField(default=False)
   lost = models.BooleanField(default=False)
   debarred = models.DateField(blank=True, null=True)
   debarredcomment = models.CharField(max_length=100, blank=True, null=True)
   category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
   department = models.ForeignKey(Departments,on_delete=models.SET_NULL, null=True, blank=True)
   designation = models.ForeignKey(Designations, on_delete=models.SET_NULL, null=True, blank=True)
   borrowernote  =  models.CharField(max_length=255, null=True, blank=True)
   opacnote  =  models.CharField(max_length=255,null=True, blank=True)
   timestamp_lastupdated = models.DateTimeField(auto_now=True)
   timestamp_added = models.DateTimeField(auto_now_add=True)

   def __str__(self):
        return "{},{} ({}) - [{}]".format( self.firstname,self.surname,self.cardnumber, self.category.categorycode)

   def get_absolute_url(self):
        return reverse('borrower-detail', args=[self.id])

   @property
   def totalissues(self): 
       issues = Issues.objects.filter(borrower_id=self.id, returned=False).count() 
       return issues

   @property
   def patronimage(self):
        return PatronPhotos.objects.filter(patron_id=self.id).first()
 
   @property
   def patronbulkphotos(self):
        return PatronBulkPhotos.objects.filter(patron_id=self.id).first()

class PatronImages(models.Model):
   borrower = models.ForeignKey(Borrowers,on_delete=models.CASCADE)
   mimetype = models.CharField(max_length=15)
   imagefile = models.BinaryField()


class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True, help_text='Enter the topic')
    
    def __str__(self):
        return self.name

class Language(models.Model):
    """
    Model representing a Language (e.g. English, Telugu, Tamil, Kannda, etc.)
    """
    name = models.CharField(max_length=30, unique=True,help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    class Meta:
        ordering = ['name',]

    def __str__(self):
       return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class CorporateAuthor(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ('name',) 
    
    def __str__(self):
        return self.name

class Authors(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)

    @property
    def name(self):
        return "{}, {}".format(self.firstname, self.lastname)

    def __str__(self):
        return "{}, {}".format(self.firstname, self.lastname)

    def get_absolute_url(self):
        return reverse('authors-detail', args=[self.id])
    
    class Meta:
       unique_together = ('firstname', 'lastname',)
       ordering = ('firstname','lastname',)

class Biblio(models.Model):
    biblionumber = models.AutoField(primary_key=True)
    isbn = models.CharField('ISBN', max_length=13,null=True,blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    callnumber = models.CharField(max_length=15, blank=True, null=True)
    authors = models.ManyToManyField(Authors, blank=True,verbose_name="authors")
    corporateauthor = models.ForeignKey(CorporateAuthor, on_delete=models.SET_NULL, blank=True,null=True)
    title = models.CharField(max_length=250)
    edition = models.CharField(max_length=50, null=True, blank=True)
    copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Publication details")
    series = models.CharField(max_length=250, null=True, blank=True)
    volume = models.CharField(max_length=20, null=True, blank=True)
    pages = models.CharField(max_length=10)
    size  = models.CharField(max_length=5, null=True,blank=True)
    genre = models.ManyToManyField(Genre,blank=True,verbose_name="Topical Term")
    contents_url = models.URLField(max_length=200, blank=True, null=True)
    index_url = models.URLField(max_length=200, blank=True, null=True)
    itemtype = models.CharField(
       max_length = 2,
       choices = itemtype_choices,
       default = 'BK',
    ) 
    totalissues = models.IntegerField(default=0, null=True, blank=True)  #system generated  
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #system generated
    timestamp_added = models.DateTimeField(auto_now_add=True) #system generated
    
    class Meta:
        ordering = ['title',]

    '''
    def __str__(self):
        return "{} : {}".format(self.itemtype, self.title)
    '''
    def __str__(self):
            return '%d, %s / BY (%s)' % (
                self.biblionumber,
                self.title, 
                ', '.join(b.name for b in self.authors.all()) 
                )

    def get_absolute_url(self):
        return reverse('biblio-detail', args=[self.biblionumber])

    @property
    def subject_headings(self):
        return format_html('<br/>'.join([g.name for g in self.genre.all()]))
    
    @property
    def author_names(self):
        return format_html('<br/>'.join([a.name for a in self.authors.all()]))
 
    @property
    def all_authors(self):
        return '; '.join([x.name for x in self.authors.all()])

    @property
    def all_genres(self):
        return '; '.join([x.name for x in self.genre.all()])

    @property
    def copies(self):
        return Items.objects.filter(biblionumber_id=self.biblionumber).count()

    @property
    def coverimage(self):
        #return PatronPhotos.objects.filter(patron_id=self.biblionumber).first()
        return LocalCoverImages.objects.filter(biblionumber=self.biblionumber).first()

    objects = DjangoQLQuerySet.as_manager()


class Items(models.Model):
    itemnumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=25, unique=True)
    dateaccessioned = models.DateField(default=timezone.now) #auto_now_add is removed
    booksellerid = models.CharField(max_length=25, blank=True, null=True)  
    invoicenumber = models.CharField(max_length=15, blank=True, null=True)
    invoicedate = models.DateField(default=timezone.now,blank=True, null=True) #removed auto_now_add=True
    totalissues = models.PositiveSmallIntegerField(null=True, blank=True) #default = 0 should be there
    itemstatus = models.CharField(max_length=2,choices=item_status_choices,default='AV')  
    location = models.CharField(max_length=4,choices=location_choices,default='GEN')  
    notforloan = models.CharField(max_length=1,choices=notforloan_choices,blank=True, null=True)  
    price  = models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
    replacementprice  = models.DecimalField(decimal_places=2,max_digits=7,blank=True, null=True)
    collectiondepartment = models.ForeignKey(CollectionDepartments,on_delete=models.SET_NULL, null=True, blank=True)
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #this field is set by the app
    timestamp_added = models.DateTimeField(auto_now_add=True)   #this field is set by the app

    def __str__(self):
        return self.barcode

    def get_absolute_url(self):
        return reverse('item-detail', args=[self.itemnumber])

    
class BiblioImages(models.Model):
    imagenumber = models.AutoField(primary_key=True),
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    mimetype = models.CharField(max_length=15) 
    imagefile = models.BinaryField()
    
    def get_absolute_url(self):
       return reverse('biblioimage-detail', args=[self.imagenumber])

class Reserves(models.Model):
    reserveid = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True)
    reservedate = models.DateTimeField(auto_now_add=True)
    cancellationdate = models.DateTimeField(null=True,blank=True) 
    priority = models.PositiveSmallIntegerField(null=True, blank=True)
    found = models.BooleanField(default=False)
    notificationdate = models.DateTimeField(null=True, blank=True)
    waitingdate = models.DateTimeField(null=True,blank=True)
    timestamp = models.DateTimeField(default=timezone.now) 
    
    def __str__(self):
       return "{} ({}) - {}/{} - {}".format(self.borrower, self.reservedate, self.biblionumber,self.item,self.priority)


#system automatically adds records to this table. No manual entry.
class AccountLines(models.Model):
   accountlines_id = models.AutoField(primary_key=True)
   borrower = models.ForeignKey(Borrowers,on_delete=models.CASCADE)
   itemnumber = models.ForeignKey(Items, blank=True, null=True, on_delete=models.SET_NULL)
   date = models.DateField(auto_now_add=True)
   amount  = models.DecimalField(decimal_places=2,max_digits=7)
   description = models.CharField(max_length=255, null=True, blank=True)
   accounttype = models.CharField(max_length=4,choices = accounttype_choices)
   manager_id = models.IntegerField()

#note -ve values for payments and +ve values for levies 

#system automatically adds records to this table when the visitor's id card is scanned at the entrace and exit
class EntryExitLogs(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE,null=True, blank=True)
   cardnumber = models.CharField(max_length=16)
   timeofentry = models.DateTimeField(null=True, blank=True)
   timeofexit = models.DateTimeField(null=True, blank=True)
   timespent = models.CharField(null=True,blank=True, max_length=8)
   imageurl  = models.CharField(null=True,blank=True, max_length=250)
   def __str__(self):
       return "{} ({} - {})".format(self.cardnumber, self.timeofentry, self.timeofexit)
   
   def get_absolute_url(self):
        return reverse('entryexitlog-detail', args=[self.id])

   class Meta:
     unique_together = ('cardnumber', 'timeofentry',)
     ordering = ('-timeofentry','cardnumber',)

#system generated records
class ActionLogs(models.Model):
   action_id = models.AutoField(primary_key=True)
   timestamp = models.DateTimeField(auto_now_add=True)
   usercode = models.ForeignKey(Borrowers,on_delete = models.CASCADE)
   module = models.CharField(max_length=17,choices=module_choices)
   action = models.CharField(max_length=11,choices=action_choices)
   def __str__(self):
       return "{} ({}) - {}/{}".format(self.usercode, self.timestamp.date(), self.module,self.action)

class SystemPreferences(models.Model):
   variable = models.CharField(max_length=50,unique=True)
   value = models.CharField(max_length=255)
   options = models.CharField(max_length=255) #options separated by '|' symbol
   descriptive_options = models.CharField(max_length=1000) #separated by '|' symbol
   explanation = models.CharField(max_length=255)
   vartype = models.CharField(max_length=20) #YesNo - Choice - TextInput
   
   def get_descriptive_value(self):
       retval = ''
       if self.vartype == 'YesNo':
          if int(self.value)==1:
             retval = 'Do'
          else:
             retval = "Don't"
       elif self.vartype == 'Choice':
           choices = self.descriptive_options.split('|')
           retval = choices[int(self.value)]
       else:   
           retval = self.value 
       return retval 

   def __str__(self):
       return "{} ({}) - {}".format(self.variable, self.get_descriptive_value(), self.explanation)

   def get_absolute_url(self):
       return reverse('edit-system-preference', args=[self.id])

class ModeratorReasons(models.Model):
   reason = models.CharField(max_length=255)

   class Meta:
       ordering = ('reason',)

   def __str__(self):
      return self.reason

class Suggestions(models.Model):
   suggestionid = models.AutoField(primary_key=True)
   suggestedby = models.ForeignKey(Borrowers,on_delete = models.CASCADE)
   suggesteddate = models.DateField(auto_now_add=True,blank=True,null=True)
   acceptedby = models.CharField(max_length=16, blank=True, null=True) #card number
   #acceptedby = models.IntegerField(blank=True, null=True)
   accepteddate = models.DateField(auto_now_add=True,blank=True,null=True) #no auto_now should be deliberately set
   rejectedby = models.CharField(max_length=16, blank=True,null=True) #card number
   #rejectedby = models.IntegerField(blank=True, null=True) 
   rejecteddate = models.DateField(auto_now_add=True,blank=True,null=True) #no auto_now should be deliberately set
   status = models.CharField(max_length=8,choices=suggestions_status_choices, default='ASKED')
   note = models.TextField(blank=True,null=True)
   author = models.CharField(max_length=100,blank=True,null=True)
   title  = models.CharField(max_length=255)
   copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True)
   publishercode = models.CharField(max_length=100,blank=True,null=True)
   isbn = models.CharField(max_length=13,blank=True,null=True)
   reason = models.ForeignKey(ModeratorReasons,on_delete=models.SET_NULL,blank=True, null=True)
   price = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
   total = models.DecimalField(max_digits=7,decimal_places=2,blank=True,null=True)

class Stopwords(models.Model):
   word = models.CharField(max_length=255, unique=True)
   def __str__(self):
      return self.word

class SearchHistory(models.Model):
   user = models.ForeignKey(Profile, on_delete=models.CASCADE)
   sessionid = models.CharField(max_length=32),
   query_desc = models.CharField(max_length=255)
   query_url = models.CharField(max_length=1000)
 
class Quotations(models.Model):
   source = models.CharField(max_length=255)
   text = models.CharField(max_length=1500)  
   timestamp = models.DateTimeField(auto_now_add=True)

   def __str__(self):
     return "{} :- {}".format(self.text, self.source)

   def get_absolute_url(self):
        return reverse('quote-detail', args=[self.id])

   class Meta:
     unique_together = ('source', 'text',)
     ordering = ('source','text',)


class News(models.Model):
   title = models.CharField(max_length=250)
   language = models.CharField(max_length=25)
   timestamp = models.DateTimeField(auto_now_add=True)
   expirationdate = models.DateField(null=True, blank=True)
   number = models.PositiveSmallIntegerField(null=True, blank=True)
   
   class Meta:
      unique_together = ('title','number')
      ordering = ['title']

   def __str__(self):
      return "{}:{} - ({}/{})".format(self.title, self.number,self.timestamp,
          self.expirationdate)

class RentalCharges(models.Model):
   itemtype = models.CharField(choices=itemtype_choices, max_length=2)
   rentalcharge =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
   def __str__(self):
      return "{} :- {}".format(self.itemtype, self.rentalcharge)

class Tags(models.Model):
   biblionumber = models.ForeignKey(Biblio, on_delete=models.SET_NULL,null=True, blank=True) 
   tag = models.CharField(max_length=100)
   approved = models.NullBooleanField(null=True,blank=True)
   date_moderated = models.DateTimeField(auto_now_add=True,null=True, blank=True)
   approved_by = models.ForeignKey(Borrowers, on_delete=models.SET_NULL,null=True, blank=True)
   
   class Meta:
      unique_together = ('tag','biblionumber')

   def __str__(self):
      return "{} :- {}".format(self.tag, self.biblionumber)

class Comments(models.Model):
   biblionumber = models.ForeignKey(Biblio, on_delete=models.SET_NULL, null=True,blank=True) 
   comment = models.CharField(max_length=100)
   approved = models.NullBooleanField(null=True,blank=True)
   date_moderated = models.DateTimeField(auto_now_add=True,null=True, blank=True)
   approved_by = models.ForeignKey(Borrowers, on_delete=models.SET_NULL,null=True, blank=True)

   class Meta:
      unique_together = ('comment','biblionumber')

   def __str__(self):
      return "{} :- {}".format(self.tag, self.biblionumber)

class IssuingRules(models.Model):
   categorycode = models.ForeignKey(Categories,on_delete=models.CASCADE)
   itemtype = models.CharField(
       max_length = 2,
       choices = itemtype_choices,
       default = 'BK',
       )
   maxissueqty = models.PositiveSmallIntegerField()
   issuelength = models.PositiveSmallIntegerField()
   renewalsallowed = models.PositiveSmallIntegerField(default=0)
   reservesallowed = models.PositiveSmallIntegerField(default=0)
   overduefinescap =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
   rentaldiscount  =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
   fine =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
   finedays = models.PositiveSmallIntegerField(blank=True,null=True,default=0)
   chargeperiod = models.PositiveSmallIntegerField(blank=True,null=True,default=0)

   class Meta:
       unique_together = ('categorycode', 'itemtype',)

   def __str__(self):
       return "{}/{} - {}/{} days".format(self.itemtype, self.categorycode.categorycode, self.maxissueqty,self.issuelength)

   def get_absolute_url(self):
       return reverse('issuingrules-detail', args=[self.id])

class Issues(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
   item  = models.ForeignKey(Items, on_delete=models.CASCADE)
   date_due = models.DateTimeField()
   issuedate = models.DateTimeField(default=timezone.now)
   renewals = models.PositiveSmallIntegerField(default=0) #system sets this value
   returndate = models.DateTimeField(blank=True,null=True) #system sets this value
   returned = models.BooleanField(default=False)
   timestamp_lastupdated = models.DateTimeField(auto_now=True)

   class Meta:
       unique_together = ('borrower', 'item','returned',)

   def __str__(self):
       return "{}/{} - {}".format(self.borrower, self.item, "Returned" if self.returned else self.date_due)

   def get_absolute_url(self):
       return reverse('issues-detail', args=[self.id])
   
#System addes records to statistics table - no manual entries
class Statistics(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
   item = models.ForeignKey(Items,null=True, blank=True, on_delete=models.SET_NULL)
   usercardnumber = models.CharField(max_length=16) 
   typecode = models.CharField(max_length=7,choices=typecode_choices) 
   value  = models.DecimalField(decimal_places=2,max_digits=7,default=0,blank=True, null=True)

   def __str__(self):
       return "{}/{} - {}".format(self.usercardnumber, self.typecode,self.datetime)


#system automatically adds records to this table. No manual entry.
class AccountOffsets(models.Model):
   borrower = models.OneToOneField(Borrowers, on_delete = models.CASCADE)
   amountoutstanding  = models.DecimalField(decimal_places=2,max_digits=7)

class Holidays(models.Model):
   date = models.DateField()
   isexception = models.BooleanField(default=True)
   title = models.CharField(max_length=100)
   holiday_type = models.CharField(max_length=7,choices=holiday_type_choices)

   def __str__(self):
       return "{}/{}: {} ({})".format(self.holiday_type,self.title,self.date,self.date.strftime('%a'))

class Suggestion(models.Model):
   suggestionid = models.AutoField(primary_key=True)
   suggestedby = models.ForeignKey(Borrowers,on_delete = models.CASCADE)
   suggesteddate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
   #acceptedby = models.CharField(max_length=16, blank=True, null=True) #card number
   acceptedby = models.IntegerField(blank=True, null=True)
   accepteddate = models.DateTimeField(blank=True,null=True) #no auto_now should be deliberately set
   #rejectedby = models.CharField(max_length=16, blank=True,null=True) #card number
   rejectedby = models.IntegerField(blank=True, null=True) 
   rejecteddate = models.DateTimeField(blank=True,null=True) #no auto_now should be deliberately set
   status = models.CharField(max_length=8,choices=suggestions_status_choices, default='ASKED')
   note = models.TextField(blank=True,null=True)
   author = models.CharField(max_length=100,blank=True,null=True)
   title  = models.CharField(max_length=255)
   copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True)
   publishercode = models.CharField(max_length=100,blank=True,null=True)
   isbn = models.CharField(max_length=13,blank=True,null=True)
   reason = models.ForeignKey(ModeratorReasons,on_delete=models.SET_NULL,blank=True, null=True)
   price = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
   total = models.DecimalField(max_digits=7,decimal_places=2,blank=True,null=True)
   class Meta:
       unique_together = ('title','suggestedby')

   def __str__(self):
       return "{} SUGGESTED BY {}: {}".format(self.title,self.suggestedby,self.status)


class PatronPhotos(models.Model):
    patron = models.OneToOneField(Borrowers, on_delete=models.CASCADE)
    imageurl  = models.FileField(upload_to='images/patronimages')
    class Meta:
        ordering = ['patron__cardnumber']

    def __str__(self):
        return "{} - {}, {}".format(self.patron.cardnumber, self.patron.firstname, self.patron.surname)

    def get_absolute_url(self):
        return reverse('patronphoto-detail', args=[self.pk])

class LocalCoverImages(models.Model):
    biblionumber = models.OneToOneField(Biblio, on_delete=models.CASCADE)
    imageurl  = models.FileField(upload_to='images/localcoverimages')

    def __str__(self):
        return "{} ({})".format(self.biblionumber.title, self.biblionumber.pages)

    def get_absolute_url(self):
        return reverse('localcoverimage-detail', args=[self.pk])



