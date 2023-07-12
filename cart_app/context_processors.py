def total_cart_quantity(request):
    return {"total_cart_quantity": request.session.get("cart").get("total_quantity")}
