from django.shortcuts import render
from django.http import HttpResponse # No longer needed as we are now using the django render and not HttpResponse
									 # NOTE: Chapter 5 calls for import HttpResponse again

# Create your views here.

def home_page(request):
	return render(request, 'home.html', {
		'new_item_text': request.POST.get('item_text', ''),
	})

	##if request.method == 'POST':
		##return HttpResponse(request.POST['item_text'])
	# return HttpResponse('<html><title>To-Do lists</title></html>') --> Instead of building our own HttpResponse, 
	# 																     we now use the Django render function. 


