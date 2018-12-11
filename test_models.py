from model_mommy import mommy
from django.urls import reverse, resolvers, resolve
from django.test import TestCase

from intranet.models import *
from photos.models import *

class TestcasesMommy(TestCase):

# models test

    def test_model_creation_mommy(self):

        new_profile = mommy.make('accounts.Profile')
        self.assertTrue(isinstance(new_profile, Profile))
        # self.assertEqual(new_profile.__str__(), new_profile.user.email)

        new_categories = mommy.make('intranet.Categories')
        self.assertTrue(isinstance(new_categories, Categories))

        new_departments = mommy.make('intranet.Departments')
        self.assertTrue(isinstance(new_departments, Departments))

        new_collectdept = mommy.make('intranet.Collection Deprtments')
        self.assertTrue(isinstance(new_collectdept, CollectionDepartments))

        new_desig = mommy.make('intranet.Designations')
        self.assertTrue(isinstance(new_desig, Designations))

        new_borrowers = mommy.make('intranet.Borrowers')
        self.assertTrue(isinstance(new_borrowers, Borrowers))

        new_patronimg = mommy.make('intranet.PatronImages')
        self.assertTrue(isinstance(new_patronimg, PatronImages))

        new_genre = mommy.make('intranet.Genre')
        self.assertTrue(isinstance(new_genre, Genre))

        new_language = mommy.make('intranet.Language')
        self.assertTrue(isinstance(new_language, Language))

        new_publisher = mommy.make('intranet.Publisher')
        self.assertTrue(isinstance(new_publisher, Publisher))

        new_corpauth = mommy.make('intranet.CorporateAuthor')
        self.assertTrue(isinstance(new_corpauth, CorporateAuthor))

        new_authors = mommy.make('intranet.Authors')
        self.assertTrue(isinstance(new_authors, Authors))

        new_biblio = mommy.make('intranet.Biblio')
        self.assertTrue(isinstance(new_biblio, Biblio))

        new_items = mommy.make('intranet.Items')
        self.assertTrue(isinstance(new_items, Items))

        new_bibimg = mommy.make('intranet.BiblioImages')
        self.assertTrue(isinstance(new_bibimg, BiblioImages))

        new_reserves = mommy.make('intranet.Reserves')
        self.assertTrue(isinstance(new_reserves, Reserves))

        new_acclines = mommy.make('intranet.AccountLines')
        self.assertTrue(isinstance(new_acclines, AccountLines))

        new_eelogs = mommy.make('intranet.EntryExitLogs')
        self.assertTrue(isinstance(new_eelogs, EntryExitLogs))

        new_acclogs = mommy.make('intranet.ActionLogs')
        self.assertTrue(isinstance(new_acclogs, ActionLogs))

        new_syspref = mommy.make('intranet.SystemPreference')
        self.assertTrue(isinstance(new_syspref, SystemPreferences))

        new_modreas = mommy.make('intranet.ModeratorReasons')
        self.assertTrue(isinstance(new_modreas, ModeratorReasons))

        new_suggests = mommy.make('intranet.Suggestions')
        self.assertTrue(isinstance(new_suggests, Suggestions))

        new_swords = mommy.make('intranet.Stopwords')
        self.assertTrue(isinstance(new_swords, Stopwords))

        new_searchist = mommy.make('intranet.SearchHistory')
        self.assertTrue(isinstance(new_searchist, SearchHistory))

        new_quotations = mommy.make('intranet.Quotations')
        self.assertTrue(isinstance(new_quotations, Quotations))

        new_news = mommy.make('intranet.News')
        self.assertTrue(isinstance(new_news, News))

        new_rentcharges = mommy.make('intranet.RentalCharges')
        self.assertTrue(isinstance(new_rentcharges, RentalCharges))

        new_tags = mommy.make('intranet.Categories')
        self.assertTrue(isinstance(new_tags, Tags))

        new_comments = mommy.make('intranet.Comments')
        self.assertTrue(isinstance(new_comments, Comments))

        new_issuingrules = mommy.make('intranet.Categories')
        self.assertTrue(isinstance(new_issuingrules, IssuingRules))

        new_issues = mommy.make('intranet.Issues')
        self.assertTrue(isinstance(new_issues, Issues))

        new_stats = mommy.make('intranet.Statistics')
        self.assertTrue(isinstance(new_stats, Statistics))

        new_accoff = mommy.make('intranet.AccountOffsets')
        self.assertTrue(isinstance(new_accoff, AccountOffsets))

        new_hols = mommy.make('intranet.Holidays')
        self.assertTrue(isinstance(new_hols, Holidays))

        new_suggest = mommy.make('intranet.Suggestion')
        self.assertTrue(isinstance(new_suggest, Suggestion))

        new_patphoto = mommy.make('intranet.PatronPhotos')
        self.assertTrue(isinstance(new_patphoto, PatronPhotos))

        new_patbulk = mommy.make('intranet.PatronBulkPhotos')
        self.assertTrue(isinstance(new_patbulk, PatronBulkPhotos))