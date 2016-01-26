from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
	item = request.POST.get('item_text', '')
	context = {
		'new_item_text': item
	}
	return render(request, 'home.html',context)
