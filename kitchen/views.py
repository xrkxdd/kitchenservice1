
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, world! This is the home page.")

def ingridients(request):
    return HttpResponse("Hello, world! This is the ingridients page.")

def register(request):
    return HttpResponse("Hello, world! This is the register page.")

def login(request):
    return HttpResponse("Hello, world! This is the login page.")

def dishes(request):
    return HttpResponse("Hello, world! This is the dishes page.")


def cooks(request):
    return HttpResponse("Hello, world! This is the cooks page.")

