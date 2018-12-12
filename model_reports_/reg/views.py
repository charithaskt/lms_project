from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import *
from django.core.mail import EmailMessage
import requests
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def home(request):
    name = ""
    active = False
    if (User.objects.filter(active=True, admin=False)):
        x = User.objects.filter(active=True, admin=False)
        x = x[0]
        x = User.objects.get(email=x)
        name = x.fullname
        active = x.active

    return render(request, 'reg/home.html', {
        'name': name,
        'active': active
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            to_email = form.cleaned_data.get('email')
            response = requests.get(
                "http://api.quickemailverification.com/v1/verify?email=" + to_email + "&apikey=7304da5f8417d4a865dc14bc1122b0e7349b65a2b0333a7e3fda0e8c8427")
            response = response.json()
            if (response['result'] == "valid"):
                user = form.save(commit=False)
                user.active = False
                user.email_confirmed = False
                #user.password = form.cleaned_data.get('password1')
                user.save()
                u1 = User.objects.get(email=form.cleaned_data.get('email'))
                current_site = get_current_site(request)
                mail_subject = 'Activate your blog account.'
                message = render_to_string('reg/acc_active_email.html', {
                    'user': u1.fullname,
                    'domain': 'localhost:8000', #current_site
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Please confirm your email address to complete the registration')
            else:
                return HttpResponse('The email given is invalid please check it ')
    else:
        form = SignupForm()
        active = False
        if (User.objects.filter(active=True, admin=False)):
            x = User.objects.filter(active=True, admin=False)
            x = x[0]
            x = User.objects.get(email=x)
            active = x.active

        return render(request, 'reg/signup.html', {
            'active': active,
            'form': form
        })

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if (User.objects.filter(active=True, admin=False)):
            x = User.objects.filter(active=True, admin=False)
            for i in range(len(x)):
                x[i].active = False
        user.active = True
        user.email_confirmed = True
        user.last_login = timezone.now()
        user.save()

        return redirect('home')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    if request.method == 'POST':

        if (request.POST['action'] == 'login'):
            if User.objects.filter(email=request.POST['email']).count():
                ur = User.objects.get(email=request.POST['email'])
                if (request.POST['password'] == ur.password):
                    ur.active = True
                    ur.last_login = timezone.now()
                    ur.save()
                    return redirect('home')
                else:
                    return HttpResponse('Wrong Password')
            else:
                return HttpResponse('user doesnot exist')

        elif (request.POST['action'] == 'forgot'):
            u = User.objects.get(email=request.POST['email'])
            to_email = u.email
            response = requests.get(
                "http://api.quickemailverification.com/v1/verify?email=" + to_email + "&apikey=7304da5f8417d4a865dc14bc1122b0e7349b65a2b0333a7e3fda0e8c8427")
            response = response.json()
            # return HttpResponse(response)
            if (response['result'] == "valid" and response['did_you_mean'] == ''):
                #domain = get_current_site(request)
                subject = 'Reset Your Password'
                message = render_to_string('reg/Reset_password_email.html', {
                    'user': u.fullname,
                    'domain': 'localhost:8000',
                    'uid': urlsafe_base64_encode(force_bytes(u.pk)).decode,
                    'token': passwordreset_token.make_token(u)
                })

                email = EmailMessage(
                    subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('Check ur mail to reset password')
            else:
                return HttpResponse('The email given is invalid please check it ')
    else:
        form = LoginForm()
        return render(request, 'reg/login.html', {'form': form})


def reset(request, uidb64, token):
    try:
        u = force_text(urlsafe_base64_decode(uidb64))
        u = User.objects.get(pk=u)
    except:
        u = None
    if u is not None and passwordreset_token.check_token(u, token):
        if (request.POST):
            u.active = True
            u.last_login = timezone.now()
            u.password = request.POST['Password']
            u.save()
            return redirect('home')
        else:
            return render(request, 'reg/reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        return HttpResponse('Password Reset link is invalid!')


def logout(request):
    if (User.objects.filter(active=True, admin=False)):
        x = User.objects.filter(active=True, admin=False)
        x = x[0]
        x = User.objects.get(email=x)
        x.active = False
        x.save()
    return redirect('home')
