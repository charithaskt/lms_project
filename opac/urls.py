from django.urls import path, re_path
from opac import views


urlpatterns = [
    path('', views.index, name='index'),
    path('author/add/', views.AuthorCreate.as_view(), name='author-add'),
    path('books/', views.BookListView.as_view(), name='books'),
    #path('book/<uuid:pk>', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^book/(?P<pk>\d+)$', views.book_detail_view, name='biblio-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='authors-detail'),
]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]

urlpatterns += [   
    re_path(r'selfrenew/(?P<pk>\d+)$', views.renew_book_self, name='renew-book-self'),
]
urlpatterns += [   
    path('renew/', views.renew_book_librarian_init, name='renew-book-librarian-init'),
]
urlpatterns += [   
    re_path(r'processrenew/(?P<pk>\d+),(?P<loanlength>\d+)$', views.renew_book_librarian, name='renew-book-librarian'),
]
urlpatterns += [   
    path('return/', views.return_book_librarian_init, name='return-book-librarian-init'),
]
urlpatterns += [   
    re_path(r'processreturn/(?P<pk>\d+),(?P<fineamount>\d+),(?P<overdue>[\-]?\d+)$', views.return_book_librarian, name='return-book-librarian'),
]
