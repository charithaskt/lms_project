from collections import OrderedDict

from django.db import models
from django.utils import timezone
from accounts.models import User, Profile 
from django_jinja_knockout.tpl import format_local_date, flatten_dict, str_dict, reverse, Str
from intranet.models import Issues, PatronPhotos
from djangoql.queryset import DjangoQLQuerySet
from django.utils.html import format_html
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

class CollectionDepartments(models.Model):
    deptcode = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Collection Department'
        verbose_name_plural = 'Collection Departments'
        ordering = ('deptcode',)

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('deptcode', self.deptcode),
            ('description', self.description),
        ])
        return str_fields
    
    def get_absolute_url(self):
        url = Str(reverse('collectiondepartment_detail', kwargs={'collectiondepartments_id': self.pk}))
        url.text = str(self.description)
        return url

    def __str__(self):
        return "{} ({})".format(self.deptcode, self.description)

class Departments(models.Model):
    deptcode = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Patron Department'
        verbose_name_plural = 'Patron Departments'
        ordering = ('deptcode',)

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('deptcode', self.deptcode),
            ('description', self.description),
        ])
        return str_fields
    
    def get_absolute_url(self):
        url = Str(reverse('department_detail', kwargs={'departments_id': self.pk}))
        url.text = str(self.description)
        return url

    def __str__(self):
        return "{} ({})".format(self.deptcode, self.description)

class Designations(models.Model):
    designation = models.CharField(max_length=10,unique=True)
    description = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Patron Designation'
        verbose_name_plural = 'Patron Designations'
        ordering = ('description',)

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('designation', self.designation),
            ('description', self.description),
        ])
        return str_fields
    
    def get_absolute_url(self):
        url = Str(reverse('designation_detail', kwargs={'designations_id': self.pk}))
        url.text = str(self.description)
        return url

    def __str__(self):
        return self.description

class Language(models.Model):
    """
    Model representing a Language (e.g. English, Telugu, Tamil, Kannda, etc.)
    """
    name = models.CharField(max_length=30, unique=True,help_text="Enter the biblio item's natural language.",verbose_name='Language')

    class Meta:
        verbose_name = 'Biblio Language'
        verbose_name_plural = 'Biblio Languages'
        ordering = ['name',]

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('name', self.name),            
        ])
        return str_fields

    def get_absolute_url(self):
        url = Str(reverse('language_detail', kwargs={'language_id': self.pk}))
        url.text = str(self.name)
        return url
    
    def __str__(self):
       return self.name

class CorporateAuthor(models.Model):
    name = models.CharField(max_length=200, verbose_name="Corporate Author")

    class Meta:
        verbose_name = 'Corporate Body'
        verbose_name_plural = 'Corporate Bodies'
        ordering = ['name',]

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('name', self.name),            
        ])
        return str_fields

    def get_absolute_url(self):
        url = Str(reverse('corporateauthor_detail', kwargs={'corporateauthor_id': self.pk}))
        url.text = str(self.name)
        return url
    
    def __str__(self):
        return self.name

class Authors(models.Model):
    firstname = models.CharField(max_length=200, verbose_name='First Name')
    lastname = models.CharField(max_length=200, verbose_name='Last Name')
    
    class Meta:
        unique_together = ('firstname', 'lastname')
        verbose_name = 'Personal Author'
        verbose_name_plural = 'Personal Authors'
        ordering = ('firstname', 'lastname' )
    
    @property
    def name(self):
        return "{}, {}". format(self.lastname,self.firstname)

    def get_absolute_url(self):
        url = Str(reverse('author_detail', kwargs={'authors_id': self.pk}))
        url.text = "{}, {}". format(self.firstname,self.lastname)
        return url


    def get_str_fields(self):
        return OrderedDict([
            ('firstname', self.firstname),
            ('lastname', self.lastname),            
        ])

    def __str__(self):
        return ', '.join([self.firstname, self.lastname])

class Categories(models.Model):
    categorycode = models.CharField(max_length=10,unique=True,verbose_name='Borrower Category Code')
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.categorycode)

    class Meta:
        verbose_name = 'Patron Category'
        verbose_name_plural = 'Patron Categories'
        ordering = ('categorycode',)

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('categorycode', self.categorycode),
            ('description', self.description),
        ])
        return str_fields
    
    def get_absolute_url(self):
        url = Str(reverse('category_detail', kwargs={'categories_id': self.pk}))
        url.text = str(self.description)
        return url

    def __str__(self):
        return "{} ({})".format(self.categorycode, self.description)

class Borrowers(models.Model):
   borrower = models.ForeignKey(
      Profile,
      on_delete=models.SET_NULL,
      null=True,
      related_name="djk_borrower",
   )
   email = models.EmailField(max_length=255,
      unique=True,
   )
   cardnumber = models.CharField(max_length=16, unique=True,verbose_name='Cardnumber') #should be unique field
   surname = models.CharField(max_length=100,verbose_name='Last name') #should be unique field
   firstname = models.CharField(max_length=100,verbose_name='First name') #should be unique field
   birth_date = models.DateField(db_index=True, verbose_name='Birth date')
   mobile = models.CharField(max_length=32,blank=True,null=True)
   dateenrolled = models.DateField(auto_now_add=True)
   dateexpiry = models.DateField()
   gonenoaddress = models.BooleanField(default=False,verbose_name='Is Left')
   lost = models.BooleanField(default=False,verbose_name='Is Card Lost')
   debarred = models.DateField(blank=True, null=True,verbose_name='Is Suspended')
   debarredcomment = models.CharField(max_length=100, blank=True, null=True)
   category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Patron Category')
   department = models.ForeignKey(Departments,on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Patron Department')
   designation = models.ForeignKey(Designations, on_delete=models.SET_NULL, null=True, blank=True,verbose_name='Patron Desingation')
   borrowernote  =  models.CharField(max_length=255, null=True, blank=True, verbose_name='Borrower Intranet Note')
   opacnote  =  models.CharField(max_length=255,null=True, blank=True,verbose_name='Borrower OPAC Note')
   timestamp_lastupdated = models.DateTimeField(auto_now=True)
   timestamp_added = models.DateTimeField(auto_now_add=True)
   class Meta:
        unique_together = ('firstname', 'surname', 'birth_date')
        verbose_name = 'Borrower Record'
        verbose_name_plural = 'Borrower Records'
        ordering = ('firstname', 'surname', 'birth_date')

   def get_str_fields(self):
        return OrderedDict([
            ('email', self.borrower.user.email),
            ('firstname', self.firstname),
            ('surname', self.surname),
            ('birth_date', format_local_date(self.birth_date)),
            ('cardnumber', self.cardnumber),
            ('category', self.category.description),
            ('is_active', 'present' if not self.gonenoaddress else 'left')
        ])

   def __str__(self):
        print(str_dict(self.get_str_fields()))
        return str_dict(self.get_str_fields())

   """
   def __str__(self):
        return ' '.join([self.firstname, self.surname, self.borrower.user.email])
    
   def __str__(self):
        return "{},{} ({}) - [{}]".format( self.firstname,self.surname,self.cardnumber, self.category.categorycode)
   """
   def get_absolute_url(self):
        return reverse('borrower-detail', args=[self.id])

   @property
   def totalissues(self): 
       issues = Issues.objects.filter(borrower_id=self.id, returned=False).count() 
       return issues

class Supplier(models.Model):
    company_name = models.CharField(max_length=64, unique=True, verbose_name='Company name')
    direct_shipping = models.BooleanField(verbose_name='Direct shipping')

    class Meta:
        verbose_name = 'Book Supplier'
        verbose_name_plural = 'Book Suppliers'
        ordering = ('company_name',)

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('company_name', self.company_name),
        ])
        str_fields['direct_shipping'] = 'Yes (direct)' if self.direct_shipping else 'No (remote)'
        return str_fields

    def __str__(self):
        return self.get_str_fields().values()

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Publisher Name')
    
    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'
        ordering = ('name',)

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('name', self.name),
        ])
        return str_fields

    def get_absolute_url(self):
        url = Str(reverse('publisher_detail', kwargs={'publisher_id': self.pk}))
        url.text = str(self.name)
        return url
    
    def __str__(self):
        str_fields = flatten_dict(self.get_str_fields(), enclosure_fmt=None)
        try:
          if str_fields['name']:
             return str_fields['name']
        except:
          return ""

class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name='Subject Name')
    
    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ('name',)
    
    def get_absolute_url(self):
        url = Str(reverse('genre_detail', kwargs={'genre_id': self.pk}))
        url.text = str(self.name)
        return url

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('name', self.name),
        ])
        return str_fields

    def __str__(self):
        str_fields = flatten_dict(self.get_str_fields(), enclosure_fmt=None)
        try:
          genre = str_fields['name']
          if genre:
             return genre
        except:
          return ""

itemtype_choices = ( 
       ('BK', 'Book'),
       ('PR', 'Project Report'),
       ('TD', 'Theses'),
       ('XM', 'Xerox Material'),
       ('RB', 'Reference Book'),
)
class Biblio(models.Model):
    biblionumber = models.AutoField(primary_key=True)
    isbn = models.CharField('ISBN', max_length=13,null=True,blank=True)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    callnumber = models.CharField(max_length=15, blank=True, null=True)
    first_author = models.ForeignKey(Authors,blank=True, null=True,on_delete=models.SET_NULL,verbose_name='Primary Author')
    authors = models.ManyToManyField(Authors, blank=True,verbose_name="all authors", related_name='additional_authors')
    corporateauthor = models.ForeignKey(CorporateAuthor, on_delete=models.SET_NULL, blank=True,null=True, verbose_name='Corporate Author')
    title = models.CharField(max_length=250,verbose_name='Biblio Title')
    edition = models.CharField(max_length=50, null=True, blank=True)
    copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Copyright Date')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Publication Details")
    series = models.CharField(max_length=250, null=True, blank=True)
    volume = models.CharField(max_length=20, null=True, blank=True)
    pages = models.CharField(max_length=10)
    size  = models.CharField(max_length=5, null=True,blank=True)
    subject_heading = models.ForeignKey(Genre, blank=True, null=True, on_delete=models.SET_NULL,verbose_name="Subject Heading")
    genre = models.ManyToManyField(Genre,blank=True,verbose_name="Topical Term(s)", related_name="Topical_Terms")
    contents_url = models.URLField(max_length=200, blank=True, null=True)
    index_url = models.URLField(max_length=200, blank=True, null=True)
    itemtype = models.CharField(
       max_length = 2,
       choices = itemtype_choices,
       default = 'BK',
       db_index=True,
       verbose_name='Item Type',
    ) 
    totalissues = models.IntegerField(default=0, null=True, blank=True)  #system generated  
    totalholds = models.IntegerField(default=0, null=True, blank=True)  #system generated  
    timestamp_lastupdated = models.DateTimeField(auto_now=True,db_index=True) #system generated
    timestamp_added = models.DateTimeField(auto_now_add=True, db_index=True) #system generated
    # 
    class Meta:
        verbose_name = 'Biblio'
        verbose_name_plural = 'Biblios'
        ordering = ('title',)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
           self.last_update = timezone.now()
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        url = Str(reverse('biblio_detail', kwargs={'biblionumber': self.pk}))
        url.text = str(self.title)
        return url

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('title', self.title),
            ('itemtype', self.get_itemtype_display()),
            ('copyrightdate', str(self.copyrightdate)), 
            ('date_added', format_local_date(self.timestamp_added)),
            ('last_update', format_local_date(self.timestamp_lastupdated)),
            ('totalissues', str(self.totalissues)),
        ])
        if self.publisher is not None:
            str_fields['publisher'] = self.publisher.get_str_fields()
        if self.first_author is not None:
            str_fields['first_author'] = self.first_author.name
        if self.authors is not None:
            str_fields['authors'] = self.author_names
        if self.corporateauthor is not None:
            str_fields['corporateauthor'] = self.corporateauthor.name
        if self.subject_heading is not None:
            str_fields['subject_heading'] = self.subject_heading.get_str_fields()
        if self.genre is not None:
            str_fields['genre'] = self.subject_headings
        return str_fields
       
    def __str__(self):
        str_fields = flatten_dict(self.get_str_fields(), enclosure_fmt=None)
        try:
          if str_fields['first_author'] and str_fields['copyrightdate']:
             return ' › '.join([str_fields['title'],str_fields['first_author'], str_fields['copyrightdate'],str_fields['itemtype']])
        except:
          return "{}({})".format(str_fields['title'],str_fields['itemtype'])

    @property
    def subject_headings(self):
        #return format_html('<br/>'.join([g.name for g in self.genre.all()]))
        return ' | '.join([g.name for g in self.genre.all()])
    
    @property
    def author_names(self):
        #return format_html('<br/>'.join([a.name for a in self.authors.all()]))
        return ' | '.join([a.name for a in self.authors.all()])

    @property
    def copies(self):
        return Items.objects.filter(biblionumber_id=self.biblionumber).count()

    @property
    def coverimage(self):
        return PatronPhotos.objects.filter(patron_id=self.biblionumber).first()

    objects = DjangoQLQuerySet.as_manager()

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
class Items(models.Model):
    itemnumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE, verbose_name='Biblio')
    barcode = models.CharField(max_length=25, unique=True, verbose_name='Accession Number Barcode')
    dateaccessioned = models.DateField(default=timezone.now) #auto_now_add is removed
    booksellerid = models.CharField(max_length=25, blank=True, null=True, verbose_name='Source of acquisition' )  
    invoicenumber = models.CharField(max_length=15, blank=True, null=True)
    invoicedate = models.DateField(default=timezone.now,blank=True, null=True) #removed auto_now_add=True
    totalissues = models.PositiveSmallIntegerField(default=0,null=True, blank=True) #default = 0 should be there
    itemstatus = models.CharField(max_length=2,choices=item_status_choices,default='AV', db_index=True, verbose_name='Item Availability Status')  
    location = models.CharField(max_length=4,choices=location_choices,default='GEN',verbose_name="Shelf location")  
    notforloan = models.CharField(max_length=1,choices=notforloan_choices,blank=True, null=True)  
    price  = models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
    replacementprice  = models.DecimalField(decimal_places=2,max_digits=7,blank=True, null=True)
    collectiondepartment = models.ForeignKey(CollectionDepartments,on_delete=models.SET_NULL, null=True, blank=True)
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #this field is set by the app
    timestamp_added = models.DateTimeField(auto_now_add=True)   #this field is set by the app
    class Meta:
        verbose_name = 'Biblio Item'
        verbose_name_plural = 'Biblio Items'

    def get_absolute_url(self):
        url = Str(reverse('item_detail', kwargs={'itemnumber': self.pk}))
        url.text = str(self.barcode)
        return url

    def get_str_fields(self):
        str_fields = OrderedDict([
            ('biblio', self.biblionumber.get_str_fields()),
            ('date_added',format_local_date(self.timestamp_added)),
            ('last_update',format_local_date(self.timestamp_lastupdated)),
            ('dateaccessioned',format_local_date(self.dateaccessioned)),
            ('barcode', self.barcode),
        ])
        str_fields['itemstatus'] = self.get_itemstatus_display()
        return str_fields

    def __str__(self):
        str_fields = self.get_str_fields()
        return str_dict(str_fields)
    

class Reserves(models.Model):
    borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE, verbose_name='Library Patron')
    biblio = models.ForeignKey(Biblio, on_delete=models.CASCADE,verbose_name='Biblio Reserved')
    item = models.ForeignKey(Items, on_delete=models.CASCADE, null=True, blank=True,verbose_name='Item Waiting')
    reservedate = models.DateTimeField(auto_now_add=True,verbose_name='Reserved On')
    cancellationdate = models.DateTimeField(null=True,blank=True,verbose_name='Reservation Cancelled On') 
    priority = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Hold Priority')
    found = models.BooleanField(default=False, verbose_name='Reserve Found?')
    notificationdate = models.DateTimeField(null=True, blank=True, verbose_name='Notified On')
    waitingdate = models.DateTimeField(null=True,blank=True, verbose_name='Date Waiting')
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #this field is set by the app
    
    class Meta:
        unique_together = ('borrower', 'biblio')
        verbose_name = 'Biblio Level Reservation'
        verbose_name_plural = 'Biblio Level Reservation'

    def get_absolute_url(self):
        url = Str(reverse('reserve_detail', kwargs={'reserve_id': self.pk}))
        str_fields = flatten_dict(self.get_str_fields(), enclosure_fmt=None)
        url.text = ' / '.join([str_fields['borrower'], str_fields['biblio'],str(str_fields['priority']) ])
        return url

    def get_str_fields(self):
        parts = OrderedDict([
            ('borrower', self.borrower.get_str_fields()),
            ('biblio', self.biblio.get_str_fields()),
            ('reservedate', format_local_date(self.reservedate)),
            ('priority',str(self.priority)),
        ])
        parts['item']=None
        try:
          parts['item'] = self.item.barcode if self.item else None
        except:
             pass
        parts['is_found'] = 'Yes (Reserve Found)' if self.found else 'No (Reserve Pending)'
        parts['last_update']= format_local_date(self.timestamp_lastupdated)
        if self.waitingdate:
           parts['waitingdate'] = format_local_date(self.waitingdate)
        return parts

    def __str__(self):
        str_fields = self.get_str_fields()
        return str_dict(str_fields)
    
    def save(self, *args, **kwargs):
        if self.pk is None:
           self.reservedate = timezone.now()
           if self.priority==0:
              last_priority=None
              try:
                 last_priority = Reserve.objects.latest('priority')
              except:
                 pass   
              if last_priority:
                 self.priority = last_priority.priority + 1
              else:
                 self.priority = 1 
        super().save(*args, **kwargs)

    
