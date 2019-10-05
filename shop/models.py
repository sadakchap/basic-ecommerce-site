from django.db import models
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name    = models.CharField(max_length=255)
    slug    = models.SlugField(max_length=255,unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('shop:list_by_category',kwargs={'category_slug':self.slug})


class Product(models.Model):
    category    = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    name        = models.CharField(max_length=255,db_index=True)
    slug        = models.SlugField(max_length=255,db_index=True)
    image       = models.ImageField(upload_to='products/%Y/%m/%d/',blank=True)
    desc        = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10,decimal_places=2)
    available   = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)
    stock       = models.PositiveIntegerField(default=100)

    class Meta:
        ordering = ('-created',)
        index_together = (('id','slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',kwargs={'id':self.id,'slug':self.slug})
