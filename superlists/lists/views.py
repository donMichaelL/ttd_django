from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

# Create your views here.

def home_page(request):
	return render(request, 'home.html')

# get /lists
def view_list(request, list_id):
	my_list = List.objects.get(id=list_id)
	#items = Item.objects.filter(list=my_list)
	return render(request, 'list.html', {'list': my_list})

# post /lists/new
def new_list(request):
	new_list = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=new_list)
	return redirect('/lists/%d/' % (new_list.id,))

# post /lists/add_item
def add_item(request, list_id):
	my_list = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=my_list)
	return redirect('/lists/%d/' % (my_list.id,))
