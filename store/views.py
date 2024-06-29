from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View,CreateView,ListView,DetailView,UpdateView
from .forms import User_register_form,User_login_form,Category_form,Product_form,Order_form
from .models import User,Categorymodel,Productmodel,Cartmodel,Ordermodel
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.core.mail import send_mail
from django.utils.decorators import method_decorator


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

def cart_user(fn):
    def wrapper(request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Cartmodel.objects.get(id=id)
        if data.cart_user!=request.user:
            return redirect('home')
        else:
            return fn(request,*args,**kwargs)
    return wrapper

class User_regitration(View):
    def get(self,request):
        form=User_register_form()
        return render(request,"register.html",{'form':form})
    
    def post(self,request):
        form=User_register_form(request.POST)
        if form.is_valid():
            user=User.objects.create_user(**form.cleaned_data)

            subject = 'Zay Shopping'
            message = f'Hi {user.first_name} {user.last_name}, thank you for registering in Zay Shopping. Your id is {user.username}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail( subject, message, email_from, recipient_list)
        return redirect('login')
    

class User_login(View):
    def get(self,request):
        form=User_login_form()
        return render(request,"login.html",{'form':form})
    
    def post(self,request):
        form=User_login_form(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                print(request.user)
                return redirect('home')
            else:
                print('login failed')
        return redirect('login')
    
class Superuser_regitration(View):
    def get(self,request):
        form=User_register_form()
        return render(request,"registeradmin.html",{'form':form})
    
    def post(self,request):
        form=User_register_form(request.POST)
        if form.is_valid():
            User.objects.create_superuser(**form.cleaned_data)
        return redirect('login')

class Add_category(CreateView):
    model=Categorymodel
    form_class=Category_form
    template_name='category.html'
    success_url=reverse_lazy('categoryview')

class Add_product(CreateView):
    model=Productmodel
    form_class=Product_form
    template_name='product.html'
    success_url=reverse_lazy('product')

class Category_view(ListView):
    model=Categorymodel
    template_name="home.html"
    context_object_name="data"

# class Product_view(ListView):
#     model=Productmodel
#     template_name="product_view.html"
#     context_object_name="data"

class Product_view(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Productmodel.objects.filter(product_category=id)
        context={'data':data}
        return render(request,"product_view.html",context)

class Product_detail(DetailView):
    model=Productmodel
    template_name="product_detail.html"
    context_object_name="data"

class Product_update(UpdateView):
    model=Productmodel
    form_class=Product_form
    template_name='product.html'
    success_url=reverse_lazy('products')

@method_decorator(signin_required,name='dispatch')
class Addtocart(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Productmodel.objects.get(id=id)
        Cartmodel.objects.create(cart_user=request.user,cart_product=data)
        return redirect('cart')

@method_decorator(signin_required,name='dispatch')
class Cart(View):
    def get(self,request,*args,**kwargs):
        data=Cartmodel.objects.filter(cart_user=request.user)
        price=0
        for i in data:
            if i.cart_product and hasattr(i.cart_product,'product_price'):
                price+=i.cart_product.product_price*i.cart_quantity
        return render(request,'cart.html',{'data':data,'price':price})

@method_decorator(signin_required,name='dispatch')
@method_decorator(cart_user,name='dispatch')
class Cart_Delete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        Cartmodel.objects.get(id=id).delete()
        return redirect('cart')
    
@method_decorator(signin_required,name='dispatch')    
class Order(View):
    def get(self,request,*args,**kwargs):
        data=Cartmodel.objects.filter(cart_user=request.user)
        form=Order_form()
        price=0
        count=0
        cart=Cartmodel.objects.filter(cart_user=request.user)
        for i in cart:
            count+=1
            if i.cart_product and hasattr(i.cart_product,'product_price'):
                price+=i.cart_product.product_price*i.cart_quantity
        return render(request,'order.html',{'data':data,'price':price,'form':form,'count':count})
    
    def post(self,request,*args,**kwargs):
        data=Order_form(request.POST)
        if data.is_valid():
            address=data.cleaned_data.get('order_address')
            cart=Cartmodel.objects.filter(cart_user=request.user)
            for i in cart:
                Ordermodel.objects.create(order_product=i.cart_product,order_user=request.user,order_address=address,order_quantity=i.cart_quantity)
                i.delete()
            return redirect('myorders')

@method_decorator(signin_required,name='dispatch')
class Myorders(View):
    def get(self,request,*args,**kwargs):
        data=Ordermodel.objects.filter(order_user=request.user).order_by('-order_date')
        return render(request,'myorders.html',{'data':data})

@method_decorator(signin_required,name='dispatch')
class Ordernow(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Cartmodel.objects.get(id=id)
        form=Order_form()
        price=data.cart_product.product_price
        count=1
        return render(request,'orders.html',{'data':data,'price':price,'form':form,'count':count})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Cartmodel.objects.get(id=id)
        form=Order_form(request.POST)
        if form.is_valid():
            address=form.cleaned_data.get('order_address')
            Ordermodel.objects.create(order_product=data.cart_product,order_user=request.user,order_address=address,order_quantity=data.cart_quantity)
            data.delete()
        return redirect('myorders')

@method_decorator(signin_required,name='dispatch')
class Ordernow_direct(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Productmodel.objects.get(id=id)
        Cartmodel.objects.create(cart_user=request.user,cart_product=data)
        form=Order_form()
        price=data.product_price
        count=1
        return render(request,'orderbuy.html',{'data':data,'price':price,'form':form,'count':count})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get('pk')
        data=Productmodel.objects.get(id=id)
        form=Order_form(request.POST)
        cart=Cartmodel.objects.filter(cart_user=request.user).last()
        if form.is_valid():
            address=form.cleaned_data.get('order_address')
            Ordermodel.objects.create(order_address=address,order_product=data,order_user=request.user,order_quantity=1)
            cart.delete()
            return redirect('myorders')

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('login')