from django.shortcuts import render
"""from django.http import HttpResponse""" # No longer needed as we are now using the django render and not HttpResponse

# Create your views here.

def home_page(request):
	"""return HttpResponse('<html><title>To-Do lists</title></html>')""" #Instead of building our own HttpResponse, we now use the Django render function. 
	return render(request, 'home.html')
