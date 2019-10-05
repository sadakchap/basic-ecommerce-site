from django.shortcuts import render,redirect,get_object_or_404
from .models import OrderItem,Order
from .forms import OrderForm
from cart.cart import Cart
from .tasks import order_created

from django.urls import reverse

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def order_create(request):
    cart = Cart(request)
    form = OrderForm(request.POST or None)
    print('valid or not',form.is_valid())
    if form.is_valid():
        order = form.save()
        for item in cart:
            OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])

        cart.clear()
        # order_created.delay(order.id)   # uncomment it when using celery for sending invoice
        request.session['order_id'] = order.id
        return redirect(reverse('payment:process'))
    return render(request,'orders/order_create.html',{'form':form,'cart':cart})

@staff_member_required
def admin_order_detail(request,order_id):
    order = get_object_or_404(Order,id=order_id)
    return render(request,'admin/order_detail.html',{'order':order})




import weasyprint
from django.template.loader import render_to_string
from django.http import HttpResponse

@staff_member_required
def admin_order_pdf(request,order_id):
    order =get_object_or_404(Order,id=order_id)
    html = render_to_string('orders/pdf.html',{'order':order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="order_{}.pdf"'.format(order.id)

    link = 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(link)])
    return response
