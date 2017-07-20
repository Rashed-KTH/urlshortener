from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import re
import json
from urlshortener.modules.shortify import url_shortener
from urlshortener.models import Urlshort

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

	return render(request, 'urlshortener/index.html', {})

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
		if url_obj.url:
			return redirect(url_obj.url)
	except:
		return render(request, 'urlshortener/opps.html', {})