from django.shortcuts import render, redirect
from .models import Product, Order, Review, Category
from cart_app.cart import Cart
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.db import connection


# Create your views here.
def dashboard(request):
    products = Product.objects.filter(admin_approved=True)
    search_name = request.GET.get('search_name')
    search_price_min = request.GET.get('search_price_min')
    search_price_max = request.GET.get('search_price_max')
    category = request.GET.get('category')

    # Apply filters based on search parameters
    if search_name:
        products = products.filter(name__icontains=search_name)
    if search_price_min:
        products = products.filter(price__gte=search_price_min)
    if search_price_max:
        products = products.filter(price__lte=search_price_max)
    if category:
        products = products.filter(category_id=category)

    context = {'products': products}
    categories = Category.objects.all()
    context["categories"] = categories
    return render(request, "main_app/dashboard.html", context)


def add_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)
    response = cart.add_product(product)
    return JsonResponse(response, safe=False)


def remove_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(pk=product_id)
    response = cart.remove_product(product)
    return JsonResponse(response, safe=False)


def display_cart(request):
    context = {}
    cart = Cart(request)
    cart_detail = cart.get_cart_items()
    individual_items = cart_detail["individual_items"]
    print(individual_items)
    cart_total_price = cart_detail["cart_total_price"]
    context["individual_items"] = individual_items
    context["cart_total_price"] = cart_total_price
    # 10 - 15 % discount on cart_total_price
    discount = cart_total_price * 0.1
    context["discount"] = discount
    context["cart_total_price"] = cart_total_price - discount
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
    # 10 to 15 percent discount on cart_total_price
    discount = cart_total_price * 0.1
    cart_total_price = cart_total_price - discount
    context["individual_items"] = individual_items
    context["cart_total_price"] = cart_total_price
    shipping_address = request.GET.get("address")
    if request.method == "GET":
        user = request.user
        order = Order.objects.create(user=user, total_price=cart_total_price)
        # order have many products, get products from cart and add to order with quantity
        for item in individual_items:
            product = Product.objects.get(pk=item["product_id"])
            # add product to order with order_quantity and save it
            order.products.add(product)
            product.order_quantity = item["quantity"]
            # reduce quantity of product - remove this later
            product.quantity_available -= item["quantity"]
            product.save()
        request.session['order_id'] = order.id
        order.shipping_address = shipping_address
        order.save()
        cart.clear_cart()
        # email code
        subject = 'Order Confirmation'
        message = f"Your order has been placed successfully. Your order id is {order.id}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [f'{request.user.email}', ]
        send_mail(subject, message, email_from, recipient_list)
        # email code end
        messages.success(request, "Order Placed Successfully")
        return redirect("main_app:order_placed")
    return render(request, "main_app/checkout.html", context)


def print_order_history(request):
    context = {}
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-order_date")
    context["orders"] = orders
    return render(request, "main_app/order_history.html", context)


def review(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        request.session['order_id'] = order_id
        if 'review_submit' in request.POST:
            user = request.user
            review_text = request.POST.get('review')
            review_ratings = request.POST.get('ratings')
            order_id = request.session.get('order_id')
            connection.cursor().execute(
                "INSERT INTO review (user_id, review_text, order_id) VALUES (%s, %s, %s)",
                [user.id, review_text, order_id])
            # Review.objects.create(user=user, review=review_text, order_id=order_id, rating=review_ratings)
            messages.success(request, "Review Submitted Successfully")
            return redirect('main_app:dashboard')
        render(request, "main_app/review.html")
    return render(request, "main_app/review.html")


def order_placed(request):
    return render(request, 'main_app/order_placed.html')


# get all categories of products and return JSON response
def get_categories(request):
    categories = Category.objects.all()
    categories_list = []
    for category in categories:
        categories_list.append(category.name)
    return JsonResponse(categories_list, safe=False)


def add_products(request):
    context = {}
    if request.method == 'POST':
        # name, price, quantity, image, category
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        category = request.POST.get('category')
        category = Category.objects.get(pk=category)
        product = Product.objects.create(name=name, price=price, quantity_available=quantity, image=image,
                                         category=category)
        product.save()
        messages.success(request, "Product Added Successfully")
        return redirect(request.path)
    categories = Category.objects.all()
    context["categories"] = categories
    return render(request, 'main_app/add_product.html', context)


def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        connection.cursor().execute(
            "INSERT INTO main_app_contactus (name, email, message) VALUES (%s, %s, %s)",
            [name, email, message])
        # ContactUs.objects.create(name=name, email=email, message=message)
        messages.success(request, "Message Sent Successfully")
        return redirect('main_app:dashboard')
    return render(request, "main_app/contact_us.html")
