from django.contrib import admin
from .models import OrderItem,Order
# from import_export.admin import ImportExportModelAdmin

from django.utils.safestring import mark_safe
from django.urls import reverse

def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(reverse('orders:admin_order_detail',args=[obj.id])))

def order_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(reverse('orders:admin_order_pdf',args=[obj.id])))

import csv
import datetime
from django.http import HttpResponse

def export_to_csv(modeladmin,request,queryset):
    opts = modeladmin.model._meta  #going to give meta data of modeladmin class -- orders.order
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attchment; filename="{}.csv"'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [f for f in opts.get_fields() if not f.many_to_many and not f.one_to_many]
    writer.writerow([f.verbose_name for f in fields])

    for obj in queryset:
        data_row = []
        for f in fields:
            value = getattr(obj,f.name) #getattr(class,field)---getattr(O,updated) where O is obj of Order CLass
            if isinstance(value,datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export_to_CSV'

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','email','postal_code','city','paid','created','updated',order_detail,order_pdf]
    list_filter  = ['created','updated','paid']
    inlines      = [OrderItemInline]
    actions       = [export_to_csv]
