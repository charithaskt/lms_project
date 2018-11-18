#accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None,fullname=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.fullname = fullname
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password,fullname):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            fullname=fullname,
        )
        user.staff = True
        #user.active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,fullname):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            fullname=fullname,
        )
        user.staff = True
        user.admin = True
        #user.active = True
        user.save(using=self._db)
        return user
    
    def get_by_natural_key(self, email_):
        return self.get(email=email_)

# hook in the New Manager to our Model

from django.contrib.auth.models import PermissionsMixin
class User(AbstractBaseUser,PermissionsMixin ):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    fullname = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    email_confirmed = models.BooleanField(default=False)
    timestamp_added = models.DateTimeField(auto_now_add=True)
    # notice the absence of a "Password field", that's built in.
 
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname'] # Email & Password are required by default.
   
    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def natural_key(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active
   
    class Meta:
        permissions = (
	   ( 'edit_biblio_batchmode','Can perorm batch catalog modifications - ILS'),
	   ( 'bulk_import_cover_images','Can bulk import local cover images - ILS'),
	   ( 'bulk_import_patron_images','Can bulk import patron photographs - ILS'),
	   ( 'backup_restore','Can perform system backup & restore - ILS'),
	   ( 'borrow','Can borrow - ILS'),
	   ( 'circulate_place_holds','Can circulate & place holds - ILS'),
	   ( 'collect_fines_fees','Can collect fines & fees - ILS'),
	   ( 'delete_anonymize_patrons','Can delete old borrowers - ILS'),
	   ( 'edit_calendar','Can set calendar - ILS'),
	   ( 'edit_biblio','Can edit catalog - ILS'),
	   ( 'edit_items','Can edit items data - ILS'),
	   ( 'edit_news','Can write news - ILS'),
	   ( 'edit_patrons','Can edit performs data - ILS'),
	   ( 'edit_quotations','Can edit quotes - ILS'),
	   ( 'execute_reports','Can run reports - ILS'),
	   ( 'bulk_export_catalog','Can bulk export catalog & items data - ILS'),
	   ( 'force_checkout','Can force checkout to restricted borrowers - ILS'),
	   ( 'bulk_import_catalog','Can bulk import catalog & items data - ILS'),
	   ( 'bulk_import_patrons','Can bulk import patrons data - ILS'),
	   ( 'edit_items_batchmode','Can perform batch item modifications - ILS'),
	   ( 'manage_circ_rules','Can manage circulation rules - ILS'),
	   ( 'manage_restrictions','Can manage account restrictions - ILS'),
	   ( 'manage_system_preferences','Can manage system preferences - ILS'),
	   ( 'moderate_comments','Can moderate user comments - ILS'),
	   ( 'moderate_suggestions','Can moderate user suggestions - ILS'),
	   ( 'moderate_tags','Can moderate user tags - ILS'),
	   ( 'modify_holds_priority','Can modify hold priority - ILS'),
	   ( 'edit_patrons_batchmode','Can perform batch patron modifications - ILS'),
	   ( 'run_confidential_reports','Can run confidential reports - ILS'),
	   ( 'upload_local_cover_images','Can upload local cover images - ILS'),
	   ( 'upload_patron_images','Can upload patron photographs - ILS'),
	   ( 'writeoff','Can write off fines & fees - ILS'),
	   ( 'self_renew','Can self renew – ILS'),
	   ( 'self_reserve','Can self reserve – ILS'),
	   ( 'suggest_books','Can suggest books – ILS'),
	   ( 'edit_genre','Can edit genre – ILS'),
	   ( 'edit_language','Can edit language – ILS'),
	   ( 'edit_stopwords','Can edit stopwords – ILS'),
	   ( 'edit_authors','Can edit authors – ILS'),
	   ( 'edit_biblioimages','Can_edit_biblioimages – ILS'),
	   ( 'edit_rentalcharges','Can edit rentalcharges – ILS'),
	   ( 'edit_entryexitlogs','Can edit entryexitlogs – ILS'),
	   ( 'edit_systempreferences','Can edit systempreferences – ILS'),

        ) 
title_choices = (
       ('Mr',  'Mr'),
       ('Ms',  'Ms'),
       ('Mrs', 'Mrs'),
       ('Sri', 'Sri'),
       ('Dr',  'Dr'),
       ('Prof','Prof'),
)
gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile') #1 to 1 link with Django User
    userid = models.CharField(max_length=16, help_text="Roll number/aadhar numberi/employee number",null=True,blank=True)
    surname = models.CharField(max_length=50)
    firstname =  models.CharField(max_length=50)
    title = models.CharField(max_length=4,choices=title_choices, default='Mr') 
    birth_date = models.DateField(null=True, blank=True)
    mobile =  models.CharField(max_length=32)
    sex = models.CharField(max_length=1, choices=gender_choices,default='M') 
    address = models.CharField(max_length=100, blank=True, null=True) 
    address2 = models.CharField(max_length=100, blank=True, null=True) 
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=6, blank=True, null=True)
    country =  models.CharField(max_length=50)
    timestamp_lastupdated = models.DateTimeField(auto_now=True)
    #timestamp_added = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
       return self.user.email

    def get_absolute_url(self):
       return reverse('profile-detail',args=[str(self.id)])
  
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()
    post_save.connect(create_profile, sender=User)

from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
