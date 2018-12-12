# feeds.py
from django.contrib.syndication.views import Feed
from django.urls import reverse
from ils_app.models import Biblio


class LatestBibliosFeed(Feed):
   title = "ILS Biblio Feeds"
   link = "/biblio_feeds/"
   description = "Updates on changes and additions to titles acquired in the library."
   def items(self):
       return Biblio.objects.order_by('-timestamp_added')[:5]

   def item_title(self, item):
       return item.title

   def item_description(self, item):
       return item.first_author

   def item_link(self, item):
       return reverse('biblio_detail', kwargs={'biblionumber':item.pk})
       #return item.get_absolute_url()

class LatestBiblioDetailFeed(Feed):
   def items(self):
       return Biblio.objects.get(pk=Feed.item.pk)
