from django.db import models
from django.conf import settings
from django.db.models.base import ModelState
from django.urls import reverse
from django_countries.fields import CountryField


# Create your models here.
decide = (
    ('Best','best'),
    ('New','new'),
    ('Popular','popular'),
 )
   

class Items(models.Model):
    title=models.CharField(max_length=200)
    price=models.FloatField()
    image=models.ImageField(upload_to='pics')
    model=models.CharField(choices=decide,max_length=20)
    description=models.CharField(max_length=500)
    discount=models.FloatField(blank=True)
    slug=models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:products", kwargs={"slug": self.slug
        })

    def get_add_to_cart_url(self):
         return reverse("core:addtocart", kwargs={"slug": self.slug
        })
    
    def get_remove_to_cart_url(self):
         return reverse("core:remove_from_cart", kwargs={"slug": self.slug
        })
    
    



class OrderItems(models.Model):
    items=models.ForeignKey(Items,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)


def __str__(self):
        return f"{self.quantity} of {self.items.title}"

def get_total_item_price(self):
     return self.items.price * self.quantity
     

def get_total_discount_price(self):
     return self.items.discount * self.quantity
     

def get_total_saving_price(self):
    return self.get_total_item_price - self.get_total_discount_price

def get_total_price(self):
    if self.items.discount():
        return self.get_total_discount_price()
    else:
        return self.get_total_itemprice()



class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItems)
    start_date=models.DateTimeField(auto_now_add=True)
    order_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    billing_address=models.ForeignKey('shipping_address',on_delete=models.SET_NULL,blank=True,null=True)
    Payment=models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)

def __str__(self):
        return self.user.username

def get_total(self):
    total=0
    for order_item in self.items.all():
        total += order_item.get_total_price
    return total

    

class shipping_address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    email=models.EmailField()      #pip install django-countries
    address=models.CharField(max_length=200)
    country = CountryField(multiple=False)
    state=models.CharField(max_length=200)
    zip=models.IntegerField()
    

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


