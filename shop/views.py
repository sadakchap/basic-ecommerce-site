from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from cart.forms import CartAddProductForm
from .models import Category,Product

# Create your views here.
def product_list(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    context = {
        'category':category,
        'categories':categories,
        'products':products
    }
    return render(request,'shop/product_list.html',context)

def product_detail(request,id,slug):
    product = get_object_or_404(Product,id=id,slug=slug)
    cart_form = CartAddProductForm()
    return render(request,'shop/product_detail.html',{'product':product,'cart_form':cart_form})
