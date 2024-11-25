from django.db import models
from customers.models import Customer
from carts.models import Cart, CartItem
import uuid
from products.models import Product
# Create your models here.
class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, default=None, related_name='cart', help_text="The cart used for this order")
    choices = (('Created','Created'), ('Pending','Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled'))
    status = models.CharField(choices=choices, default='Created', max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_amount(self):
        # Calculate total amount from all items in the cart
        return self.cart.items.aggregate(total=models.Sum('total_price'))['total'] or 0

    def __str__(self):
        return f"{self.customer.first_name} "
    
    


    
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items', help_text="The order this item belongs to")
    cartitems = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='items', help_text="The cart item associated with this order item")

  
    def __str__(self):
        return f"{self.cartitems.product.name} in Order {self.order.order_id}"
