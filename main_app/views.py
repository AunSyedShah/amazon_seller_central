from django.shortcuts import render, redirect
from .models import Product
from cart_app.cart import Cart
from django.http import JsonResponse


# Create your views here.
def dashboard(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'main_app/dashboard.html', context)


def add_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)
    response = cart.add_product(product)
    return JsonResponse(response)


def remove_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)
    response = cart.remove_product(product)
    return JsonResponse(response)


def display_cart(request):
    cart = Cart(request)
    context = {
        'cart': cart.get_cart_items()
    }
    return render(request, 'main_app/cart.html', context)
