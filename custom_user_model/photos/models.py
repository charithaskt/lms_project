from __future__ import unicode_literals

from django.db import models
from intranet.models import Borrowers

class PatronBulkPhotos(models.Model):
    patron_id = models.ForeignKey(Borrowers, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='patron_bulk_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
      return self.patron_id.cardnumber

