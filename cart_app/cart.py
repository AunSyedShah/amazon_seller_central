from django.conf import settings


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        # alternative self.cart = 'cart'
        self.cart = self.session.get(
            settings.CART_SESSION_ID
        )  # if cart exists return, otherwise None
        if (
                not self.cart
        ):  # if cart is not already initialized, initialize it with empty dicts
            self.cart = self.session[settings.CART_SESSION_ID] = {}
            self.cart.update({"total_quantity": 0})
            self.save()

    def save(self):
        self.session.modified = True

    def get_cart_total_quantity(self):
        return str(self.cart["total_quantity"])

    def add_product(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:  # if product is not already in cart, add it
            self.cart[product_id] = {"quantity": 1, "price": str(product.price)}
            self.cart["total_quantity"] += 1
            self.save()
            return {
                "message": f"product with id {product_id} added initially",
                "quantity": self.cart[product_id]["quantity"],
                "total_quantity": self.get_cart_total_quantity(),
            }
        else:
            self.cart[product_id]["quantity"] += 1
            self.cart["total_quantity"] += 1
            self.save()
            return {
                "message": f"product with id {product_id} increment by 1",
                "quantity": f"{self.cart[product_id]['quantity']}",
                "total_quantity": self.get_cart_total_quantity(),
            }

    # reduce quantity by 1 and remove if quantity is 0
    def remove_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            if self.cart[product_id]["quantity"] > 1:
                self.cart[product_id]["quantity"] -= 1
                self.save()
                return {
                    "message": f"product with id {product_id} decrement by 1",
                    "quantity": f"{self.cart[product_id]['quantity']}",
                }
            else:
                del self.cart[product_id]
                self.save()
                return {"message": f"product with id {product_id} removed from cart"}

    # method to display cart items in a standard format
    def get_cart_items(self):
        cart_items = []
        for product_id in self.cart:
            if product_id != "total_quantity":
                cart_items.append(
                    {
                        "id": product_id,
                        "quantity": self.cart[product_id]["quantity"],
                        "price": self.cart[product_id]["price"],
                    }
                )
        print(cart_items)
        return cart_items
