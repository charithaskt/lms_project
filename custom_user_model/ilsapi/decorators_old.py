from rest_framework.response import Response
from rest_framework.views import status
from intranet.models import Authors, Publisher, Suggestion, Borrowers, ModeratorReasons, Biblio, Genre
from intranet.models import Authors, CorporateAuthor, Language, Publisher
from intranet.models import suggestions_status_choices, itemtype_choices
import datetime
import re
import decimal
from accounts.models import User, Profile

def validate_request_data_authors(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        firstname = args[0].request.data.get("firstname", "")
        lastname = args[0].request.data.get("lastname", "")
        if not firstname or not lastname:
            return Response(
                data={
                    "message": "Both firstname and lastname are required to add an author"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            firstname = firstname.strip()
            re.sub(' +', ' ',firstname)
            lastname = lastname.strip()
            re.sub(' +', ' ',lastname)
            authors = Authors.objects.filter(firstname__iexact=firstname,lastname__iexact=lastname)
            if len(authors) > 0:
                return Response(
                    data={
                        "message": "A record with that author already exists"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        return fn(*args, **kwargs)
    return decorated

def validate_request_data_publishers(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        data = args[0].request.data
        messages=[]
        if isinstance(data,list):
            i=0
            while i<len(data):
               name = data[i].get("name")
               if not name:
                  messages.append("Record({}): Name is required".format(i+1))
               name = name.strip()
               re.sub(' +', ' ',name)
               publishers = Publisher.objects.filter(name__iexact=name)
               if len(publishers) > 0:
                  messages.append("Record({}) : An entry with that Name '{}' already exists".format(i+1,name))
               i=i+1
        else: 
           name=data.get('name')
           name = name.strip()
           re.sub(' +', ' ',name)
           publishers = Publisher.objects.filter(name__iexact=name)
           if len(publishers) > 0:
               messages.append("An entry with that Name '{}' already exists".format(name))
        if len(messages)>0:
            return Response(
                data={
                    "message": messages,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
                
        return fn(*args, **kwargs)
    return decorated

#put a check on max number of suggestions by an individual - limit 2
def validate_request_data_post_suggestions(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        profile_id = User.objects.get(email=args[0].request.user).profile.id
        user_= Borrowers.objects.get(borrower=profile_id)
        user_id=None
        if user_:
           user_id=user_.id
        if user_id==None:
            return Response(
               data={
                   "message": "You are not a library borrower. You can suggest only then."
               },
               status=status.HTTP_400_BAD_REQUEST
            )
           
        numberOfSuggestions = 0
        if user_:
            numberOfSuggestions = Suggestion.objects.filter(suggestedby=user_id,status='ASKED').count()
        if numberOfSuggestions>1:
            return Response(
                data={
                        "message": "You are not allowed to give more than 2 suggestions at a time"
                    },
                    status=status.HTTP_400_BAD_REQUEST
            )
        title = args[0].request.data.get("title", "")
        if not title:
            return Response(
                data={
                    "message": "Title is required for the suggestion to be added"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        isbn = args[0].request.data.get("isbn", "")
        if isbn:
            if len(isbn)>=10 and re.match(r'(\d{10}|\d{12}[0-9X])',isbn,re.M|re.I):
                pass
            else:
                return Response(
                    data={
                        "message": "Invalid ISBN"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        copyrightdate = args[0].request.data.get("copyrightdate", "")              
        if copyrightdate:
            yr = str(copyrightdate)
            year = re.match(r'(^\d{4}$)',yr)
            if year:
                pass   
            else:
                return Response(
                    data={
                        "message": "Invalid Copyrightdate"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        price = args[0].request.data.get("price", "")              
        if price:
            price_ = str(price)
            price = re.search(r'(\d{1,4}|\d{1,4}\.\d\d)',price_)
            if price:
                pass   
            else:
                return Response(
                    data={
                        "message": "Invalid price. Should be between 0 and 9999. No decimals allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        total = args[0].request.data.get("total", "")              
        if total:
            total_ = str(total)
            total = re.search(r'(\d{1,5}|\d{1,5}\.\d\d)',total_)
            if total:
                pass   
            else:
                return Response(
                    data={
                        "message": "Invalid total amount. Should be between 0 and 99999. No decimals allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return fn(*args, **kwargs)
        
    return decorated

def validate_request_data_put_suggestions(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        suggestion = Suggestion.objects.get(pk=kwargs["pk"])
        if suggestion:
            suggestedby = suggestion.suggestedby
        else:
            return Response(
                data={
                    "message": "No such suggestion exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        request_user = User.objects.get(email=args[0].request.user)
        profile_id = request_user.profile.id
        user_ = Borrowers.objects.get(borrower=profile_id)
        if not (request_user.staff==True or suggestedby == user_): 
            return Response(
                data={
                    "message": "Only staff or the owner can edit/delete/moderate suggestion"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user_:
            return Response(
                data={
                    "message": "You need to be a library borrower to edit/delete suggestion"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        #suggested_user = Borrowers.objects.get(borrower=suggestedby.borrower)
        existing_title = suggestion.title
        request_title = args[0].request.data.get("title","")
        if request_title!="" and user_!=suggestedby:
            return Response(
                data={
                    "message": "Only the owner of suggestion can change the title of the Suggestion"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        s_status = args[0].request.data.get("status", "")
        if s_status =="":
           s_status = suggestion.status
        if s_status=="":
            return Response(
                data={
                    "message": "Suggestion status can't be left empty"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
          s_status = s_status.upper()
          status_ = []
          for choice in suggestions_status_choices:
              status_.append(choice[0])
          if not s_status in status_:
              return Response(
                data={
                    "message": "Invalid suggestion status. Should be one of '{}'".format(status_)
                },
                status=status.HTTP_400_BAD_REQUEST
              )
          if user_==suggestedby and (not s_status=='ASKED'):
              return Response(
                  data={
                      "message": "You can't moderate your own suggestion. Leave the status as 'ASKED'."
                  },
                  status=status.HTTP_400_BAD_REQUEST
              )  
        isbn = args[0].request.data.get("isbn", "")
        if isbn:
            if re.match(r'(^\d{10}$|^\d{12}[0-9X]$)',isbn,re.M|re.I):
                pass
            else:
                return Response(
                    data={
                        "message": "Invalid ISBN"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        copyrightdate = args[0].request.data.get("copyrightdate", "")              
        if copyrightdate:
            year = re.match(r'(^\d{4}$)',copyrightdate)
            if year:
                copyrightdate = year   
            else:
                return Response(
                    data={
                        "message": "Invalid Copyrightdate"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        price = args[0].request.data.get("price", "")              
        if price:
            price_ = str(price)
            price = re.search(r'(\d{1,4}|\d{1,4}\.\d\d)',price_)
            if price:
                pass   
            else:
                return Response(
                    data={
                        "message": "Invalid price. Should be between 0 and 9999. No decimals allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        total = args[0].request.data.get("total", "")              
        if total:
            total_ = str(total)
            total = re.search(r'(\d{1,5}|\d{1,5}\.\d\d)',total_)
            if total:
                pass   
            else:
                return Response(
                    data={
                        "message": "Invalid total amount. Should be between 0 and 99999. No decimals allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        reason = args[0].request.data.get("reason", "")
        reasonids=[]
        if reason:
           reason=int(reason)
           reasons = ModeratorReasons.objects.all()               
           for reason_ in reasons:
               reasonids.append(reason_.id)
           if len(reasonids)>0 and reason not in reasonids:
               message = "Invalid reason. It should be a number and should be one of '{}'.".format(reasonids)
               return Response(
                   data={
                       "message": message,
                   },
                   status=status.HTTP_400_BAD_REQUEST
               )
        return fn(*args, **kwargs)
    return decorated



def validate_request_data_delete_suggestions(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        suggestion = Suggestion.objects.get(pk=kwargs["pk"])
        if suggestion:
            suggestedby = suggestion.suggestedby
        else:
            return Response(
                data={
                    "message": "No such suggestion exists"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        request_user = User.objects.get(email=args[0].request.user)
        profile_id = request_user.profile.id
        user_ = Borrowers.objects.get(borrower=profile_id)
        if not (request_user.staff==True or suggestedby == user_): 
            return Response(
                data={
                    "message": "Only staff or the owner can edit/delete/moderate suggestion"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)
    return decorated


def validate_request_data_biblio(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        isbn = args[0].request.data.get("isbn", "")
        if isbn:
            if len(isbn)>=10 and re.search(r'(^\d{10}$s|^\d{12}[0-9x]$)',isbn,re.M|re.I):
                pass
            else:
                return Response(
                    data={
                        "message": "Invalid ISBN"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        copyrightdate = args[0].request.data.get("copyrightdate", "")              
        if copyrightdate:
            yr = str(copyrightdate)
            if re.match(r'(^\d{4}$)',yr):
                pass   
            else:
                return Response(
                    data={
                        "message": "Invalid Copyrightdate. It should be year of publication."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
                
                return fn(*args, **kwargs)

        itemtype = args[0].request.data.get("itemtype", "")
        if itemtype:
           itemtypes = []
           for itemtype_ in itemtype_choices:
               itemtypes.append(itemtype_[0])   
           if itemtype.upper()  not in itemtypes:
               message = "Invalid itemtype: It should be one of '{}'.".format(itemtypes)
               return Response(
                   data={
                       "message": message,
                   },
                   status=status.HTTP_400_BAD_REQUEST
               ) 
        corporateauthor = args[0].request.data.get("corporateauthor", "")
        corpauthor_ids=[]
        if corporateauthor:
           corporateauthor=int(corporateauthor)
           corpauthors = CorporateAuthor.objects.all()               
           for corpauthor_ in corpauthors:
               corpauthor_ids.append(corpauthor_.id)
           if len(corpauthor_ids)>0 and corporateauthor not in corpauthor_ids:
               message = "Invalid corporate author. It should be a number and should be one of '{}'.".format(corpauthor_ids)
               return Response(
                   data={
                       "message": message,
                   },
                   status=status.HTTP_400_BAD_REQUEST
               )
        publisher = args[0].request.data.get("publisher", "")
        if publisher:
           if not Publisher.objects.get(pk=int(publisher)):
               message = 'Publisher[{}] is invalid'.format(publisher)
               return Response(
                   data={
                       "message": message,
                   },
                   status=status.HTTP_400_BAD_REQUEST
               )
        language = args[0].request.data.get("language", "")
        if language:
           if not Language.objects.get(pk=int(language)):
               message = 'Language[{}] is invalid'.format(language)
               return Response(
                   data={
                       "message": message,
                   },
                   status=status.HTTP_400_BAD_REQUEST
               ) 
        authors = args[0].request.data.get("authors", "")
        message = []
        if len(authors)>0:
           for author in authors:
               if not Authors.objects.get(pk=int(author)):
                   message.append('Author[{}] is invalid'.format(author))      
           if len(message)>0:               
               return Response(
                   data={
                       "message": message,
                   },
                   status=status.HTTP_400_BAD_REQUEST
               )
        
        genre = args[0].request.data.get("genre", "")
        message = []
        if len(genre)>0:
           for genre_ in genre:
               if not Genre.objects.get(pk=int(genre_)):
                   message.append('Genre[{}] is invalid'.format(genre))      
           if len(message)>0:               
               return Response(
                   data={
                       "message": message,
                   },
                   status=status.HTTP_400_BAD_REQUEST
               )
        
        return fn(*args, **kwargs)        
    return decorated
