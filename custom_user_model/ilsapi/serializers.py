from rest_framework import serializers
#from django.contrib.auth.models import User
from accounts.models import User
from intranet.models import Authors, Suggestion, Publisher, Biblio, Genre

from rest_framework.reverse import reverse

class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ("id","firstname", "lastname")

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.lastname = validated_data.get("lastname", instance.lastname)
        instance.save()
        return instance

class PublishersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ("id","name")

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

class SuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("suggestionid","suggestedby","suggesteddate","acceptedby",
            "accepteddate","rejectedby","rejecteddate","status","note","author","title","copyrightdate",
            "publishercode","isbn","reason","price","total",
        )

    def update(self, instance, validated_data):
        instance.suggestedby = validated_data.get("suggestedby", instance.suggestedby)
        instance.suggesteddate = validated_data.get("suggesteddate", instance.suggesteddate)
        instance.acceptedby = validated_data.get("acceptedby", instance.acceptedby)
        instance.accepteddate = validated_data.get("accepteddate", instance.accepteddate)
        instance.rejectedby = validated_data.get("rejectedby", instance.rejectedby)
        instance.rejecteddate = validated_data.get("rejecteddate", instance.rejecteddate)
        instance.status = validated_data.get("status", instance.status)
        instance.note = validated_data.get("note", instance.note)
        instance.author = validated_data.get("author", instance.author)
        instance.title = validated_data.get("title", instance.title)
        instance.copyrightdate = validated_data.get("copyrightdate", instance.copyrightdate)
        instance.publishercode = validated_data.get("publishercode", instance.publishercode)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        instance.reason = validated_data.get("reason", instance.reason)
        instance.price = validated_data.get("price", instance.price)
        instance.total = validated_data.get("total", instance.total)
        instance.save()
        return instance

class SuggestionsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("suggestionid","suggestedby","note","author","title","copyrightdate",
            "publishercode","isbn","price","total",
        )

    def update(self, instance, validated_data):
        instance.suggestedby = validated_data.get("suggestedby", instance.suggestedby)
        instance.suggesteddate = validated_data.get("suggesteddate", instance.suggesteddate)
        instance.acceptedby = validated_data.get("acceptedby", instance.acceptedby)
        instance.accepteddate = validated_data.get("accepteddate", instance.accepteddate)
        instance.rejectedby = validated_data.get("rejectedby", instance.rejectedby)
        instance.rejecteddate = validated_data.get("rejecteddate", instance.rejecteddate)
        instance.status = validated_data.get("status", instance.status)
        instance.note = validated_data.get("note", instance.note)
        instance.author = validated_data.get("author", instance.author)
        instance.title = validated_data.get("title", instance.title)
        instance.copyrightdate = validated_data.get("copyrightdate", instance.copyrightdate)
        instance.publishercode = validated_data.get("publishercode", instance.publishercode)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        instance.reason = validated_data.get("reason", instance.reason)
        instance.price = validated_data.get("price", instance.price)
        instance.total = validated_data.get("total", instance.total)
        instance.save()
        return instance

class SuggestionsPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("suggestionid","suggestedby","status","note","author","title","copyrightdate",
            "publishercode","isbn","reason","price","total",
        )
        read_only_fields = ('suggestedby',)
    def update(self, instance, validated_data):
        #instance.suggestedby = validated_data.get("suggestedby", instance.suggestedby)
        instance.suggestedby=instance.suggestedby
        instance.suggesteddate = validated_data.get("suggesteddate", instance.suggesteddate)
        instance.acceptedby = validated_data.get("acceptedby", instance.acceptedby)
        instance.accepteddate = validated_data.get("accepteddate", instance.accepteddate)
        instance.rejectedby = validated_data.get("rejectedby", instance.rejectedby)
        instance.rejecteddate = validated_data.get("rejecteddate", instance.rejecteddate)
        instance.status = validated_data.get("status", instance.status)
        instance.note = validated_data.get("note", instance.note)
        instance.author = validated_data.get("author", instance.author)
        #instance.title = validated_data.get("title", instance.title)
        instance.title = instance.title
        instance.copyrightdate = validated_data.get("copyrightdate", instance.copyrightdate)
        instance.publishercode = validated_data.get("publishercode", instance.publishercode)
        instance.isbn = validated_data.get("isbn", instance.isbn)
        instance.reason = validated_data.get("reason", instance.reason)
        instance.price = validated_data.get("price", instance.price)
        instance.total = validated_data.get("total", instance.total)
        instance.save()
        return instance

class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email","fullname")


class SuggestionsByOwnerIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ("suggestionid","suggestedby","suggesteddate","acceptedby",
            "accepteddate","rejectedby","rejecteddate","status","note","author","title","copyrightdate",
            "publishercode","isbn","reason","price","total",
        )

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id","name")

class GenreHyperlink(serializers.HyperlinkedRelatedField):
    # We define these as class attributes, so we don't need to pass them as arguments.
    view_name = 'GenreDetailView'
    queryset = Genre.objects.all()

    def get_url(self, obj, view_name, request, format):
        url_kwargs = {
            #'genre_slug': obj.name,
            'pk': obj.pk
        }
        return reverse(view_name, kwargs=url_kwargs, request=request, format=format)

    def get_object(self, view_name, view_args, view_kwargs):
        lookup_kwargs = {
           #'genre__name': view_kwargs['genre_slug'],
           'pk': view_kwargs['pk']
        }
        return self.get_queryset().get(**lookup_kwargs)
        
class BibliosSerializer(serializers.ModelSerializer):
    #genre = GenreHyperlink()
    class Meta:
        model = Biblio
        fields = ('biblionumber','itemtype','isbn',  'callnumber',  'title', 'edition', 'copyrightdate',
             'series','volume','pages','size', 'contents_url','index_url', 'biblionumber',
             'language','authors','corporateauthor','publisher','genre'
        )

class BibliosShowSerializer(serializers.ModelSerializer):
    #genre = GenreHyperlink()
    genre =  GenreSerializer(many=True,read_only=True)
    authors =  AuthorsSerializer(many=True,read_only=True)
    publisher =  PublishersSerializer(read_only=True)
    language = serializers.StringRelatedField(many=False)
    corporateauthor = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )
    url = serializers.HyperlinkedRelatedField(many=False,view_name='biblionumber',read_only=True) 
    class Meta:
        model = Biblio
        fields = ('url','itemtype','isbn',  'callnumber', 'title', 'edition', 'copyrightdate',
             'series','volume','pages','size', 'contents_url','index_url', 'biblionumber',
             'language','authors','corporateauthor','publisher','genre'
        )


from intranet.models import PatronPhotos, Borrowers  

class BorrowersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    debarred = serializers.DateField(required=False)
    dateexpiry = serializers.DateField()
    class Meta:
        model = Borrowers
        fields = ("id","borrower","email","cardnumber","firstname", "surname","mobile","dateexpiry",
           'gonenoaddress','lost','debarred','debarredcomment','category','department','designation',
           'borrowernote','opacnote')

class PatronPhotosSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatronPhotos
        fields = ("id","patron", "imageurl")

    def update(self, instance, validated_data):
        instance.imageurl = validated_data.get("imageurl", instance.imageurl)
        patron_ = validated_data.get("patron")
        if patron_ and not instance.patron:
           patron  = Borrowers.objects.get(pk=patron_)
           if patron:
              instance.patron = patron
        instance.save()
        return instance

class PatronPhotosShowSerializer(serializers.ModelSerializer):
    patron =  BorrowersSerializer(read_only=True)
    class Meta:
        model = PatronPhotos
        fields = ('id','patron','imageurl')
