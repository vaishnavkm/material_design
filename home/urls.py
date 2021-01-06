from django.urls import path,include
from .views import  home,products,ordersummaryview,payement
from .views import (addtocart,product,checkout,remove_from_cart,remove_item_cart)
from . import views
from . import models
from . import forms

app_name = 'core'

urlpatterns = [
    path('',home.as_view(),name='home'),
    path('product/',views.product,name='product'),
    path('checkout/',checkout.as_view(),name='checkout'),
    path('products/<slug>/', products.as_view(), name='products'),
    path('addtocart/<slug>/', addtocart, name='addtocart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('register/',views.register_id,name='register'),
    path('login/',views.login_id,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('ordersummaryview/',ordersummaryview.as_view(),name='ordersummaryview'),
    path('remove_item_cart/<slug>/',views.remove_item_cart, name='remove_item_cart'),
    path('payement/',payement.as_view(),name='payement'),
   
  
  

]

