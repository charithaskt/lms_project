import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .forms import PatronPhotoForm
from .models import PatronBulkPhotos
from intranet.models import Borrowers
import os
import re
class BasicUploadView(View):
    def get(self, request):
        photos_list = PatronBulkPhotos.objects.all()
        return render(self.request, 'photos/basic_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PatronPhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            base = os.path.basename(photo.file.url)
            cardnumber = (os.path.splitext(base)[0]).upper()
            instance = None
            try:
               instance = PatronBulkPhotos.objects.get(patron_id=None,file=photo.file)
            except:
                pass 
            if instance:
                patron = None
                try:
                    patron = Borrowers.objects.get(cardnumber=cardnumber)  
                except:
                    pass
                if patron:
                   photorec = None
                   try:
                       photorec = PatronBulkPhotos.objects.get(patron_id=patron)
                   except:
                       pass
                   if photorec:
                       instance.file.delete()
                       instance.delete()
                   else:
                       instance.patron_id = patron
                       print(instance.patron_id)
                       instance.save()
                else:
                   print("No such cardnumber ", cardnumber)
                   instance.file.delete()
                   instance.delete()
            else:
                print("No such photo instance")
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = PatronBulkPhotos.objects.all()
        return render(self.request, 'photos/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PatronPhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            base = os.path.basename(photo.file.url)
            cardnumber = (os.path.splitext(base)[0]).upper()
            instance = None
            try:
               instance = PatronBulkPhotos.objects.get(patron_id=None,file=photo.file)
            except:
                pass 
            if instance:
                patron = None
                try:
                    patron = Borrowers.objects.get(cardnumber=cardnumber)  
                except:
                    pass
                if patron:
                   photorec = None
                   try:
                       photorec = ParonBulkPhotos.objects.get(patron_id=patron)
                   except:
                       pass
                   if photorec:
                       instance.file.delete()
                       instance.delete()
                   else:
                       instance.patron_id = patron
                       instance.save()
                else:
                   instance.file.delete()
                   instance.delete()
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = PatronBulkPhotos.objects.all()
        return render(self.request, 'photos/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            base = os.path.basename(photo.file.url)
            cardnumber = (os.path.splitext(base)[0]).upper()
            instance = None
            try:
               instance = PatronBulkPhotos.objects.get(patron_id=None,file=photo.file)
            except:
                pass 
            if instance:
                patron = None
                try:
                    patron = Borrowers.objects.get(cardnumber=cardnumber)  
                except:
                    pass
                if patron:
                   photorec = None
                   try:
                       photorec = ParonBulkPhotos.objects.get(patron_id=patron)
                   except:
                       pass
                   if photorec:
                       instance.file.delete()
                       instance.delete()
                   else:
                       instance.patron_id = patron
                       instance.save()
                else:
                   instance.file.delete()
                   instance.delete()
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def delete_patron_photo(request, pk):
     photo=None
     try:
        photo = PatronBulkPhotos.objects.get(pk=pk)
     except:
        pass
     if photo:
        photo.file.delete()
        photo.delete()
     return redirect(request.POST.get('next'))

def clear_database(request):
     photos = PatronBulkPhotos.objects.all()
     for photo in photos:
        photo.file.delete()
        photo.delete()
     return redirect(request.POST.get('next'))


