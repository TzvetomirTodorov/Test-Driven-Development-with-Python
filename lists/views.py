from django.shortcuts import redirect, render
# No longer needed as we are now using the django render and not HttpResponse
from django.http import HttpResponse
from lists.models import Item
                                                                         # s
                                                                         # NOTE:
                                                                         # Chapter
                                                                         # 5
                                                                         # calls
                                                                         # for
                                                                         # import
                                                                         # HttpResponse
                                                                         # again

# Create your views here.


def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

    # if request.method == 'POST':
    # 	new_item_text = request.POST['item_text']
    # 	Item.objects.create(text = new_item_text)
    # else:
    # 	new_item_text = ''

    # return render(request, 'home.html', {
    # 	'new_item_text': new_item_text,
    # })

    # return render(request, 'home.html', {
    # 	'new_item_text': request.POST.get('item_text', ''),
    # })

    # item = Item()
    # item.text = request.POST.get('item_text', '')
    # item.save()

    # if request.method == 'POST':
    # 	Item.objects.create(text = request.POST['item_text'])
    # 	return redirect('/')

    # return render(request, 'home.html')

    # if request.method == 'POST':
        # return HttpResponse(request.POST['item_text'])
    # return HttpResponse('<html><title>To-Do lists</title></html>') --> Instead of building our own HttpResponse,
    # 																     we now use the Django render function.
