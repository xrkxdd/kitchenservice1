from django.shortcuts import render, redirect
from django.http import HttpResponse

import kitchen.views


def home(request):
    return render(request, 'home.html')

def ingredients(request):
    return render(request, 'ingredients.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def dishes(request):
    return render(request, 'dishes.html')


def cooks(request):
    return render(request, 'cooks.html')

