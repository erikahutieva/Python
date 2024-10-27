from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import *

menu = [{'title': "Home", 'url_name': 'home'},
        {'title': "Cart", 'url_name': 'cart'},
        {'title': "Categories", 'url_name': 'categories'},
        {'title': "Products", 'url_name': 'searchProducts'},
        {'title': "Clients", 'url_name': 'searchClients'},
        {'title': "About", 'url_name': 'about'},
        # {'title': "Log in", 'url_name': 'login'}
]

def index(request):
    context = {
        'title': 'Главная страница',
        'text': 'Пока пусто :(',
        'menu': menu,
        'site': 'home'
    }
    return render(request, 'mylaba/index.html', context=context)

def about(request):
    context = {
        'title': 'О сайте',
        'text': 'Пока пусто :(',
        'menu': menu,
        'site': 'about',
    }
    return render(request, 'mylaba/index.html', context=context)

def searchClients(request):
    context = {
        'title': 'Поиск по клиентам',
        'users': Clients.objects.all(),
        'menu': menu,
        'site': 'searchClients',
    }
    if (request.GET) and (request.GET['q'] != ''):
        try:
            query = [request.GET['q'].split()[0], request.GET['q'].split()[1]]
        except:
            query = [request.GET['q'].split()[0],]

        users = Clients.objects.filter(surname=query[0])
        context['users'] = users

    if len(context['users']) == 0:
        context['users'] = Clients.objects.all()

    return render(request, 'mylaba/search.html', context=context)


def searchProducts(request):
    context = {
        'title': 'Поиск по товарам',
        'products': Products.objects.all(),
        'menu': menu,
        'site': 'searchProducts',
    }
    if (request.GET) and (request.GET['q'] != ''):
        flag = 1
        try:
            products = Products.objects.filter(name=request.GET['q'])
            print(request.GET)
        except:
            flag = 0

        if flag:
            context['products'] = products

    if len(context['products']) == 0:
        context['products'] = Products.objects.all()

    return render(request, 'mylaba/productsearch.html', context=context)


def client(requests, clientid):
    return HttpResponse(f"Клиент номер {clientid}")

def product(requests, productid):
    p = Products.objects.get(pk=productid)
    context = context = {
        'title': p.name,
        'menu': menu,
        'product': p,
        'site': 'product'
    }


    if requests.POST:
        if requests.POST['add_to_cart'] == 'add_to_cart':
            proverka = Cart.objects.filter(product_id=p.pk)
            if proverka:
                proverka[0].quantity += int(requests.POST['quantity'])
                if proverka[0].quantity <= p.total_amount:
                    proverka[0].save()
            else:
                Cart.objects.create(product_id=p.pk, quantity=int(requests.POST['quantity']), name=p.name, price=p.price)

    return render(requests, 'mylaba/product.html', context=context)

def categorys(request):
    context = {
        'title': 'Каталог товаров',
        'menu': menu,
        'site': 'categories'
    }

    cats = Category.objects.all()
    context['cats'] = cats

    return render(request, 'mylaba/categorys.html', context=context)

def catalog_category(requests, cat_slug):
    context = {
        'title': 'Каталог товаров',
        'menu': menu,
        'site': 'categorys'
    }

    products = Category.objects.get(slug=cat_slug).products_set.all()
    context['products'] = products

    return render(requests, 'mylaba/catalog.html', context=context)

def cart(request):
    context = {
        'title': 'Корзина',
        'menu': menu,
        'site': 'categorys',
        'cartitems': '',
        'total_amount': 0,
        'error': 0,
    }
    total_amount = 0
    cartitems = Cart.objects.all()
    if cartitems:
        context['cartitems'] = cartitems
        for item in cartitems:
            total_amount += item.line_total()
        context['total_amount'] = total_amount

    if request.POST:
        method = request.POST['payment']
        user = get_object_or_404(Clients, pk=request.POST['user_id'])

        if not user:
            context['error'] = 1
        else:
            if method == 'no-cash':
                if  total_amount <= user.account:
                    user.total_purchase += total_amount
                    user.account -= total_amount
                    for item in Cart.objects.all():
                        prdct = get_object_or_404(Products, pk=item.product_id)
                        prdct.total_amount -= item.quantity
                    Cart.objects.all().delete()
                    user.save()
                    prdct.save()

                    return redirect('cart')
                else:
                    context['error'] = 1
            elif method == 'cash':
                user.total_purchase += total_amount
                for item in Cart.objects.all():
                    prdct = get_object_or_404(Products, pk=item.product_id)
                    prdct.total_amount -= item.quantity
                Cart.objects.all().delete()
                user.save()
                prdct.save()

                return redirect('cart')
            elif method == 'credit':
                if total_amount <= user.loan_limit:
                    user.total_purchase += total_amount
                    user.loan_balance += total_amount
                    user.loan_limit -= total_amount
                    for item in Cart.objects.all():
                        prdct = get_object_or_404(Products, pk=item.product_id)
                        prdct.total_amount -= item.quantity
                    Cart.objects.all().delete()
                    user.save()
                    prdct.save()

                    return redirect('cart')
                else:
                    context['error'] = 1
            elif method == 'barter':
                for item in Cart.objects.all():
                    prdct = get_object_or_404(Products, pk=item.product_id)
                    prdct.total_amount -= item.quantity
                Cart.objects.all().delete()
                user.save()
                prdct.save()

                return redirect('cart')
            elif method == 'offsetting':
                if total_amount >= user.loan_balance:
                    user.loan_limit += user.loan_balance
                    user.account += total_amount - user.loan_balance
                    user.loan_balance = 0
                else:
                    user.loan_limit += total_amount
                    user.loan_balance -= total_amount

                for item in Cart.objects.all():
                    prdct = get_object_or_404(Products, pk=item.product_id)
                    prdct.total_amount += item.quantity
                Cart.objects.all().delete()
                user.save()
                prdct.save()

                return redirect('cart')
            else:
                context['error'] = 1

    return render(request, 'mylaba/cart.html', context=context)

def add_to_cart(request):
    return redirect('cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, product_id=item_id)
    cart_item.delete()
    return redirect("cart")

def clear_cart(request):
    Cart.objects.all().delete()
    return redirect('cart')

def pageNotFound(request, exception):
    # return HttpResponseNotFound('<h1 align="center">Ошибка 404: Страница не найдена</h1>')
    return render(request, 'mylaba/error.html')