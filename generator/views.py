import random
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from password_generator.settings import SENDER, PASSWORD
from .forms import ContactForm
from .models import Password_Model
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import smtplib


# @login_required
def password(request):
    """
    The function helps to GENERATE A PASSWORD depending on the user's preference,
    it can be composed of small letters, uppercase letters, numbers and signs,
    also we can choose the length of the desired password and with method choise we generate password.
    """
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
    """Method generated HOME PAGE"""
    return render(request, 'generator/home.html')


def about(request):
    """Method generated ABOUT PAGE"""
    about_site = 'Hello this my site!'
    return render(request, 'generator/about.html', {'about_site_dict': about_site})


def register(request):
    """
    user registration method, by filling in UserCreationForm we,
     if successful, register a new user and redirect
    to the main page
    """
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
    """
    the method of sending our generated mail to us using the smtplib method, if successful
    we receive a letter to the mail and message, otherwise we get an exception,
    then a redirect to the main page occurs
    """

    sender = SENDER  # sender and password we take from django-environ(file .env)
    password = PASSWORD

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():  # fill out the form before submitting
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
            }
            message = MIMEText("".join(thepassword))
            message['Subject'] = "YOUR PASSWORD"  # create subject(this is message in gmail)
            server = smtplib.SMTP("smtp.gmail.com", 587)  # pass password and port
            server.starttls()  # start encrypted exchange via dls
            try:  # try send message and password
                server.login(sender, password)  # pass sender and password
                server.sendmail(sender, form.cleaned_data['email_address'], f"{message}\nThis is your generated "
                                                                            f"password, save him.\nTHANK YOU FOR "
                                                                            f"USING OUR SERVICE!")
                # sending sender, receiver and
                # message(generated password passed to message variable)

            except BadHeaderError:  # exception
                return HttpResponse('Incorrect title found')
            return redirect("home")

    form = ContactForm()
    return render(request, "generator/contact.html", {'form': form})
