from django.shortcuts import render,redirect,get_object_or_404
from orders.models import Order

import braintree

import weasyprint
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from io import BytesIO
# Create your views here.

def payment_process(request):
    order_id = request.session['order_id']
    order = get_object_or_404(Order,id=order_id)
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce')
        result = braintree.Transaction.sale({
                    'amount':'{:.2f}'.format(order.get_total_cost()),
                    'payment_method_nonce': nonce,
                    'options': {
                        'submit_for_settlement': True
                    }
        })

        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            order.save()
            sub = 'My Shop - Invoice no. {}'.format(order.id)
            msg = 'Please, find an attachted invoice for your recent purchase.'
            email = EmailMessage(sub,msg,settings.EMAIL_HOST_USER,[order.email])

            html = render_to_string('orders/pdf.html',{'order':order})
            out = BytesIO()
            link = 'https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css'
            stylesheets = [weasyprint.CSS(link)]
            weasyprint.HTML(string=html).write_pdf(out,stylesheets=stylesheets)
            email.attach('order_{}.pdf'.format(order.id),out.getvalue(),'application/pdf')
            email.send()

            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        client_token = braintree.ClientToken.generate()
        return render(request,'payment/payment_process.html',{'order':order,'client_token':client_token})


def payment_canceled(request):
    return render(request,'payment/payment_canceled.html')

def payment_done(request):
    return render(request,'payment/payment_done.html')
