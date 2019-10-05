from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    sub = 'Order nr. {}'.format(order.id)
    msg	= 'Dear {},\n\nYou have	successfully placed	an order.\nYour order id is {}.'.format(order.first_name,order.id)
    mail_sent = send_mail(sub,msg,'aliceprerna@gmail.com',[order.email])
    return mail_sent
