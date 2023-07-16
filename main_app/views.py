from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem
from cart_app.cart import Cart
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


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
    context["individual_items"] = individual_items
    context["cart_total_price"] = cart_total_price
    return render(request, "main_app/cart.html", context)


def clear_cart(request):
    cart = Cart(request)
    res = cart.clear_cart()
    messages.success(request, res["message"])
    return redirect("main_app:dashboard")


def clear_all_sessions(request):
    Session.objects.all().delete()
    return JsonResponse({"message": "all sessions clear"})


def product_detail(request, product_id):
    context = {}
    product = Product.objects.get(pk=product_id)
    context["product"] = product
    return render(request, "main_app/product_detail.html", context)


"""checkout logic, take products from cart and create order with the help of cart order and cart items
reduce quantity of product and clear cart"""


def checkout(request):
    context = {}
    cart = Cart(request)
    cart_detail = cart.get_cart_items()
    individual_items = cart_detail["individual_items"]
    cart_total_price = cart_detail["cart_total_price"]
    context["individual_items"] = individual_items
    context["cart_total_price"] = cart_total_price
    if request.method == "GET":
        user = request.user
        order = Order.objects.create(user=user, total_price=cart_total_price)
        for item in individual_items:
            product = Product.objects.get(pk=item["product_id"])
            product.quantity_available -= item["quantity"]
            product.save()
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=item["price"],
            )
            # put order_item in order
            order.products.add(product)
        cart.clear_cart()
        messages.success(request, "Order Placed Successfully")
        return redirect("main_app:dashboard")
    return render(request, "main_app/checkout.html", context)
