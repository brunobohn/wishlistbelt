# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from models import *

# Create your views here.
def index(request):
        return render(request, 'wishapp/index.html')

def register(request):
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return redirect('/')
    else:
        username = request.POST['username']
        if "username" not in request.session:
            request.session['username'] = username
        
        if "logged_in" not in request.session:
            request.session['logged_in'] = True
               
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed_pw, date_hired = request.POST['date_hired'])

    return redirect('/reg/'+str(user.id))

## Validating User to Login
def login(request):
	user = User.objects.filter(username = request.POST.get('username')).first()
        username = request.POST['username']
        if "username" not in request.session:
            request.session['username'] = username
        
        if "logged_in" not in request.session:
            request.session['logged_in'] = True

	if user and bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
		return redirect('/reg/'+str(user.id))
	else: 
		# messages.error(request, 'invalid credentials')
		messages.add_message(request, messages.INFO, 'invalid credentials', extra_tags="login")
		request.session.clear()
        return redirect('/')

def home(request, id):
        if "logged_in" not in request.session:
            return redirect('/')
        else:
            username = request.session["username"]
            user = User.objects.get(username=username)


            context = {
                        'data': user,
                        "id": user.id,
                        "name": user.name,
                        "products": Product.objects.all().filter(group=user),
                        "users": Product.objects.all().exclude(group=id).order_by("created_at")
                    }
            
        return render(request, 'wishapp/home.html',context)

def create(request,id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        username = request.session["username"]
        user = User.objects.get(username=username)
        context = {
                        "id": user.id,
                    }

        return render(request, 'wishapp/create.html',context)

def addproduct(request):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        username = request.session["username"]
        user = User.objects.get(username=username)
        errors = Product.objects.product_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)
            return redirect('/reg/'+str(user.id)+'/create')
        

        product = Product.objects.create(
        item_name = request.POST["product"],
        user = User.objects.get(username=request.session['username'])
        )

        product.group.add(User.objects.get(username=request.session['username']))
        product.save()

        return redirect('/reg/'+str(user.id))

def logout(request):
    request.session.clear()
    return redirect('/')


def showproduct(request,product_id):
    if "logged_in" not in request.session:
            return redirect('/')
    else:
        product = Product.objects.get(id=product_id)

        context = {
                    "product": product.item_name,
                    "users": product.group.all()

                }
    return render(request, 'wishapp/product.html',context)


def join(request, id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(username=request.session['username'])


        product = Product.objects.get(id=id)
        product.group.add(user)
        product.save()

        return redirect('/reg/'+str(user.id))

def delete_product(request, product_id):
    if "logged_in" not in request.session:
        return redirect('/')
    else:
        username = request.session["username"]
        user = User.objects.get(username=username)
        product = Product.objects.get(id=product_id)
        product.group.remove(user)
        Product.objects.get(id=product_id).delete()

        return redirect('/reg/'+str(user.id))

def remove(request,product_id):
    username = request.session["username"]
    user = User.objects.get(username=username)
    product = Product.objects.get(id=product_id)
    product.group.remove(user)

    return redirect('/reg/'+str(user.id))
