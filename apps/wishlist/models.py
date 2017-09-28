from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
	def login_validator(self, postData):
		errors = {}
		if not len(postData['username']) or len(postData['password']) < 8:
			errors['email']="Please enter valid credentials."
		return errors

	def basic_validator(self, postData):
		errors = {}
# VALIDATING THE NAME
		if len(postData['name']) == 0:
			errors['name']="Please enter your name"
# VALIDATING username
		if len(postData['username']) == 0:
			errors['username']="Please enter your username"

# VALIDATING PASSWORD
		if len(postData['password']) == 0:
			errors['password']="Please enter a password"
		else:
			if len(postData['password']) < 8:
				errors['password']= "Password must be at least 8 characters."

			if not any([letter.isupper() for letter in postData['password']]):
				errors['password1']= "Password must contain at least one uppercase letter."

			if not any([letter.isdigit() for letter in postData['password']]):
				errors['password2']= "Password must contain at least one number."

			if not any([letter in "!@#$%^&*()-_=+~`\"'<>,.?/:;\}{][|" for letter in postData['password']]):
				errors['password3']= "Password must contain at least one special character."

			if postData['password'] != postData['passconf']:
				errors['password4']= 'Password and confirmation fields must match.'
		return errors


class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	doh = models.DateField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __repr__(self):
		return ("<User object: id:{} {} {}>".format(self.id, self.name, self.alias))

class Item(models.Model):
	name = models.CharField(max_length=255)
	createdby = models.ForeignKey(User, related_name = "createdby")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Addedby(models.Model):
	user = models.ForeignKey(User, related_name = "addedby")
	item = models.ForeignKey(Item, related_name = "item_added")

