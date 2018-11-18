from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Departments, Designations, Borrowers, Categories
from .models import SystemPreferences,PatronImages,Biblio,BiblioImages,Items,Suggestions
from .models import Issues, Reserves, AccountLines, AccountOffsets, Statistics, Genre, Language
from .models import Publisher,  Authors, CorporateAuthor,Holidays, ActionLogs, EntryExitLogs, ModeratorReasons
from .models import Quotations, News, Stopwords, SearchHistory, IssuingRules, RentalCharges, CollectionDepartments
from .models import Tags, Comments, Suggestion, PatronPhotos 
 
admin.site.register(SystemPreferences)
admin.site.register(Departments)
admin.site.register(CollectionDepartments)
admin.site.register(Designations)
admin.site.register(Categories)
admin.site.register(Borrowers)
admin.site.register(PatronImages)

@admin.register(Items) 
class ItemsAdmin(admin.ModelAdmin):
     list_display = ('itemnumber','barcode','biblionumber','itemstatus','booksellerid','price','notforloan','collectiondepartment','totalissues')
     list_filter = ('itemstatus', 'notforloan','booksellerid','location','collectiondepartment')
     fieldsets = (
        ('Item', {
            'fields': ('biblionumber', 'replacementprice','totalissues')
        }),
        ('Availability', {
            'fields': ('itemstatus', 'notforloan', 'location', 'collectiondepartment')
        }),
        ('Acquisition', {
            'fields': ('dateaccessioned', 'barcode','booksellerid','invoicenumber','invoicedate','price')
        }),
    )

class ItemsInline(admin.TabularInline):
    model = Items

@admin.register(Biblio)
class BiblioAdmin(admin.ModelAdmin):
    list_display = ('itemtype','title', 'display_authors', 'copyrightdate','edition','publisher','display_genre')
    list_filter = ('itemtype','authors', 'publisher','copyrightdate','genre')
    fieldsets = (
        ('Title', {
            'fields': ('title','itemtype','authors', 'edition','genre','corporateauthor','totalissues')
        }),
        ('Imprint', {
            'fields': ('publisher', 'copyrightdate','isbn','language','series','volume')
        }),
        ('Colletion', {
            'fields': ('pages', 'size','callnumber')
        }),
        ('Urls', {
            'fields': ('contents_url', 'index_url')
        }),
    )

    inlines = [ItemsInline]

    def display_genre(self, *args):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in args[0].genre.all()[:3])

    def display_authors(self, *args):
        """Create a string for the Authors. This is required to display authors in Admin."""
        return ', '.join(author.name for author in args[0].authors.all()[:3])
    
#admin.site.register(Biblio)

admin.site.register(BiblioImages)
#admin.site.register(Items)
admin.site.register(Suggestions)
admin.site.register(Issues)
admin.site.register(Reserves)
admin.site.register(AccountLines)
admin.site.register(AccountOffsets)
admin.site.register(Statistics)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Publisher)
admin.site.register(Authors)
admin.site.register(CorporateAuthor)
admin.site.register(Holidays)
admin.site.register(ActionLogs)
admin.site.register(EntryExitLogs)
admin.site.register(ModeratorReasons)
admin.site.register(Stopwords)
admin.site.register(News)
admin.site.register(Quotations)
admin.site.register(SearchHistory)
admin.site.register(RentalCharges)
admin.site.register(IssuingRules)
admin.site.register(Tags)
admin.site.register(Comments)
admin.site.register(Suggestion)
admin.site.register(PatronPhotos)

