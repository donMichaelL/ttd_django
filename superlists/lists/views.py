from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item

# Create your views here.

def home_page(request):
	if request.method == 'POST':
		item = Item(text=request.POST.get('item_text', ''))
		item.save()
		return redirect('/lists/the-only-list')
	return render(request, 'home.html')


def view_list(request):
	items = Item.objects.all()
	return render(request, 'list.html', {'items': items})
