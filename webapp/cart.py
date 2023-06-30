from django.conf import settings
from decimal import Decimal
from .models import Product


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in self.session:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        self.cart[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = int(quantity)
            self.save()

    def get_items(self):
        items = []
        for product_id, item_data in self.cart.items():
            try:
                product = Product.objects.get(id=product_id)
                item = {
                    'product': product,
                    'quantity': item_data['quantity'],
                    'price': item_data['price'],
                    'total': product.price * item_data['quantity']
                }
                items.append(item)
            except Product.DoesNotExist:
                pass
        return items
    
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        total = Decimal(0)
        for item in self.get_items():
            total += item['total']
        return total
