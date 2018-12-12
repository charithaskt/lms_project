from django.urls import path, re_path
from opac import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.home, name='home'),
    path('author/add/', views.AuthorCreate.as_view(), name='author-add'),
    path('books/', views.BookListView.as_view(), name='books'),
    #path('book/<uuid:pk>', views.BookDetailView.as_view(), name='book-detail'),
    re_path(r'^book/(?P<pk>\d+)/$', views.book_detail_view, name='biblio-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)/$', views.AuthorDetailView.as_view(), name='authors-detail'),
    path('search/',views.catalog_search, name="catalog-search"),
    path('quote/add/', views.QuoteCreate.as_view(), name='quote-add'),
    path('quotes/', views.QuotesListView.as_view(), name='quotes'),
    re_path(r'^quote/(?P<pk>\d+)/$', views.QuoteDetailView.as_view(), name='quote-detail'),
    path('entryexitlogs/add/', csrf_exempt(views.EntryExitLogCreate.as_view()), name='entryexitlogs-add'),
    path('entryexitlogs/', views.EntryExitLogsListView.as_view(), name='entryexitlogs-list'),
    re_path(r'^entryexitlog/(?P<pk>\d+)/$', views.EntryExitLogDetailView.as_view(), name='entryexitlog-detail'),
    path('search_visitors/',views.entryexitlog_search, name="entryexitlog-search"),
]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('issued_books/', views.IssuedBooksListView.as_view(), name='issued-books'),
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
urlpatterns += [   
    path('issue/', views.issue_item_librarian_init, name='issue-item-librarian-init'),
]
urlpatterns += [   
    re_path(r'processissue/(?P<borrower_pk>\d+),(?P<item_pk>\d+),(?P<held_self>(True|False)),(?P<renewal>(True|False)),(?P<loan_length>\d+)$', views.issue_item_librarian, name='issue-item-librarian'),
]
urlpatterns += [   
    path('collect_fine/', views.fine_collect_librarian_init, name='fine-collect-librarian-init'),
]
urlpatterns += [   
    re_path(r'processfine/(?P<borrower_pk>\d+),(?P<account_pk>\d+),(?P<fine>\d+\.?\d+)$', views.fine_collect_librarian, name='fine-collect-librarian'),
]
