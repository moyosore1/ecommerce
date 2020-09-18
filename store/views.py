from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem, Shipping, Customer, Category
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from .filters import ProductFilter


# Create your views here.
def shop(request):
    data = cartData(request)
    categories = Category.objects.all()
    products = Product.objects.all().order_by('?')[:6]
    productsMostShopped = Product.objects.all().order_by('?')[:6]
    print(products)    
    
    context = {
        'products': products,
        'categories': categories,
        'cart_items': data['cartItems'],
        'most': productsMostShopped,
    }

    return render(request, 'store/home.html', context)

def cart(request):
    data = cartData(request)
    categories = Category.objects.all()
    context = {
        'items': data['items'],
        'order': data['order'],
        'cart_items': data['cartItems'],
        'categories': categories,
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
    categories = Category.objects.all()
    context = {
        'items': data['items'],
        'order': data['order'],
        'cart_items': data['cartItems'],
        'categories': categories,
    }
    return render(request, 'store/checkout.html', context)

def update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, order_status='pending')
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)

    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()

    return JsonResponse('Yoooo, server talking!!', safe=False)


def shipping(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        address = data['shippingDetails']['address']
        email = customer.user.email
        state = data['shippingDetails']['state']
        city = data['shippingDetails']['city']
        zipCode = data['shippingDetails']['zip']
        order, created = Order.objects.get_or_create(customer=customer, order_status='pending')

    else:
        customer, order = guestOrder(request, data)
        name = data['userDetails']['name']
        email = data['userDetails']['email']
        address = data['shippingDetails']['address']
        state = data['shippingDetails']['state']
        city = data['shippingDetails']['city']
        zipCode = data['shippingDetails']['zip']

    order.transaction_id = transaction_id
    total = float(data['shippingDetails']['total'])
    if total == order.get_cart_total:
        order.order_status = 'delivered'
    order.save()

    Shipping.objects.create(
        customer=customer,
        order=order,
        address=address,
        state=state,
        city=city,
        zipcode=zipCode,
    )

    send_mail(
    'Order '+str(transaction_id),
    'Your order was received and is being processed. Thanks for shopping with us.',
    'moyosoreolumideobi@gmail.com',
    [email],
    fail_silently=False,
    )

    return JsonResponse('Hello there ', safe=False)


def category_products(request, pk):
    category = get_object_or_404(Category, id=pk)
    products = category.product_set.all()
    categories = Category.objects.all()
    context = {
        'products': products,
        'category': category,
        'categories': categories,
    }
    return render(request, 'store/category_products.html', context)


@login_required
def wishlist(request):
    customer = request.user.customer
    customer_wishlist_products = customer.wishlist.get_wishlist_products
    number_of_products = customer.wishlist.get_wishlist_total
    data = cartData(request)
    categories = Category.objects.all()

    if number_of_products >= 1:
        context = {
            'wishlist_products' : customer_wishlist_products,
            'categories': categories,
            'cart_items': data['cartItems'],
        }
        return render(request, 'store/wishlist.html', context)
    else:
        context = {
            'categories': categories,
            'cart_items': data['cartItems'],
        }
        return render(request, 'store/empty_wishlist.html', context)

def product_details(request, pk):
    product = Product.objects.get(id=pk)
    data = cartData(request)
    categories = Category.objects.all()
    wishlist = request.user.customer.wishlist
    productCategoryId = product.product_category.id
    in_wishlist = wishlist.check_if_product_in_wishlist(product)
    context = {
        'product': product,
        'categories': categories,
        'cart_items': data['cartItems'],
        'in_wishlist': in_wishlist,
        'categoryId': productCategoryId,
    }
    return render(request, 'store/product_details.html', context)


@login_required
def add_to_wishlist(request, pk):
    wishlist = request.user.customer.wishlist
    product = Product.objects.get(id=pk)
    if wishlist.check_if_product_in_wishlist(product) == False:
        wishlist.products.add(product)
        messages.success(request, product.product_name+' was successfully added to your wishlist!')
        
    else:
        messages.info(request, product.product_name+' already in your wishlist!')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_wishlist(request, pk):
    wishlist = request.user.customer.wishlist
    product = Product.objects.get(id=pk)
    if wishlist.check_if_product_in_wishlist(product):
        wishlist.products.remove(product)
        messages.success(request, product.product_name+' removed from your wishlist.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else: 
        return redirect('Store-home')  

@login_required
def move_to_cart(request, pk):
    wishlist = request.user.customer.wishlist
    product = Product.objects.get(id=pk)
    if wishlist.check_if_product_in_wishlist(product):
        wishlist.products.remove(product)
        return redirect('Store-cart')
    else: 
        return redirect('Store-home')     


def search_products(request):
    data = cartData(request)
    categories = Category.objects.all()
    search_query = request.GET.get('product_name')
    search = ProductFilter(request.GET, queryset=Product.objects.all())
    context = {
        'search_query':search_query,
        'cart_items': data['cartItems'],
        'categories': categories,
        'search':search
    }
    return render(request, 'store/results.html', context)

def help_customers(request):
    categories = Category.objects.all()
    data = cartData(request)
    return render(request, 'store/help.html', {'categories':categories, 'cart_items': data['cartItems']})

def contact_us(request):
    categories = Category.objects.all()
    data = cartData(request)
    return render(request, 'store/contact_us.html', {'categories': categories, 'cart_items': data['cartItems']})


@login_required
def account_details(request):
    userDetails = request.user
    categories = Category.objects.all()
    data = cartData(request)
    context = {
        'user': userDetails, 
        'cart_items': data['cartItems'],
        'categories': categories,
    }

    return render(request, 'store/account.html', context)
