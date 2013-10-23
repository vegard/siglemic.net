# Django
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import httplib
import json

dummy_password = client_secret

def site_login(request):
	# XXX: url encode?
	return HttpResponseRedirect('https://api.twitch.tv/kraken/oauth2/authorize?response_type=code&client_id=%s&redirect_uri=%s&scope=user_read' % (client_id, redirect_uri))

@login_required
def site_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def site_authenticate(request):
	scope = request.GET['scope']
	code = request.GET['code']

	connection = httplib.HTTPSConnection('api.twitch.tv', timeout=5)
	connection.request('POST', 'https://api.twitch.tv/kraken/oauth2/token', 'client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s' % (client_id, client_secret, redirect_uri, code))
	response = connection.getresponse()
	if response.status != 200:
		# XXX: proper error message
		raise RuntimeError("calling kraken/oauth2/token")

	body = json.loads(response.read())
	access_token = body['access_token']

	connection.request('GET', 'https://api.twitch.tv/kraken/user?oauth_token=%s' % access_token)
	response = connection.getresponse()
	if response.status != 200:
		# XXX: proper error message
		raise RuntimeError("calling kraken/user")

	twitch_user = json.loads(response.read())
	# keys: bio, display_name, name, created_at, updated_at, partnered, logo, _id, email

	twitch_username = twitch_user['name']

	try:
		user = User.objects.get(username=twitch_username)
	except User.DoesNotExist:
		user = User.objects.create_user(twitch_username, email=twitch_user['email'], password=client_secret)

	user = authenticate(username=twitch_username, password=client_secret)
	login(request, user)

	return HttpResponseRedirect('/')

from django.template import RequestContext, loader

def site_main(request):
	return render_to_response('website/main.html', RequestContext(request))

def site_stream(request):
	return render_to_response('website/stream.html', RequestContext(request))

def site_news(request):
	return render_to_response('website/news.html', RequestContext(request))

def site_faq(request):
	return render_to_response('website/faq.html', RequestContext(request))

def site_resources(request):
	return render_to_response('website/resources.html', RequestContext(request))

def site_gallery(request):
	return render_to_response('website/gallery.html', RequestContext(request))
