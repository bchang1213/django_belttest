# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
	if "user" in request.session:
		return redirect('/dashboard')
	return	render(request, "wishlist/index.html")

def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		user = User.objects.get(username=request.POST['username'])
		if user:
			if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
				messages.error(request, 'Account with those credentials could not be found.')
				return redirect('/')
			else:
				if user:
					request.session['user'] = user.id
					messages.success(request, 'Login Successful!')
					return	redirect('/dashboard')
					# return redirect(reverse('success',kwargs ={'user_id':user.id}))

def logout(request):
	del request.session['user']
	return redirect('/')

def register(request):
	errors = User.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags= tag)
		return redirect('/')
	else:
		user = User.objects.create()
		user.name = request.POST['name']
		user.username = request.POST['username']
		user.doh =request.POST['doh']
		user.password =bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		user.save()
		messages.success(request, 'User created. Please login!')
		return redirect('/')

def dashboard(request):
	context={
	'user': User.objects.get(id=request.session['user']),
	'addedbyitems': Addedby.objects.filter(user_id=request.session['user']),
	'notaddedbyuser': Addedby.objects.exclude(user_id = request.session['user']),
	}
	return render(request, "wishlist/dashboard.html", context)

def itemform(request):
	return render(request, "wishlist/itemform.html")

def additem(request):
	if len(request.POST['item']) < 3:
		messages.error(request, "Your item must be at least 3 characters long.")
	item = Item.objects.create(name=request.POST['item'], createdby_id=request.session['user'])
	additemtolist = Addedby.objects.create(item_id=item.id, user_id=request.session['user'])
	item.save()
	return redirect('/dashboard')

def aboutitem(request, item_id):
	context={
	'item': Item.objects.get(id=item_id),
	'userswhoadded': Addedby.objects.filter(item_id=item_id),
	}
	return render(request, "wishlist/aboutitem.html", context)

def addwish(request, item_id):
	additem = Addedby.objects.create(item_id=item_id, user_id=request.session['user'])
	return redirect('/')

def removewish(request, item_id):
	removeitem = Addedby.objects.filter(item_id=item_id)
	removeitem.delete()
	return redirect('/')

def delete(request, item_id):
	deleteitem = Item.objects.filter(id = item_id)
	deleteitem.delete()
	return redirect('/')









