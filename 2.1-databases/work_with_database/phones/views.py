from django.shortcuts import render, get_object_or_404
from phones.models import Phone

def index(request):
    return render(request, 'index.html')

def catalog(request):
    sort = request.GET.get('sort')
    phones = Phone.objects.all()

    if sort == 'name':
        phones = phones.order_by('name')
    elif sort == 'min_price':
        phones = phones.order_by('price')
    elif sort == 'max_price':
        phones = phones.order_by('-price')

    context = {'phones': phones}
    return render(request, 'catalog.html', context)

def product(request, slug):
    phone = get_object_or_404(Phone, slug=slug)
    context = {'phone': phone}
    return render(request, 'product.html', context)