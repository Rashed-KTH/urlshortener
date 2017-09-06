import json
import re
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from urlshortener.modules.shortify import url_shortener
from urlshortener.models import Urlshort
from urlshortener.modules.serializers import UserSerializer, UrlshortSerializer

# Api end point to get the current temparature of kista
TEMPARATURE_ENDPOINT = "https://api.darksky.net/forecast/310c1407438ae52c7be84b723c6af2ba/59.4024,17.9465"

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class UrlshortViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shorten url to be viewed or edited.
    """
    queryset = Urlshort.objects.all()
    serializer_class = UrlshortSerializer
    

def index(request):
	"""
	Entry page of the application.
	If the request is a ajax request:
		->fetch the url and execute the 'url_shortener' method 
		->if everything goes well return a HttpResponse with json data
	otherwise:
		render the index.html page
	"""
	if request.is_ajax():
		url = request.GET.get('url', None)

		json_response = url_shortener(url)

		return HttpResponse(json.dumps(json_response),
            content_type='application/json')

	# Api integration for temparature at kista
	response = requests.get(TEMPARATURE_ENDPOINT)
	json_response = response.json()
	temp_far = float(json_response["currently"]["temperature"])
	temp_cel = int(((temp_far - 32)*5) / 9)
	return render(request, 'urlshortener/index.html', {"current_temp":temp_cel})

def test(request):
	"""
	Test page to varify the urlshortener application
	"""
	return render(request, 'urlshortener/test.html', {})

def page_redirect(request, hash_value):
	"""
	redirecting user to the appropiate url based on hash_value
	IN : hash_value -> generated while shortening the url
	OUT : redirect to url

	"""
	#url_obj = get_object_or_404(Urlshort,hash_value=hash_value) #django default page not found
	try:
		url_obj = Urlshort.objects.get(hash_value=hash_value)
		if url_obj.original_url:
			return redirect(url_obj.original_url)
	except:
		return render(request, 'urlshortener/opps.html', {})

