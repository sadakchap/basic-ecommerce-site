from django.db import models
from shop.models import Product

# Create your models here.

class Order(models.Model):
    first_name  = models.CharField(max_length=255)
    last_name   = models.CharField(max_length=255)
    email       = models.EmailField()
    address     = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city        = models.CharField(max_length=200)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    paid        = models.BooleanField(default=False)
    braintree_id= models.CharField(max_length=150,blank=True)

    def __str__(self):
        return 'Order {}'.format(self.id)

    class Meta:
        ordering = ('-created',)

    def get_total_cost(self):
        return sum([i.get_cost() for i in self.items.all()])


class OrderItem(models.Model):
    order   = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
    price   = models.DecimalField(max_digits=10,decimal_places=2)
    quantity= models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
