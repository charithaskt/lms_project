from django.urls import path, include
from .views import ListCreateAuthorsView, AuthorsDetailView, LoginView
from .views import ListCreatePublishersView, PublishersDetailView
from .views import ListCreateSuggestionsView, SuggestionsDetailView
from .views import ListCreateMySuggestionsView, MySuggestionsDetailView
from .views import ListCreateBibliosView, BiblioDetailView
from .views import SuggestionsByOwnerIdListView
from .views import SuggestionsByOwnerCardnumberListView
from .views import SuggestionsByOwnerEmailListView
from .views import GenreByNameListView, ListCreateGenreView, GenreDetailView, BibliosByTitleRegxListView
from .views import BibliosByTitleListView, BibliosByRangeListView
#from rest_framework_jwt.views import obtain_jwt_token
#from custom_user_model.settings import JWTAUTH


#from .views import  RegisterUsers
from ilsapi import views as api_views
urlpatterns = [
    path('authors/', ListCreateAuthorsView.as_view(), name="authors-list-create"),
    path('author/<int:pk>/', AuthorsDetailView.as_view(), name="author-detail"),
    path('genres/', ListCreateGenreView.as_view(), name="genre-list-create"),
    path('genre/<int:pk>/', GenreDetailView.as_view(), name="genre-detail"),
    path('genres/byname/<str:name>/', GenreByNameListView.as_view(), name="genre-byname"),
    path('publishers/', ListCreatePublishersView.as_view(), name="publishers-list-create"),
    path('publisher/<int:pk>/', PublishersDetailView.as_view(), name="publisher-detail"),
    path('biblios/', ListCreateBibliosView.as_view(), name="biblios-list-create"),
    path('biblios/bytitle/<str:title>/', BibliosByTitleListView.as_view(), name="biblios-bytitle-list"),
    path('biblios/bytitleregx/<str:regx>/', BibliosByTitleRegxListView.as_view(), name="biblios-bytitleregx-list"),
    path('biblios/byrange/<str:begin>/', BibliosByRangeListView.as_view(), name="biblios-bytitle-list"),
    path('biblio/<int:pk>/', BiblioDetailView.as_view(), name="biblios-detail"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    #path('auth/register/', RegisterUsers.as_view(), name="auth-register")
    #path('suggestions/', ListCreateSuggestionsView.as_view(), name="suggestions-list-create"),
    path('suggestions/', ListCreateMySuggestionsView.as_view(), name="mysuggestions-list-create"),
    #path('suggestion/<int:pk>/', SuggestionsDetailView.as_view(), name="suggestion-detail"),
    path('suggestion/<int:pk>/', MySuggestionsDetailView.as_view(), name="mysuggestion-detail"),
    path('suggestions/byownerid/<int:ownerid>/', SuggestionsByOwnerIdListView.as_view(), name="suggestions-byownerid"),
    path('suggestions/byownercardnumber/<str:cardnumber>/', SuggestionsByOwnerCardnumberListView.as_view(), name="suggestions-byownercardnumber"),
    path('suggestions/byowneremailid/<str:email>/', SuggestionsByOwnerEmailListView.as_view(), name="suggestions-byowneremail"),
    #--------
    path('borrowers/',api_views.ListCreateBorrowersView.as_view(), name="borrowerss-list-create"),
    path('borrower/<int:pk>/',api_views.BorrowerDetailView.as_view(), name="borrower-detail"),
    path('patronphotos/',api_views.ListCreatePatronPhotosView.as_view(), name="patronsphotos-list-create"),
    path('patronphoto/<int:pk>/',api_views.PatronPhotosDetailView.as_view(), name="patronphoto-detail"),


]

'''
if JWTAUTH:
   urlpatterns +=  [path('api-token-auth/', obtain_jwt_token, name='create-token'),]
else:
   #urlpatterns +=  [path('api-auth/', include('rest_auth.urls'))]
   urlpatterns +=  [path('api-auth/', include('rest_framework.urls'))]

'''
