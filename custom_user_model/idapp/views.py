from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from .models import *
from . import mybarcode
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie, csrf_exempt
from accounts.models import User, Profile

@csrf_exempt
def index(request):
    # if post request came

    if request.method == 'POST':
        # getting values from post
        global email

        email = request.POST['email']
        print("email = ",email)
        try:
            u = User.objects.get(email=email)
        except:
            return HttpResponse("No user with that email '{}' exists".format(email))
        else:
            if not u.is_active:
                return HttpResponse("User with that email '{}' is not currently an active user".format(email))
        
        context = {
            'firstname': u.profile.firstname,
            'surname': u.profile.surname,
            'email': u.profile.user.email,
            'mobile': u.profile.mobile,
            'userid': u.profile.userid
        }
        template = loader.get_template('idapp/show.html')
        return HttpResponse(template.render(context, request))
        
    else:
        template = loader.get_template('idapp/reg.html')
        return HttpResponse(template.render())


def barcode(request,userid):
    # instantiate a drawing object
    # import mybarcode
    d = mybarcode.MyBarcodeDrawing(userid)
    binaryStuff = d.asString('gif')
    return HttpResponse(binaryStuff, 'image/gif')

