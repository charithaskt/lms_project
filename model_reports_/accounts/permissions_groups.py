from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, Profile  # import User model

def list_all_permissions():
   ps = Permission.objects.all()
   ps_count = ps.count()
   i = 0
   print("permissions = (")
   while i<ps_count:
       p = ps[i]
       print("(\"{}\",\"{}\"),".format(p.codename,p.name))
       i = i + 1
   print(")")

#get_all_permissions()

def list_groups():
   gs = Group.objects.all()
   print("groups = (")
   i=0
   while i<gs.count:
      g = gs[i]
      print("(\"{}\",",format(g.name)
      i = i + 1
   print(")")


def list_all_groups_permissions():
   gs = Group.objects.all()
   gs_count = gs.count()
   i = 0
   print("groups = (")
   while i<gs_count:
       g = gs[i]
       gps = g.permissions.all()
       gp_count = gps.count()
       j=0
       while j<gp_count:
          print("(\"{} - {}\"),".format(g,gps[j].codename))
          j = j + 1 A
       i = i + 1
   print(")")

def delete_groups():
    gs = Group.objects.all()
    gs_count = gs.count
    if gs_count()>0:
       i = 0
       while i<ps_count():
           group = gs[i]
           group.delete()
           i = i + 1
    
def delete_ils_permissions():
    delete_groups()
    ps = Permission.objects.filter(name__icontains='ILS')
    ps_count = ps.count()
    if ps_count()>0:
       i = 0
       while i<ps_count():
           permission = ps[i]
           permission.delete()
           i = i + 1


permissions = [
    {'codename':'edit_biblio_batchmode','name':'Can perorm batch catalog modifications - ILS'},
    {'codename':'bulk_import_cover_images','name':'Can bulk import local cover images - ILS'},
    {'codename':'bulk_import_patron_images','name':'Can bulk import patron photographs - ILS'},
    {'codename':'backup_restore','name':'Can perform system backup & restore - ILS'},
    {'codename':'borrow','name':'Can borrow - ILS'},
    {'codename':'circulate_place_holds','name':'Can circulate & place holds - ILS'},
    {'codename':'collect_fines_fees','name':'Can collect fines & fees - ILS'},
    {'codename':'delete_anonymize_patrons','name':'Can delete old borrowers - ILS'},
    {'codename':'edit_calendar','name':'Can set calendar - ILS'},
    {'codename':'edit_biblio','name':'Can edit catalog - ILS'},
    {'codename':'edit_items','name':'Can edit items data - ILS'},
    {'codename':'edit_news','name':'Can write news - ILS'},
    {'codename':'edit_patrons','name':'Can edit performs data - ILS'},
    {'codename':'edit_quotations','name':'Can edit quotes - ILS'},
    {'codename':'execute_reports','name':'Can run reports - ILS'},
    {'codename':'bulk_export_catalog','name':'Can bulk export catalog & items data - ILS'},
    {'codename':'force_checkout','name':'Can force checkout to restricted borrowers - ILS'},
    {'codename':'bulk_import_catalog','name':'Can bulk import catalog & items data - ILS'},
    {'codename':'bulk_import_patrons','name':'Can bulk import patrons data - ILS'},
    {'codename':'edit_items_batchmode','name':'Can perform batch item modifications - ILS'},
    {'codename':'manage_circ_rules','name':'Can manage circulation rules - ILS'},
    {'codename':'manage_restrictions','name':'Can manage account restrictions - ILS'},
    {'codename':'manage_system_preferences','name':'Can manage system preferences - ILS'},
    {'codename':'moderate_comments','name':'Can moderate user comments - ILS'},
    {'codename':'moderate_suggestions','name':'Can moderate user suggestions - ILS'},
    {'codename':'moderate_tags','name':'Can moderate user tags - ILS'},
    {'codename':'modify_holds_priority','name':'Can modify hold priority - ILS'},
    {'codename':'edit_patrons_batchmode','name':'Can perform batch patron modifications - ILS'},
    {'codename':'run_confidential_reports','name':'Can run confidential reports - ILS'},
    {'codename':'upload_local_cover_images','name':'Can upload local cover images - ILS'},
    {'codename':'upload_patron_images','name':'Can upload patron photographs - ILS'},
    {'codename':'writeoff','name':'Can write off fines & fees - ILS'},
    {'codename':'self_renew','name':'Can self renew – ILS'},
    {'codename':'self_reserve','name':'Can self reserve – ILS'},
    {'codename':'suggest_books','name':'Can suggest books – ILS'},
    {'codename':'edit_genre','name':'Can edit genre – ILS'},
    {'codename':'edit_language','name':'Can edit language – ILS'},
    {'codename':'edit_stopwords','name':'Can edit stopwords – ILS'},
    {'codename':'edit_authors','name':'Can edit authors – ILS'},
    {'codename':'edit_biblioimages','name':'Can_edit_biblioimages – ILS'},
    {'codename':'edit_rentalcharges','name':'Can edit rentalcharges – ILS'},
    {'codename':'edit_quotations','name':'Can edit quotations – ILS'},
    {'codename':'edit_entryexitlogs','name':'Can edit entryexitlogs – ILS'},
    {'codename':'edit_systempreferences','name':'Can edit systempreferences – ILS'},

]
groups_permissions = [
    {'group':'Technical Manager','codename':'add_user','name':''},
    {'group':'Technical Manager','codename':'change_user','name':''},
    {'group':'Technical Manager','codename':'delete_user','name':''},
    {'group':'Technical Manager','codename':'edit_biblio_batchmode','name':'Can perorm batch catalog modifications - ILS'},
    {'group':'Technical Manager','codename':'edit_items_batchmode','name':'Can perform batch item modifications - ILS'},
    {'group':'Technical Manager','codename':'bulk_export_catalog','name':'Can bulk export catalog & items data - ILS'},
    {'group':'Technical Manager','codename':'bulk_import_catalog','name':'Can bulk import catalog & items data - ILS'},
    {'group':'Technical Manager','codename':'bulk_import_cover_images','name':'Can bulk import local cover images - ILS'},
    {'group':'Technical Manager','codename':'bulk_import_patron_images','name':'Can bulk import patron photographs - ILS'},
    {'group':'Technical Manager','codename':'edit_patrons_batchmode','name':'Can perform batch patron modifications - ILS'},
    {'group':'Technical Manager','codename':'bulk_import_patrons','name':'Can bulk import patrons data - ILS'},
    {'group':'Technical Manager','codename':'delete_anonymize_patrons','name':'Can delete old borrowers - ILS'},
    {'group':'Technical Manager','codename':'backup_restore','name':'Can perform system backup & restore - ILS'},
    {'group':'Technical Manager','codename':'manage_circ_rules','name':'Can manage circulation rules - ILS'},
    {'group':'Technical Manager','codename':'manage_system_preferences','name':'Can manage system preferences - ILS'},
    {'group':'Technical Manager','codename':'run_confidential_reports','name':'Can run confidential reports - ILS'},
    {'group':'Catalogue Manager','codename':'moderate_comments','name':'Can moderate user comments - ILS'},
    {'group':'Catalogue Manager','codename':'moderate_suggestions','name':'Can moderate user suggestions - ILS'},
    {'group':'Catalogue Manager','codename':'moderate_tags','name':'Can moderate user tags - ILS'},
    {'group':'Technical Manager','codename':'add_departments','name':''},
    {'group':'Technical Manager','codename':'add_issuingrules','name':''},
    {'group':'Technical Manager','codename':'change_issuingrules','name':''},
    {'group':'Technical Manager','codename':'delete_issuingrules','name':''},
    {'group':'Technical Manager','codename':'edit_systempreferences','name':'Can edit systempreferences – ILS'},
    {'group':'Catalogue Manager','codename':'edit_genre','name':'Can edit genre – ILS'},
    {'group':'Catalogue Manager','codename':'add_genre','name':''},
    {'group':'Catalogue Manager','codename':'change_genre','name':''},
    {'group':'Catalogue Manager','codename':'delete_genre','name':''},
    {'group':'Catalogue Manager','codename':'edit_language','name':'Can edit language – ILS'},
    {'group':'Catalogue Manager','codename':'add_language','name':''},
    {'group':'Catalogue Manager','codename':'change_language','name':''},
    {'group':'Catalogue Manager','codename':'delete_language','name':''},
    {'group':'Catalogue Manager','codename':'edit_stopwords','name':'Can edit stopwords – ILS'},
    {'group':'Catalogue Manager','codename':'add_stopwords','name':''},
    {'group':'Catalogue Manager','codename':'change_stopwords','name':''},
    {'group':'Catalogue Manager','codename':'delete_stopwords','name':''},
    {'group':'Catalogue Manager','codename':'add_tags','name':''},
    {'group':'Catalogue Manager','codename':'change_tags','name':''},
    {'group':'Catalogue Manager','codename':'delete_tags','name':''},
    {'group':'Cataloguer','codename':'edit_biblio','name':'Can edit catalog - ILS'},
    {'group':'Cataloguer','codename':'edit_items','name':'Can edit items data - ILS'},
    {'group':'Cataloguer','codename':'upload_local_cover_images','name':'Can upload local cover images - ILS'},
    {'group':'Cataloguer','codename':'edit_authors','name':'Can edit authors – ILS'},
    {'group':'Cataloguer','codename':'add_authors','name':''},
    {'group':'Cataloguer','codename':'change_authors','name':''},
    {'group':'Cataloguer','codename':'delete_authors','name':''},
    {'group':'Cataloguer','codename':'add_biblio','name':''},
    {'group':'Cataloguer','codename':'change_biblio','name':''},
    {'group':'Cataloguer','codename':'delete_biblio','name':''},
    {'group':'Cataloguer','codename':'edit_biblioimages','name':'Can_edit_biblioimages – ILS'},
    {'group':'Cataloguer','codename':'add_biblioimages','name':''},
    {'group':'Cataloguer','codename':'change_biblioimages','name':''},
    {'group':'Cataloguer','codename':'delete_biblioimages','name':''},
    {'group':'Cataloguer','codename':'add_corporateauthor','name':''},
    {'group':'Cataloguer','codename':'change_corporateauthor','name':''},
    {'group':'Cataloguer','codename':'delete_corporateauthor','name':''},
    {'group':'Cataloguer','codename':'add_items','name':''},
    {'group':'Cataloguer','codename':'change_items','name':''},
    {'group':'Cataloguer','codename':'delete_items','name':''},
    {'group':'Cataloguer','codename':'add_publisher','name':''},
    {'group':'Cataloguer','codename':'change_publisher','name':''},
    {'group':'Cataloguer','codename':'delete_publisher','name':''},
    {'group':'Patron Manager','codename':'edit_calendar','name':'Can set calendar - ILS'},
    {'group':'Patron Manager','codename':'edit_patrons','name':'Can edit performs data - ILS'},
    {'group':'Patron Manager','codename':'force_checkout','name':'Can force checkout to restricted borrowers - ILS'},
    {'group':'Patron Manager','codename':'manage_restrictions','name':'Can manage account restrictions - ILS'},
    {'group':'Patron Manager','codename':'modify_holds_priority','name':'Can modify hold priority - ILS'},
    {'group':'Patron Manager','codename':'upload_patron_images','name':'Can upload patron photographs - ILS'},
    {'group':'Patron Manager','codename':'writeoff','name':'Can write off fines & fees - ILS'},
    {'group':'Patron Manager','codename':'add_borrowers','name':''},
    {'group':'Patron Manager','codename':'change_borrowers','name':''},
    {'group':'Patron Manager','codename':'delete_borrowers','name':''},
    {'group':'Patron Manager','codename':'add_departments','name':''},
    {'group':'Patron Manager','codename':'change_departments','name':''},
    {'group':'Patron Manager','codename':'delete_departments','name':''},
    {'group':'Patron Manager','codename':'add_designations','name':''},
    {'group':'Patron Manager','codename':'change_designations','name':''},
    {'group':'Patron Manager','codename':'delete_designations','name':''},
    {'group':'Patron Manager','codename':'add_holidays','name':''},
    {'group':'Patron Manager','codename':'change_holidays','name':''},
    {'group':'Patron Manager','codename':'delete_holidays','name':''},
    {'group':'Patron Manager','codename':'edit_rentalcharges','name':'Can edit rentalcharges – ILS'},
    {'group':'Patron Manager','codename':'add_rentalcharges','name':''},
    {'group':'Patron Manager','codename':'change_rentalcharges','name':''},
    {'group':'Patron Manager','codename':'delete_rentalcharges','name':''},
    {'group':'Reports Manager','codename':'execute_reports','name':'Can run reports - ILS'},
    {'group':'News Manager','codename':'edit_news','name':'Can write news - ILS'},
    {'group':'News Manager','codename':'edit_quotations','name':'Can edit quotes - ILS'},
    {'group':'News Manager','codename':'add_news','name':''},
    {'group':'News Manager','codename':'change_news','name':''},
    {'group':'News Manager','codename':'delete_news','name':''},
    {'group':'News Manager','codename':'add_quotations','name':''},
    {'group':'News Manager','codename':'change_quotations','name':''},
    {'group':'News Manager','codename':'delete_quotations','name':''},
    {'group':'Circulation Staff','codename':'circulate_place_holds','name':'Can circulate & place holds - ILS'},
    {'group':'Circulation Staff','codename':'collect_fines_fees','name':'Can collect fines & fees - ILS'},
    {'group':'Patron','codename':'borrow','name':'Can borrow - ILS'},
    {'group':'Patron','codename':'self_renew','name':'Can self renew – ILS'},
    {'group':'Patron','codename':'self_reserve','name':'Can self reserve – ILS'},
    {'group':'Patron','codename':'suggest_books','name':'Can suggest books – ILS'},
    {'group':'Gate Register Manager','codename':'edit_entryexitlogs','name':'Can edit entryexitlogs – ILS'},

]


groups = [
    'Technical Manager',
    'Technical Manager',
    'Catalogue Manager',
    'Cataloguer',
    'Patron Manager',
    'Reports Manager',
    'News Manager',
    'Circulation Staff',
    'Patron',	
]

def create_permissions():
    ct = ContentType.objects.get_for_model(User)
    i=0
    pcount = length(permissions)
    if pcount>0:
        while i<pcount:
           codename = permissions[i]['codename']
           name = permissions[i]['name']
           ps =  Permissions.objects.get(codename=codename)
           if ps:
              pass
           else:
              p = Permissions.objects.create(codename=codename,name=name,content_type=ct)
           i = i + 1:

              
def create_populate_groups():
    i=0
    ct = ContentType.objects.get_for_model(User)
    while i<length(groups_permissions):
        new_group, created = Group.objects.get_or_create(name=groups_permissions[i]['group'])
        if new_group:
            gperms = new_group.permissions.filter(codename=groups_permissions[i]['codename']).count()
            if gperms == 0:
                permission = Permissions.get(codename=groups_permissions[i]['codename']) 
                if permission:
                    new_group.permissions.add(permission)
                else:
                   if groups_permissions[i]['name']:
                       permission = Permission.create(codename=groups_permissions[i]['codename'],name=groups_permissions[i]['name'],content_type=ct)
                       if permission:
                          new_group.permissions.add(permission)
        i = i + 1
