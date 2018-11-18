from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, Profile  # import User model

def get_all_permissions():
   ps = Permission.objects.all()
   ps_count = ps.count()
   i = 0
   print("permissions = (")
   while i<ps_count:
       p = ps[i]
       print("(\"{}\",\"{}\"),".format(p.codename,p.name))
       i = i + 1
   print(")")

get_all_permissions()
