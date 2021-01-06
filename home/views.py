from django.http import request
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import View
from .models import *
from .models import Items,shipping_address,Payment,Order,OrderItems
from django.views.generic import DetailView,ListView,View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms  import CreateForm,checkoutform
from django.core.exceptions import ObjectDoesNotExist
from home import forms
from django.conf import settings
import stripe 
stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
class home(ListView):
    model=Items
    paginate_by=2
    template_name='home.html'

class products(DetailView):
    model=Items
    template_name='product.html'
 

def product(request):
    content={'items':Items.objects.all()}
    return render(request,'products.html',content)

class checkout(View):
    def get(self,*args, **kwargs):
        form=checkoutform()
        context={
            'form':form
        }
        return render(self.request,'checkout.html',context)
    

    def post(self,*args, **kwargs):
        form=checkoutform(self.request.POST or None)
        try:
         order=Order.objects.get(user=self.request.user,ordered=False)
         if form.is_valid():
            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            address=form.cleaned_data.get('address')
            country=form.cleaned_data.get('country')
            state=form.cleaned_data.get('state')
            zip=form.cleaned_data.get('zip')
            #save_billing_add=form.cleaned_data.get('save_billing_add')
            #save_info=form.cleaned_data.get('save_info')
            payement=form.cleaned_data.get('payement')
            Shipping_address=shipping_address(
               user=self.request.user,
               first_name=first_name,
               last_name=last_name,
               username=username,
               email=email,
               address=address,
               country=country,
               state=state,
               zip=zip,

           )
            Shipping_address.save()
            order.Shipping_address=Shipping_address
            order.save()
            return redirect('core:payement')
         messages.warning(self.request,"failed checkout")
         return redirect('core:checkout')
           
        except ObjectDoesNotExist:
           messages.error(self.request,"you donot have order")
           return redirect('core:checkout')
        

class payement(View):    #pip install django-payments-cod
    def get(self,*args, **kwargs):
        return render(self.request,'payement.html')  

    def post(self, *args, **kwargs):
       order=Order.objects.get(user=self.request.user,ordered=False)
       token=self.request.POST.get('stripeToken')
       #amount=order.item * 100
       try:
         charge=stripe.Charge.create(amount=amount,currency="usd",source=token)
         payement=payement()
         payement.stripe_charge_id=charge['id']
         payement.user=self.request.user 
         payement.amount=amount 
         payement.save()
         messages.success(self,request,"your order was successfull")
         return redirect('/')
       except stripe.error.CardError as e:
    # Since it's a decline, stripe.error.CardError will be caught
        body = e.json_body
        err=body.get('error',{})
        messages.error(self.request, f"{err.get('messages')}")
        return redirect('/')
       
       
        
       
       except stripe.error.RateLimitError as e:
        
    # Too many requests made to the API too quickly
        messages.error(self.request, "rate limit error")
        return redirect('/')
        
        
       except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        messages.error(self.request, "invalid error")
        return redirect('/')
        
        
       except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        messages.error(self.request, "not authencited")
        return redirect('/')
        
       except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        messages.error(self.request, "network error")
        return redirect('/')
        
       except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        messages.error(self.request, "smoenthing went wrong")
        return redirect('/')
        
       except Exception as e:
        # Something else happened, completely unrelated to Stripe
        messages.error(self.request, "a serriouos error")
        return redirect('/')






       
       






    

@login_required
def addtocart(request,slug):
    item=get_object_or_404(Items,slug=slug)
    order_item,created=OrderItems.objects.get_or_create(
    items=item,
    user=request.user,
    ordered=False,
    ) 
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item in the  order
        if order.items.filter(items__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request,'This Item Quantity Was  Updated')
            #return render(request,'cart.html')
            return redirect("core:ordersummaryview")  
        else:
            messages.info(request,'This Item Was Added To Your Cart')
            order.items.add(order_item)
            #return render(request,'cart.html')
            return redirect("core:products",slug=slug)    
    else:
        order_date=timezone.now()
        order=Order.objects.create(user=request.user,order_date=order_date)
        order.items.add(order_item)
        messages.info(request,'This Item Was Added To Your Cart')
        return redirect("core:products",slug=slug)    #("core:product",kwargs={'slug':slug})

@login_required
def remove_from_cart(request,slug):
    item=get_object_or_404(Items,slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False,
        )
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item in the  order
        if order.items.filter(items__slug=item.slug).exists():
            order_item=OrderItems.objects.filter(
    items=item,
    user=request.user,
    ordered=False,
    ) [0]
            order.items.remove(order_item)
            messages.info(request,'This Item Was Removed To Your Cart')
            
            #return render(request,'cart.html')
            return redirect("core:products",slug=slug)  
        else:
            
            #return render(request,'cart.html')
            messages.info(request,'This Item Was Not In Your Cart')
            return redirect("core:products",slug=slug)   
    else:
        #the user doesnot have a order
        messages.info(request,'you donot have a ordeer')
        return redirect("core:products",slug=slug)

@login_required
def remove_item_cart(request,slug):
    item=get_object_or_404(Items,slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False,
        )
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item in the  order
        if order.items.filter(items__slug=item.slug).exists():
            order_item=OrderItems.objects.filter(
    items=item,
    user=request.user,
    ordered=False,
    ) [0]  
            if order_item.quantity >1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request,'This Item Was updated')
            
            #return render(request,'cart.html')
            return redirect("core:ordersummaryview")  
        else:
            
            #return render(request,'cart.html')
            messages.info(request,'This Item Was Not In Your Cart')
            return redirect("core:ordersummaryview",slug=slug)   
    else:
        #the user doesnot have a order
        messages.info(request,'you donot have a ordeer')
        return redirect("core:ordersummaryview",slug=slug)
    











def register_id(request):
    form=CreateForm()
    if request.method == 'POST':
        form=CreateForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request,'You Have Successely Registered : ' +  user)
            return redirect("/login")
       
    content={'form':form}
    return render(request,'register.html',content)

def login_id(request):

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request,"User Is Not Created ")

    content={}
    return render(request,'login.html',content)


def logout_user(request):
    logout(request)
    return redirect('/login')

class ordersummaryview(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user,ordered=False)
            context = {
                'object':order
            } 
            
            return render(self.request,'carts.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"you donot have order")
            return redirect('/')
        