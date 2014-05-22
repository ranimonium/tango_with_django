from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Rango bango dango tango <a href='/rango/about'>About</a>")

def about(request):
	return HttpResponse("Rango says: this the fcking about page <a href='/rango/'>Index</a>")

