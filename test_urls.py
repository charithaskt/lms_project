from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.test import TestCase
from django.urls import reverse,resolve
from django.views.generic import TemplateView

from accounts.views import signup, account_activation_sent, activate, edit_user, profiles_list, profile_detail
from idapp.views import index
from ilsapi.views import ListCreateAuthorsView, AuthorsDetailView, ListCreateGenreView, GenreDetailView, \
    GenreByNameListView, ListCreatePublishersView, PublishersDetailView, ListCreateBibliosView, BibliosByTitleListView, \
    BibliosByTitleRegxListView, BibliosByRangeListView, BiblioDetailView, ListCreateMySuggestionsView, \
    MySuggestionsDetailView, SuggestionsByOwnerIdListView, SuggestionsByOwnerCardnumberListView, \
    SuggestionsByOwnerEmailListView, ListCreateBorrowersView, PatronPhotosDetailView, BorrowerDetailView, \
    ListCreatePatronPhotosView
from opac.views import AuthorCreate, BookListView, book_detail_view, AuthorListView, AuthorDetailView, \
    LoanedBooksByUserListView, renew_book_self, renew_book_librarian_init, renew_book_librarian, \
    return_book_librarian_init
from photos.views import clear_database, delete_patron_photo, ProgressBarUploadView, DragAndDropUploadView


class Testurls(TestCase):
    def test_auth_add_resolved(self):
        url=reverse('author-add')
        self.assertEqual(resolve(url).func, AuthorCreate)

    def test_index_resolved(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_books_resolved(self):
        url = reverse('books')
        self.assertEqual(resolve(url).func, BookListView)

    def test_biblio_detail_resolved(self):
        url = reverse('biblio-detail',args=['some-number'])
        self.assertEqual(resolve(url).func, book_detail_view)


    def test_clear_database_resolved(self):
        url = reverse('clear_database')
        self.assertEqual(resolve(url).func, clear_database)

    def test_delete_patron_photo_resolved(self):
        url = reverse('delete_patron_photo',args=['some-number'])
        self.assertEqual(resolve(url).func, delete_patron_photo)

    def test_progress_bar_upload_resolved(self):
        url = reverse('progress_bar_upload')
        self.assertEqual(resolve(url).func, ProgressBarUploadView)

    def test_drag_and_drop_upload_resolved(self):
        url = reverse('drag_and_drop_upload')
        self.assertEqual(resolve(url).func,DragAndDropUploadView )

    def test_barcode_resolved(self):
        url = reverse('barcode')
        self.assertEqual(resolve(url).func, index)

    def test_authors_list_create_resolved(self):
        url = reverse('authors-list-create')
        self.assertEqual(resolve(url).func, ListCreateAuthorsView)

    def test_author_detail_resolved(self):
        url = reverse('author-detail')
        self.assertEqual(resolve(url).func, AuthorsDetailView)

    def test_genre_list_create_resolved(self):
        url = reverse('genre-list-create')
        self.assertEqual(resolve(url).func, ListCreateGenreView)

    def test_genre_detail_resolved(self):
        url = reverse('genre-detail')
        self.assertEqual(resolve(url).func, GenreDetailView)

    def test_genre_byname_resolved(self):
        url = reverse('genre-byname')
        self.assertEqual(resolve(url).func, GenreByNameListView)

    def test_publishers_list_(self):
        url = reverse('publishers-list-create')
        self.assertEqual(resolve(url).func, ListCreatePublishersView)

    def test_publisher_detail_resolved(self):
        url = reverse('publisher-detail')
        self.assertEqual(resolve(url).func, PublishersDetailView)

    def test_biblios_list_create_resolved(self):
        url = reverse('biblios-list-create')
        self.assertEqual(resolve(url).func, ListCreateBibliosView)

    def test_biblios_bytitle_list_resolved(self):
        url = reverse('biblios-bytitle-list')
        self.assertEqual(resolve(url).func, BibliosByTitleListView)

    def test_biblios_bytitleregx_list_resolved(self):
        url = reverse('biblios-bytitleregx-list')
        self.assertEqual(resolve(url).func, BibliosByTitleRegxListView)

    def test_biblios_bytitle_list_resolved(self):
        url = reverse('biblios-bytitle-list')
        self.assertEqual(resolve(url).func, BibliosByRangeListView)

    def test_biblios_detail_resolved(self):
        url = reverse('biblios-detail')
        self.assertEqual(resolve(url).func, BiblioDetailView)

    def test_biblios_bytitle_list_resolved(self):
        url = reverse('auth-login')
        self.assertEqual(resolve(url).func, LoginView)

    def test_ListCreateMySuggestionsView_resolved(self):
        url = reverse('mysuggestions-list-create')
        self.assertEqual(resolve(url).func, ListCreateMySuggestionsView)

    def test_mysuggestion_detail_resolved(self):
        url = reverse('mysuggestion-detail')
        self.assertEqual(resolve(url).func,MySuggestionsDetailView )

    def test_SuggestionsByOwnerIdListView_resolved(self):
        url = reverse('suggestions-byownerid')
        self.assertEqual(resolve(url).func, SuggestionsByOwnerIdListView)

    def test_SuggestionsByOwnerCardnumberListView_resolved(self):
        url = reverse('suggestions-byownercardnumber')
        self.assertEqual(resolve(url).func, SuggestionsByOwnerCardnumberListView)

    def test_suggestions_byowneremail_resolved(self):
        url = reverse('suggestions-byowneremail')
        self.assertEqual(resolve(url).func, SuggestionsByOwnerEmailListView)

    def test_ListCreateBorrowersView_resolved(self):
        url = reverse('borrowerss-list-create')
        self.assertEqual(resolve(url).func, ListCreateBorrowersView)

    def test_BorrowerDetailView_resolved(self):
        url = reverse('borrower-detail')
        self.assertEqual(resolve(url).func, BorrowerDetailView)

    def test_ListCreatePatronPhotosView_resolved(self):
        url = reverse('patronsphotos-list-create')
        self.assertEqual(resolve(url).func,ListCreatePatronPhotosView )

    def test_PatronPhotosDetailView_resolved(self):
        url = reverse('patronphoto-detail')
        self.assertEqual(resolve(url).func,PatronPhotosDetailView )

    def test_AuthorListView_resolved(self):
        url = reverse('authors')
        self.assertEqual(resolve(url).func,AuthorListView )

    def test_AuthorDetailView_resolved(self):
        url = reverse('authors-detail')
        self.assertEqual(resolve(url).func,AuthorDetailView )

    def test_my_borrowed_resolved(self):
        url = reverse('my-borrowed')
        self.assertEqual(resolve(url).func,LoanedBooksByUserListView )

    def test_renew_book_self_resolved(self):
        url = reverse('renew-book-self')
        self.assertEqual(resolve(url).func,renew_book_self )

    def test_renew_book_librarian_init_resolved(self):
        url = reverse('renew-book-librarian-init')
        self.assertEqual(resolve(url).func,renew_book_librarian_init )

    def test_renew_book_librarian_resolved(self):
        url = reverse('renew-book-librarian')
        self.assertEqual(resolve(url).func,renew_book_librarian )

    def test_return_book_librarian_init_resolved(self):
        url = reverse('return-book-librarian')
        self.assertEqual(resolve(url).func,return_book_librarian_init )

    def test_login_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func,login)

    def test_logout_resolved(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func,logout )

    def test__resolved(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func,signup )

    def test_account_activation_sent_resolved(self):
        url = reverse('account_activation_sent')
        self.assertEqual(resolve(url).func,account_activation_sent )

    def test_activate_resolved(self):
        url = reverse('activate',args=[23,34])
        self.assertEqual(resolve(url).func,activate )

    def test_account_update_resolved(self):
        url = reverse('account_update')
        self.assertEqual(resolve(url).func, edit_user)

    def test_account_profiles_resolved(self):
        url = reverse('account_profiles')
        self.assertEqual(resolve(url).func, profiles_list )

    def test_profile_detail_resolved(self):
        url = reverse('profile_detail')
        self.assertEqual(resolve(url).func, profile_detail)

    def test__resolved(self):
        url = reverse('photos-home')
        self.assertEqual(resolve(url).func, TemplateView)




