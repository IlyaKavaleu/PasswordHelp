import random
from email.mime.text import MIMEText

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ContactForm
from .models import Password_Model
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import smtplib


@login_required
def password(request):
    characters = list('qwertyuiopasdfghjklzxcvbnm')
    if request.GET.get('uppercase'):
        characters.extend('QWERTYUIOPASDFGHJKLZXCVBNM')
    if request.GET.get('numbers'):
        characters.extend('1234567890')
    if request.GET.get('special'):
        characters.extend('!@#$%^&*()_+')
    lenght = int(request.GET.get('lenght', 10))

    global thepassword
    thepassword = ''
    for x in range(lenght):
        thepassword += random.choice(characters)
    return render(request, 'generator/password.html', {'password': thepassword})


def home(request):
    return render(request, 'generator/home.html')


def about(request):
    about_site = 'Hello this my site!'
    return render(request, 'generator/about.html', {'about_site_dict': about_site})


def register(request):
    if request.method != "POST":
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('home')
    context = {'form': form}
    return render(request, 'registration/register.html', context)


def contact(request):
    sender = 'kavaleuilia@gmail.com'
    password = 'onvpcbwutftzxcki'

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                }
            message = MIMEText("".join(thepassword))
            message['Subject'] = "YOUR PASSWORD"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            try:
                server.login(sender, password)
                server.sendmail(sender, form.cleaned_data['email_address'], f"{message}\nThis is your generated password, save him.\nTHANK YOU FOR USING OUR SERVISE!")
            except BadHeaderError:
                return HttpResponse('Найден некорректный заголовок')
            return redirect("home")

    form = ContactForm()
    return render(request, "generator/contact.html", {'form': form})