from accounts.models import User
from django.contrib.auth import authenticate, login
import datetime
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

from .decorators import validate_request_data_authors, validate_request_data_post_suggestions,validate_request_data_put_suggestions, validate_request_data_delete_suggestions
from .decorators import validate_request_data_publishers
from .decorators import validate_request_data_biblio
from intranet.models import Authors, Publisher, Genre,CorporateAuthor, Language 
from .serializers import AuthorsSerializer, PublishersSerializer, TokenSerializer, UserSerializer
from .serializers import SuggestionsSerializer, SuggestionsByOwnerIdSerializer
from .serializers import SuggestionsPostSerializer, SuggestionsPutSerializer, BibliosSerializer
from .serializers import GenreSerializer, BibliosShowSerializer
from intranet.models import Suggestion, Borrowers, ModeratorReasons, Biblio
from accounts.models import User, Profile
import re
import decimal
# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class ListCreateAuthorsView(generics.ListCreateAPIView):
    """
    GET authors/
    POST authors/
    """
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = (permissions.IsAdminUser,)

    @validate_request_data_authors
    def post(self, request, *args, **kwargs):
        an_Author = Authors.objects.create(
            firstname=request.data["firstname"],
            lastname=request.data["lastname"]
        )
        return Response(
            data=AuthorsSerializer(an_Author).data,
            status=status.HTTP_201_CREATED
        )
    

class AuthorsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET author/:id/
    PUT author/:id/
    DELETE author/:id/
    """
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = (permissions.IsAdminUser,)
 
    def get(self, request, *args, **kwargs):
        try:
            an_author = self.queryset.get(pk=kwargs["pk"])
            return Response(AuthorsSerializer(an_author).data)
        except Authors.DoesNotExist:
            return Response(
                data={
                    "message": "Author with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND

            )

    def put(self, request, *args, **kwargs):
        try:
            an_author = self.queryset.get(pk=kwargs["pk"])
            serializer = AuthorsSerializer()
            updated_author = serializer.update(an_author, request.data)
            return Response(AuthorsSerializer(updated_author).data)
        except Authors.DoesNotExist:
            return Response(
                data={
                    "message": "Author with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            an_author = self.queryset.get(pk=kwargs["pk"])
            an_author.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Authors.DoesNotExist:
            return Response(
                data={
                    "message": "Author with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ListCreatePublishersView(generics.ListCreateAPIView):
    """
    GET publishers/
    POST publishers/
    """
    queryset = Publisher.objects.all()
    serializer_class = PublishersSerializer
    permission_classes = (permissions.IsAdminUser,)
         
    @validate_request_data_publishers
    def post(self, request, *args, **kwargs):
        #a_publisher = Publisher.objects.create(
        #    name=request.data["name"],            
        #)
        if not isinstance(request.data, list):
           data = [request.data]
        else:
           data = request.data
        serializer = PublishersSerializer(data=data, many=True)
        if serializer.is_valid(): 
           serializer.save()
           return Response(
              data=serializer.data,
              status=status.HTTP_201_CREATED
           )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublishersDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET publisher/:id/
    PUT publisher/:id/
    DELETE publisher/:id/
    """
    queryset = Publisher.objects.all()
    serializer_class = PublishersSerializer
    permission_classes = (permissions.IsAdminUser,)
 
    def get(self, request, *args, **kwargs):
        try:
            a_publisher = self.queryset.get(pk=kwargs["pk"])
            return Response(PublishersSerializer(a_publisher).data)
        except Publisher.DoesNotExist:
            return Response(
                data={
                    "message": "Publisher with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_publisher = self.queryset.get(pk=kwargs["pk"])
            serializer = PublisherSerializer()
            updated_publisher = serializer.update(a_publisher, request.data)
            return Response(PublishersSerializer(updated_publisher).data)
        except Publisher.DoesNotExist:
            return Response(
                data={
                    "message": "Publisher with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_publisher = self.queryset.get(pk=kwargs["pk"])
            a_publisher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Publisher.DoesNotExist:
            return Response(
                data={
                    "message": "Publisher with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """

    # This permission class will over ride the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


"""

class RegisterUsers(generics.CreateAPIView):
    #
    #POST auth/register/
    #
    permission_classes = (permissions.AllowAny,)
    
    @validate_request_data_users
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        fullname = request.data.get("fullname", "")
        if not email or (not password or not fullname):
            return Response(
                data={
                    "message": "email, password and fullname is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            fullname=fullname, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )

"""

class ListCreateSuggestionsView(generics.ListCreateAPIView):
    #
    #GET suggestions/
    #POST suggestions/
    
    queryset = Suggestion.objects.all()
    #queryset = User.objects.none() #required for DjangoModelPermissions
    serializer_class = SuggestionsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    @validate_request_data_post_suggestions
    def post(self, request, *args, **kwargs):
        profile_id = User.objects.get(email=request.user).profile.id
        borrower_ = Borrowers.objects.get(borrower=profile_id)
        
        author = request.data.get("author")
        if author:
            author=author.strip()
            author = re.sub(' +',' ',author)
        title = request.data.get("title")
        if title:
            title=title.strip()
            title = re.sub(' +',' ',title)
        note = request.data.get("note")
        if note:
            note=note.strip()
            note = re.sub(' +',' ',note)
        publishercode = request.data.get("publishercode")
        if publishercode:
            publishercode=publishercode.strip()
            publishercode = re.sub(' +',' ',publishercode)
        
        a_suggestion = Suggestion.objects.create(
            suggestedby=borrower_,
            author=author,
            title = title,
            status = "ASKED",
            rejecteddate=None,
            accepteddate=None,
            copyrightdate = request.data.get("copyrightdate"),
            publishercode = publishercode,
            note = note,
            price = request.data.get("price"),
            total = request.data.get("total"),
        )
        
        serializer = SuggestionsPostSerializer(data=request.data)
        if serializer.is_valid(): 
           serializer.save()
           return Response(
              data=serializer.data,
              status=status.HTTP_201_CREATED
           )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            data=SuggestionsSerializer(a_suggestion).data,
            status=status.HTTP_201_CREATED
        )

class ListCreateMySuggestionsView(generics.ListCreateAPIView):
    
    #GET mysuggestions/
    #POST mysuggestions/
    
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionsPostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    @validate_request_data_post_suggestions
    def post(self, request, *args, **kwargs):
        print('user=',request.user)
        profile_id = User.objects.get(email=request.user).profile.id
        print('prifileid=',profile_id)
        borrower_ = Borrowers.objects.get(borrower=profile_id)
        
        data = {} 
        author = request.data.get("author")
        if author:
            author=author.strip()
            author = re.sub(' +',' ',author)
            data["author"]=author
        title = request.data.get("title")
        if title:
            title=title.strip()
            title = re.sub(' +',' ',title)
            data["title"]=title.upper()
        note = request.data.get("note")
        if note:
            note=note.strip()
            note = re.sub(' +',' ',note)
            data["note"]=note
        publishercode = request.data.get("publishercode")
        if publishercode:
            publishercode=publishercode.strip()
            publishercode = re.sub(' +',' ',publishercode)
            data["publishercode"]=publishercode
        copyrightdate = request.data.get("copyrightdate")
        price = request.data.get("price")
        price = re.search(r'(\d+\.\d\d|\d+)',price).group(1)
        total = request.data.get("total")
        total = re.search(r'(\d+\.\d\d|\d+)',total).group(1)
        data["suggestedby"]=borrower_.id
        data["rejecteddate"]=None
        data["accepteddate"]=None
        data["copyrightdate"]=copyrightdate
        data["price"]=decimal.Decimal(price)
        data["total"]=decimal.Decimal(total)
        serializer = SuggestionsPostSerializer(data=data)
        if serializer.is_valid(): 
           serializer.save()
           return Response(
              data=serializer.data,
              status=status.HTTP_201_CREATED
           )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SuggestionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET suggestion/:id/
    PUT suggestion/:id/
    DELETE suggestion/:id/
    """
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            a_suggestion = self.queryset.get(pk=kwargs["pk"])
            return Response(SuggestionsSerializer(a_suggestion).data)
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "Suggestion with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data_put_suggestions
    def put(self, request, *args, **kwargs):
        author = request.data.get("author")
        if author:
            author=author.strip()
            author = re.sub(' +',' ',author)
            request.data["author"]=author
        title = request.data.get("title")
        if title:
            title=title.strip()
            title = re.sub(' +',' ',title)
            request.data["title"]=title
        note = request.data.get("note")
        if note:
            note=note.strip()
            note = re.sub(' +',' ',note)
            request.data["note"]=note          
        publishercode = request.data.get("publishercode")
        if publishercode:
            publishercode=publishercode.strip()
            publishercode = re.sub(' +',' ',publishercode)
            request.data["publishercode"]=publishercode
        try:
            a_suggestion = self.queryset.get(pk=kwargs["pk"])
            serializer = SuggestionsSerializer()
            profile_id = User.objects.get(email=request.user).profile.id
            borrower_ = Borrowers.objects.get(borrower=profile_id)
            request.data["status"]=request.data.get("status").upper() 
            if request.data.get("status")=="ASKED":
                request.data["rejecteddate"]=None
                request.data["accepteddate"]=None
                request.data["acceptedby"]=None
                request.data["rejectedby"]=None
            elif request.data.get("status")=="ACCEPTED":
                request.data["rejecteddate"]=None
                request.data["rejectedby"]=None
                if not a_suggestion.accepteddate:
                   request.data["accepteddate"]=datetime.datetime.now()
                   request.data["acceptedby"]=borrower_.id
            elif request.data.get("status")=="REJECTED":
                request.data["accepteddate"]=None
                request.data["acceptedby"]=None 
                if not a_suggestion.rejecteddate:
                   request.data["rejecteddate"]=datetime.datetime.now()
                   request.data["rejectedby"]=borrower_.id
                
            updated_suggestion = serializer.update(a_suggestion, request.data)
            return Response(SuggestionsSerializer(updated_suggestion).data)
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "Suggestion with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
    @validate_request_data_delete_suggestions
    def delete(self, request, *args, **kwargs):
        try:
            a_suggestion = self.queryset.get(pk=kwargs["pk"])
            a_suggestion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "Suggestion with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class MySuggestionsDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET mysuggestions/:id/
    PUT mysuggestions/:id/
    DELETE mysuggestions/:id/
    """
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionsPutSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    #permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            a_suggestion = self.queryset.get(pk=kwargs["pk"])
            return Response(SuggestionsSerializer(a_suggestion).data)
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "Suggestion with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data_put_suggestions
    def put(self, request, *args, **kwargs):

      try:
        a_suggestion = self.queryset.get(pk=kwargs["pk"])
        profile_id = User.objects.get(email=request.user).profile.id
        borrower_ = Borrowers.objects.get(borrower=profile_id)
        data = {}
        author = request.data.get("author")
        if author:
            author=author.strip()
            author = re.sub(' +',' ',author)
            data["author"]=author
        ''' 
        title = request.data.get("title")
        if title:
            title=title.strip()
            title = re.sub(' +',' ',title)
            data["title"]=title
        '''
        note = request.data.get("note")
        if note:
           if (borrower_.id==a_suggestion.suggestedby.id):
              note=note.strip()
              note = re.sub(' +',' ',note)
              data["note"]=note          
        status_=request.data.get("status").upper() 
        reason = request.data.get("reason")
        if reason and (not status_=="ASKED"):
           if not (borrower_.id==a_suggestion.suggestedby.id):
              data["reason"]=ModeratorReasons.objects.get(id=reason)          
        publishercode = request.data.get("publishercode")
        if publishercode:
            publishercode=publishercode.strip()
            publishercode = re.sub(' +',' ',publishercode)
            data["publishercode"]=publishercode
        copyrightdate = request.data.get("copyrightdate")
        copyrightdate = re.search(r'(\d+)',copyrightdate).group(1)
        if copyrightdate:
            data["copyrightdate"]=copyrightdate
        price = request.data.get("price")
        price = re.search(r'(\d+\.\d\d|\d+)',price).group(1)
        if price:
            data["price"]=decimal.Decimal(price)
        total = request.data.get("total")
        total = re.search(r'(\d+\.\d\d|\d+)',total).group(1)
        if total:
            data["total"]=decimal.Decimal(total)   
        status_=request.data.get("status").upper() 
        if status_=="ASKED":
            data["rejecteddate"]=None
            data["accepteddate"]=None
            data["acceptedby"]=None
            data["rejectedby"]=None
            data["status"]="ASKED"
        elif status_=="ACCEPTED":
            data["rejecteddate"]=None
            data["rejectedby"]=None
            data["status"]="ACCEPTED"
            if not a_suggestion.accepteddate:
                data["accepteddate"]=datetime.datetime.now()
                data["acceptedby"]=borrower_.id
        elif status_=="REJECTED":
            data["accepteddate"]=None
            data["acceptedby"]=None 
            data["status"]="REJECTED"
            if not a_suggestion.rejecteddate:
                data["rejecteddate"]=datetime.datetime.now()
                data["rejectedby"]=borrower_.id
        serializer = SuggestionsPutSerializer()                       
        updated_suggestion = serializer.update(a_suggestion, data)
        return Response(SuggestionsPutSerializer(updated_suggestion).data)
      except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "Suggestion with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data_delete_suggestions
    def delete(self, request, *args, **kwargs):
        try:
            a_suggestion = self.queryset.get(pk=kwargs["pk"])
            a_suggestion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "Suggestion with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


class SuggestionsByOwnerIdListView(generics.ListAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionsByOwnerIdSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        #
        #This view should return a list of all the purchases for
        #the user as determined by the username portion of the URL.
        #
        try:
           ownerid = self.kwargs['ownerid']
           suggestions_ = self.queryset.filter(suggestedby=ownerid)
           #return Response(SuggestionsSerializer(suggestions_).data)
           return suggestions_
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "No suggestion(s) with id: {} exist".format(kwargs["ownerid"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class SuggestionsByOwnerCardnumberListView(generics.ListAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionsByOwnerIdSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        #
        #This view should return a list of all the purchases for
        #the user as determined by the username portion of the URL.
        #
        try:
           cardnumber = self.kwargs['cardnumber']
           suggestions_ = self.queryset.filter(suggestedby__cardnumber__istartswith=cardnumber)
           #return Response(SuggestionsSerializer(suggestions_).data)
           return suggestions_
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "No suggestion(s) with cardnumber: {} exist".format(kwargs["cardnumber"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class SuggestionsByOwnerEmailListView(generics.ListAPIView):
    queryset = Suggestion.objects.all()
    serializer_class = SuggestionsByOwnerIdSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        #
        #This view should return a list of all the purchases for
        #the user as determined by the username portion of the URL.
        #
        try:
           email = self.kwargs['email']
           suggestions_ = self.queryset.filter(suggestedby__email__iexact=email)
           #return Response(SuggestionsSerializer(suggestions_).data)
           return suggestions_
        except Suggestion.DoesNotExist:
            return Response(
                data={
                    "message": "No suggestion(s) with emailid: {} exist".format(kwargs["email"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class BibliosByTitleListView(generics.ListAPIView):
    #GET biblios/byTitle/<str:title>
    queryset = Biblio.objects.all()
    serializer_class = BibliosShowSerializer
    #permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #
        #This view should return a list of all the purchases for
        #the user as determined by the username portion of the URL.
        #
        try:
           title = self.kwargs['title']
           title_ = self.queryset.filter(title__icontains=title)
           #return Response(BibliosShowSerializer(title_).data)
           return title_
        except Biblio.DoesNotExist:
            return Response(
                data={
                    "message": "No biblio with title keyword: {} exists".format(kwargs["title"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class BibliosByRangeListView(generics.ListAPIView):
    #GET biblios/byrange/<int:begin>
    queryset = Biblio.objects.all()
    serializer_class = BibliosShowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #
        #This view should return a list of all the purchases for
        #the user as determined by the username portion of the URL.
        #
        try:
           begin = int(self.kwargs['begin'])
           end = begin+4
           biblios_ = self.queryset.all()
           
           #return Response(BibliosShowSerializer(title_).data)
           return biblios_[begin : end]
        except Biblio.DoesNotExist:
            return Response(
                data={
                    "message": "No biblios in the given range between {} and {}".format(begin,begin+4)
                },
                status=status.HTTP_404_NOT_FOUND
            )
class BibliosByTitleRegxListView(generics.ListAPIView):
    #GET biblios/byregx/<str:regx>
    queryset = Biblio.objects.all()
    serializer_class = BibliosShowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        #
        #This view should return a list of all the purchases for
        #the user as determined by the username portion of the URL.
        #
        try:
           input = self.kwargs['regx']
           results_ = Biblio.objects.filter(title__iregex=input)[:3]
           #return Response(BibliosShowSerializer(title_).data)
           return results_
        except Biblio.DoesNotExist:
            return Response(
                data={
                    "message": "No biblio title with given regular expression: {} exists".format(kwargs["input"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
#TEXTO = sys.argv[1]
#my_regex = r"\b(?=\w)" + re.escape(TEXTO) + r"\b(?!\w)"
#if re.search(my_regex, subject, re.IGNORECASE):
#Model.objects.filter(adv_images__regex=r'^\d+')[:3]
class ListCreateBibliosView(generics.ListCreateAPIView):
    
    #GET biblios/
    #POST biblios/
    
    queryset = Biblio.objects.all()
    serializer_class = BibliosSerializer
    permission_classes = (permissions.IsAdminUser,)
    def get(self, request, *args, **kwargs):
        biblios_ = Biblio.objects.all()
        if not biblios_ is None:
           serializer = BibliosShowSerializer(biblios_[:2], many=True)
           return Response(
                  data=serializer.data,
                  #status=status.HTTP_201_CREATED
           )
                   
    
        else:
            return Response(
                data={
                    "message": "No biblio records exist in the database"
                },
                status=status.HTTP_404_NOT_FOUND
            )
    @validate_request_data_biblio
    def post(self, request, *args, **kwargs):
        data = {} 
        
        title = request.data.get("title")
        if title:
            title=title.strip()
            title = re.sub(' +',' ',title)
            data["title"]=title
        edition = request.data.get("edition")
        if edition:
            edition=edition.strip()
            edition = re.sub(' +',' ',edition)
            data["edition"]=edition
        
        pages = request.data.get("pages")
        if pages:
            pages=pages.strip()
            pages = re.sub(' +',' ',pages)
            if len(pages)>0:
                if not re.search(r'(\sp\.$)',pages,re.M|re.I):
                    data["pages"]=pages + " p."
                else:
                    data["pages"]=pages  
        size = request.data.get("size")
        if size:
            size=size.strip()
            size = re.sub(' +',' ',size)
            if len(size)>0:
                if not re.search(r'(\scm$)',size, re.M|re.I):
                    data["size"]=size + " cm"
                else:
                    data["size"]=size    
            
        language = request.data.get("language")
        if language:
            language_ = Language.objects.get(pk=int(language))
            if language_:
                data["language"]=language_.id  
        
        corporateauthor = request.data.get("corporateauthor")
        if corporateauthor:
            corpauthor_ = CorporateAuthor.objects.get(pk=int(corporateauthor))
            if corpauthor_:
                data["corporateauthor"]=corpauthor_.id  
        publishercode = request.data.get("publisher")
        if publishercode:
            pubcode_ = Publisher.objects.get(pk=int(publishercode))
            if pubcode_:
                data["publisher"]=pubcode_.id
        copyrightdate = request.data.get("copyrightdate") 
        if copyrightdate:   
            data["copyrightdate"]=copyrightdate
        isbn = request.data.get("isbn")
        if isbn:
            isbn = isbn.upper()   
            data["isbn"]=isbn
        
        series = request.data.get("series")
        if series:
            series=series.strip()
            series=re.sub(' +',' ',series)
            data["series"]=series
        callnumber = request.data.get("callnumber")
        if callnumber:
            callnumber=callnumber.strip()
            callnumber=re.sub(' +',' ',callnumber)
            data["callnumber"]=callnumber
        volume = request.data.get("volume")  
        if volume:
            volume=volume.strip()
            volume=re.sub(' +',' ',volume)
            data["volume"]=volume
        contents_url = request.data.get("contents_url")
        if contents_url:
            contents_url=contents_url.strip()
            contents_url=re.sub(' +',' ',contents_url)
            data["contents_url"]=contents_url
        index_url = request.data.get("index_url")
        if index_url:
            index_url=index_url.strip()
            index_url=re.sub(' +',' ',index_url)
            data["index_url"]=index_url 
        authors = request.data.get("authors")
        authors_ = []
        if len(authors)>0:
            for author in authors:
                author=author.strip()
                authors_.append(Authors.objects.get(pk=int(author)).id)
            data["authors"]=authors_
        
        genre = request.data.get("genre")
        genres_ = []
        if len(genre)>0:
            for genre_ in genre:
                genre_=genre_.strip()
                genres_.append(Genre.objects.get(pk=int(genre_)).id)
            data["genre"]=genres_
        
        serializer = BibliosSerializer(data=data)
        if serializer.is_valid(): 
           serializer.save()
           serializer = BibliosShowSerializer(data=data)
           return Response(
              data=serializer.data,
              status=status.HTTP_201_CREATED
           )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BiblioDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET biblio/:id/
    PUT biblio/:id/
    DELETE biblio/:id/
    """
    queryset = Biblio.objects.all()
    serializer_class = BibliosSerializer
    permission_classes = (permissions.IsAdminUser,)
    #permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, *args, **kwargs):
        try:
            a_biblio = self.queryset.get(pk=kwargs["pk"])
            return Response(BibliosShowSerializer(a_biblio).data)
        except Biblio.DoesNotExist:
            return Response(
                data={
                    "message": "Biblio with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data_biblio
    def put(self, request, *args, **kwargs):

      try:
        a_biblio = self.queryset.get(pk=kwargs["pk"])
        data = {}
        authors = request.data.get("authors")
        if isinstance(authors,'list'):
           data["authors"]=authors
        title = request.data.get("title")
        title = request.data.get("title")
        if title:
            title=title.strip()
            title = re.sub(' +',' ',title)
            data["title"]=title
        edition = request.data.get("edition")
        if edition:
            edition=edition.strip()
            edition = re.sub(' +',' ',edition)
            data["edition"]=edition
        
        pages = request.data.get("pages")
        if pages:
            pages=pages.strip()
            pages = re.sub(' +',' ',pages)
            if len(pages)>0:
                if not re.search(r'(\sp\.$)',pages,re.M|re.I):
                    data["pages"]=pages + " p."
                else:
                    data["pages"]=pages  
        size = request.data.get("size")
        if size:
            size=size.strip()
            size = re.sub(' +',' ',size)
            if len(size)>0:
                if not re.search(r'(\scm$)',size, re.M|re.I):
                    data["size"]=size + " cm"
                else:
                    data["size"]=size    
            
        language = request.data.get("language")
        if language:
            language_ = Language.objects.get(pk=int(language))
            if language_:
                data["language"]=language_.id  
        
        corporateauthor = request.data.get("corporateauthor")
        if corporateauthor:
            corpauthor_ = CorporateAuthor.objects.get(pk=int(corporateauthor))
            if corpauthor_:
                data["corporateauthor"]=corpauthor_.id  
        publishercode = request.data.get("publisher")
        if publishercode:
            pubcode_ = Publisher.objects.get(pk=int(publishercode))
            if pubcode_:
                data["publisher"]=pubcode_.id
        copyrightdate = request.data.get("copyrightdate") 
        if copyrightdate:   
            data["copyrightdate"]=copyrightdate
        isbn = request.data.get("isbn")
        if isbn:
            isbn = isbn.upper()   
            data["isbn"]=isbn
        
        series = request.data.get("series")
        if series:
            series=series.strip()
            series=re.sub(' +',' ',series)
            data["series"]=series
        callnumber = request.data.get("callnumber")
        if callnumber:
            callnumber=callnumber.strip()
            callnumber=re.sub(' +',' ',callnumber)
            data["callnumber"]=callnumber
        volume = request.data.get("volume")  
        if volume:
            volume=volume.strip()
            volume=re.sub(' +',' ',volume)
            data["volume"]=volume
        contents_url = request.data.get("contents_url")
        if contents_url:
            contents_url=contents_url.strip()
            contents_url=re.sub(' +',' ',contents_url)
            data["contents_url"]=contents_url
        index_url = request.data.get("index_url")
        if index_url:
            index_url=index_url.strip()
            index_url=re.sub(' +',' ',index_url)
            data["index_url"]=index_url 
        authors = request.data.get("authors")
        authors_ = []
        if len(authors)>0:
            for author in authors:
                author=author.strip()
                authors_.append(Authors.objects.get(pk=int(author)).id)
            data["authors"]=authors_
        
        genre = request.data.get("genre")
        genres_ = []
        if len(genre)>0:
            for genre_ in genre:
                genre_=genre_.strip()
                genres_.append(Genre.objects.get(pk=int(genre_)).id)
            data["genre"]=genres_
        serializer = BibliosSerializer()                       
        updated_biblio = serializer.update(a_biblio, data)
        return Response(BibliosShowSerializer(updated_suggestion).data)
      except Biblio.DoesNotExist:
            return Response(
                data={
                    "message": "Biblio with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_biblio = self.queryset.get(pk=kwargs["pk"])
            a_biblio.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Biblio.DoesNotExist:
            return Response(
                data={
                    "message": "Biblio with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )



class GenreByNameListView(generics.ListAPIView):
    #GET genres/byName/<str:name>
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAdminUser,)

    def get_queryset(self):
        #
        #This view should return a list of all the purchases for
        #the user as determined by the username portion of the URL.
        #
        try:
           name = self.kwargs['name']
           name_ = self.queryset.filter(name__icontains=name)
           #return Response(GenreSerializer(name_).data)
           return name_
        except Genre.DoesNotExist:
            return Response(
                data={
                    "message": "No genre with name: {} exists".format(kwargs["name"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

class ListCreateGenreView(generics.ListCreateAPIView):
    
    #GET genres/
    #POST genres/
    
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAdminUser,)
    def post(self, request, *args, **kwargs):
        data = {} 
        
        name = request.data.get("name")
        if name:
            name=name.strip()
            name = re.sub(' +',' ',name)
            data["name"]=name
        
        serializer = GenreSerializer(data=data)
        if serializer.is_valid(): 
           serializer.save()
           return Response(
              data=serializer.data,
              status=status.HTTP_201_CREATED
           )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET genre/:id/
    PUT genre/:id/
    DELETE genre/:id/
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (permissions.IsAdminUser,)
 
    def get(self, request, *args, **kwargs):
        try:
            a_genre = self.queryset.get(pk=kwargs["pk"])
            return Response(GenreSerializer(a_genre).data)
        except Genre.DoesNotExist:
            return Response(
                data={
                    "message": "Genre with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, *args, **kwargs):
        try:
            a_genre = self.queryset.get(pk=kwargs["pk"])
            serializer = GenreSerializer()
            genre_name = request.data.get("name")
            data = {}
            if len(genre_name)>0:
               genre_name=genre_name.strip()
               genre_name=re.sub(' +',' ',genre_name)
               data["name"]=genre
            updated_genre = serializer.update(a_genre, data)
            return Response(GenreSerializer(updated_genre).data)
        except Genre.DoesNotExist:
            return Response(
                data={
                    "message": "Genre with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_genre = self.queryset.get(pk=kwargs["pk"])
            a_genre.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Genre.DoesNotExist:
            return Response(
                data={
                    "message": "Genre with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from .decorators import validate_request_data_borrowers
from .decorators import validate_request_data_patronphotos
from intranet.models import Borrowers, PatronPhotos
from .serializers import BorrowersSerializer, PatronPhotosSerializer, PatronPhotosShowSerializer
import re
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import JSONParser

class ListCreateBorrowersView(generics.ListCreateAPIView):
    """
    GET borrowers/
    POST borrowers/
    """
    queryset = Borrowers.objects.all()
    serializer_class = BorrowersSerializer
    permission_classes = (permissions.IsAdminUser,)
         
    @validate_request_data_borrowers
    def post(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
           data = [request.data]
        else:
           data = request.data
        for patron in data:
           patron["firstname"].strip()
           patron["surname"].strip()
           re.sub(' +', ' ',patron["firstname"])
           re.sub(' +', ' ',patron["surname"])
           patron["email"].strip()
           re.sub(' +', ' ',patron["email"])
           patron["cardnumber"].strip()
           re.sub(' +', ' ',patron["cardnumber"])
           re.sub('[a-z]','[A-Z]',patron["cardnumber"])
                 
             
        serializer = BorrowersSerializer(data=data, many=True)
        if serializer.is_valid(): 
           serializer.save()
           return Response(
              data=serializer.data,
              status=status.HTTP_201_CREATED
           )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BorrowerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET borrower/:id/
    PUT borrower/:id/
    DELETE borrower/:id/
    """
    queryset = Borrowers.objects.all()
    serializer_class = BorrowersSerializer
    permission_classes = (permissions.IsAdminUser,)
 
    def get(self, request, *args, **kwargs):
        try:
            a_patron = self.queryset.get(pk=kwargs["pk"])
            return Response(BorrowersSerializer(a_patron).data)
        except Borrowers.DoesNotExist:
            return Response(
                data={
                    "message": "Borrower with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data_borrowers
    def put(self, request, *args, **kwargs):
        try:
            a_patron = self.queryset.get(pk=kwargs["pk"])
            serializer = BorrowersSerializer()
            request.data["firstname"].strip()
            request.data["surname"].strip()
            re.sub(' +', ' ',request.data["firstname"])
            re.sub(' +', ' ',request.data["surname"])
            patron["email"].strip()
            re.sub(' +', ' ',patron["email"])
            patron["cardnumber"].strip()
            re.sub(' +', ' ',patron["cardnumber"])
            re.sub('[a-z]','[A-Z]',patron["cardnumber"])
           
            updated_patron = serializer.update(a_patron, request.data)
            return Response(BorrowersSerializer(updated_patron).data)
        except Borrowers.DoesNotExist:
            return Response(
                data={
                    "message": "Borrower with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            return Response(
                data={
                    "message": "Invalid operation: Change of Borrower not allowed",
                },
                status=status.HTTP_404_NOT_FOUND
            ) 

    def delete(self, request, *args, **kwargs):
        try:
            a_patron = self.queryset.get(pk=kwargs["pk"])
            a_patron.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Borrowers.DoesNotExist:
            return Response(
                data={
                    "message": "Borrower with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )



import os
import tempfile
import magic

def check_in_memory_mime(in_memory_file):
    mime = magic.from_buffer(in_memory_file.read(), mime=True)
    return mime

class ImageUploadParser(FileUploadParser):
    media_type = 'image/*'

class ListCreatePatronPhotosView(generics.ListCreateAPIView):
    """
    GET patronphotos/
    POST patronphotos/
    """
    queryset = PatronPhotos.objects.all()
    serializer_class = PatronPhotosSerializer
    #parser_classes = (JSONParser,)
    parser_class = (ImageUploadParser,)
    permission_classes = (permissions.IsAdminUser,)
    def get(self, request, *args, **kwargs):
        photos_ = PatronPhotos.objects.all()
        if not photos_ is None:
           serializer = PatronPhotosShowSerializer(photos_, many=True)
           return Response(
                  data=serializer.data,
           )
        else:
            return Response(
                data={
                    "message": "No photos exist in the database"
                },
                status=status.HTTP_404_NOT_FOUND
            )
     
    @validate_request_data_patronphotos
    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PatronPhotosSerializer(data=data)
        if serializer.is_valid(): 
           serializer.save()
           return Response(
                  data=serializer.data,
                  status=status.HTTP_201_CREATED
           )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatronPhotosDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET patronphoto/:id/
    PUT patronphoto/:id/
    DELETE patronphoto/:id/
    """
    queryset = PatronPhotos.objects.all()
    serializer_class = PatronPhotosSerializer
    parser_class = (ImageUploadParser,)
    #parser_classes = (JSONParser,)
    permission_classes = (permissions.IsAdminUser,)
 
    def get(self, request, *args, **kwargs):
        try:
            a_patronphoto = self.queryset.get(pk=kwargs["pk"])
            return Response(PatronPhotosShowSerializer(a_patronphoto).data)
        except PatronPhotos.DoesNotExist:
            return Response(
                data={
                    "message": "Patron Photo with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    @validate_request_data_patronphotos
    def put(self, request, *args, **kwargs):
        try:
            a_patronphoto = self.queryset.get(pk=kwargs["pk"])
            serializer = PatronPhotosSerializer()
            updated_patronphoto = serializer.update(a_patronphoto, request.data)
            return Response(PatronPhotosSerializer(updated_patronphoto).data)
        except PatronPhotos.DoesNotExist:
            return Response(
                data={
                    "message": "No photo with that id: {} exists:.".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, *args, **kwargs):
        try:
            a_patronphoto = self.queryset.get(pk=kwargs["pk"])
            a_patronphoto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except PatronPhotos.DoesNotExist:
            return Response(
                data={
                    "message": "Patron photo with id: {} does not exist".format(kwargs["pk"])
                },
                status=status.HTTP_404_NOT_FOUND
            )


