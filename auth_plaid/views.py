from __future__ import unicode_literals
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from plaid import Client
from plaid.errors import APIError, ItemError
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import UserSignupForm, UserSignupPlusForm
from .models import UserSignupPlus
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
import os
import datetime, json
import requests
import plaid
from datetime import date, datetime
from json import dumps
import logging

PLAID_CLIENT_ID = '59da8e774e95b833dcb75eb0'
PLAID_SECRET = '1a28b9be489f541ed354c1678986f7'
PLAID_PUBLIC_KEY = '6ed7370a11ccdaa1d05b065ad0d383'
PLAID_ENV='sandbox'
access_token = None
public_token = None

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def index(request):
	return redirect('/auth/home/')

def home(request):
	return render(request, 'auth_plaid/home.html')

def signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                request.session['signup_username'] = username
                request.session['signup_email'] = email
                request.session['signup_password'] = password
                return redirect('/auth/signup-plus')
            else:
                return render(request, 'registration/signup.html', {'form' : form, 'error' : 'Looks like a username with that email or password already exists'})
    else:
        form = UserSignupForm()
    return render(request, 'registration/signup.html', {'form' : form, 'errors' : ''})

def signup_plus(request):
    error = ''
    if not request.session.get('signup_username'):
        return redirect('/')
    if request.method == 'POST':
        form = UserSignupPlusForm(request.POST)
        if request.session['signup_email'] == request.POST['email_address']:
            request.session['signup_plus_city'] = request.POST['city']
            request.session['signup_plus_country'] = request.POST['country']
            request.session['signup_plus_state'] = request.POST['state']
            request.session['signup_plus_zip_code'] = request.POST['zip_code']
            request.session['signup_plus_home_phone'] = request.POST['home_phone']
            request.session['signup_plus_birth_date'] = request.POST['birth_date']
            request.session['signup_plus_gender'] = request.POST['gender']
            return redirect('/auth/plaid_verify')
        else:
            form = UserSignupPlusForm()
            error = 'Your email address is not valid'
    else:
        form = UserSignupPlusForm()
    return render(request, 'registration/signupplus.html', {'form' : form, 'error' : error})

def plaid_verify(request):
	if not request.session.get('signup_username'):
		return redirect('/')
	context = {'plaid_public_key': PLAID_PUBLIC_KEY, 'plaid_environment': PLAID_ENV}
	return render(request, 'auth_plaid/plaid_verify.html', context)

def complete_signup(request):
    if not request.session.get('signup_username'):
        return redirect('/')
    username = request.session['signup_username']
    logging.error(username)
    email = request.session['signup_email']
    password = request.session['signup_password']
    User.objects.create_user(username, email, password)
    user = authenticate(username = username, password = password)
    login(request, user)
    if user.is_authenticated:
        obj = UserSignupPlus()
        obj.email_address = email
        obj.city = request.session['signup_plus_city']
        obj.country = request.session['signup_plus_country']
        obj.state = request.session['signup_plus_state']
        obj.zip_code = request.session['signup_plus_zip_code']
        obj.home_phone = request.session['signup_plus_home_phone']
        obj.birth_date = request.session['signup_plus_birth_date']
        obj.gender = request.session['signup_plus_gender']
        obj.save()
	return redirect('/dashboard')

@login_required(login_url='/auth/login/')
def dashboard(request):
	return render(request, 'auth_plaid/dashboard.html')