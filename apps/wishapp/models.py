from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        get_username = User.objects.filter(username=postData['username'])

        if len(postData['username']) == 0:
            errors["no_username"] = "Please enter your username"
        if (len(get_username) == 0):
            errors["username_does_not_exist"] = "Username does not exist."
            return errors
        else:
            get_stored_pw = get_username.first().password

            if len(postData['password']) == 0:
                errors["no_password"] = "Please enter your password."
            if bcrypt.checkpw(postData['password'].encode(), get_stored_pw.encode()) == False:
                errors["wrong_password"] = "Incorrect password."
            return errors

    def reg_validator(self, postData):
        errors = {}
        get_username = User.objects.filter(username=postData['username'])

        #username exists:
        if len(get_username) > 0:
            errors["username_exists"] = "Username already exists."

        #LENGTHS
        if len(postData['name']) < 2:
            errors["first_length"] = "Name must be longer than 2 characters"
        if len(postData['username']) < 2:
            errors["User_length"] = "Username must be longer than 2 characters"
        if len(postData['password']) < 8:
            errors["no_password"] = "Your password must be greater than 8 characters."
        if len(postData['confirm-password']) == 0 :
            errors["no_confirm"] = "Please confirm your password."
        if len(postData["date_hired"]) == 0:
            errors["no_date"] = "Please confirm your hiring date."

        #FORMAT
        if all(letter.isalpha() for letter in postData['username']) == False:
            errors["first_format"] = "Your Username must only contain letters."
        #Password
        if (postData['password'] != postData['confirm-password']):
            errors['password_confirm'] = "Your password confirmation does not match."

        return errors

class ProductManager(models.Manager):
    def product_validator(self, postData):
        errors = {}
        if len(postData["product"]) == 0:
            errors["no_product"] = "Please enter a product."
        if len(postData['product']) < 2:
            errors["product_error"] = "Product must be longer than 2 characters"
        return errors  



class User(models.Model):
    name = models.CharField(max_length = 45)
    username = models.CharField(max_length = 45)
    password = models.CharField(max_length = 255)
    date_hired = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Product(models.Model):
    item_name = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    group = models.ManyToManyField(User, related_name="wishlist")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = ProductManager()

