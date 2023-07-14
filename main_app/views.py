from django.shortcuts import render, redirect
from .models import Product
from cart_app.cart import Cart
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.
def dashboard(request):
    context = {"products": Product.objects.all()}
    return render(request, "main_app/dashboard.html", context)


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
    context = {}
    cart = Cart(request)
    cart_detail = cart.get_cart_items()
    individual_items = cart_detail["individual_items"]
    cart_total_price = cart_detail["cart_total_price"]
    context = {
        "individual_items": individual_items,
        "cart_total_price": cart_total_price,
    }
    return render(request, "main_app/cart.html", context)


def clear_cart(request):
    cart = Cart(request)
    res = cart.clear_cart()
    messages.success(request, res["message"])
    return redirect('main_app:dashboard')
