from django.shortcuts import render, redirect
from .models import Item
# Create your views here.
def index(request):
    context = {'items' : Item.objects.all(),
    }
    return render(request,'inventory/index.html', context)

def new(request):
    context = {}
    if 'errors' in request.session:
        context = {
                    'errors':request.session['errors'],
                    'formdata':request.session['formdata'],
                    }
    return render(request,'inventory/new.html', context=context)

def create(request):
    (flag,data) = Item.objects.newItem(request.POST)
    if flag == True:
        if 'errors' in request.session:
            del request.session['errors']
            del request.session['formdata']
        return redirect('inventory:index')
    else:
        request.session['formdata'] = { 'edit': False,
                                'name': request.POST['item'],
                                'description': request.POST['description'],
                                'price': request.POST['price'],
                                }
        request.session['errors'] = data
        return redirect('inventory:new')
    return redirect('inventory:index')

def show(request):
    print "show()"
    return redirect('inventory:index')
def edit(request,id):
    context = {}
    item = Item.objects.get(id=id)

    context = { 'edit': True,
                'formdata':{ 'name':item.name,
                             'description': item.description,
                             'price': item.price,
                             'id': item.id,
                            },
                }
    return render(request,'inventory/new.html', context=context)

def update(request,id):

    (error,data) = Item.objects.editItem(request.POST,id)

    if error == True:
        request.session['formdata'] = { 'edit': True,
                                'name': request.POST['item'],
                                'description': request.POST['description'],
                                'price': request.POST['price'],
                                }
        request.session['errors'] = data
        return redirect('inventory:new')
    else:
        if 'errors' in request.session:
            del request.session['errors']
            del request.session['formdata']
        return redirect('inventory:index')
    return redirect('inventory:index')
def destroy(request,id):
    print "destroy()", id
    toDelete = Item.objects.get(id=id)
    print "Deleting",toDelete.name
    toDelete.delete()
    return redirect('inventory:index')
