from django import forms
from .models import User,Categorymodel,Productmodel,Ordermodel


class User_register_form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'})
        }

class User_login_form(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class Category_form(forms.ModelForm):
    class Meta:
        model=Categorymodel
        fields="__all__"
        widgets={
            'category_name':forms.TextInput(attrs={'class':'form-control',}),
        }

class Product_form(forms.ModelForm):
    class Meta:
        model=Productmodel
        fields="__all__"
        widgets={
            'product_name':forms.TextInput(attrs={'class':'form-control'}),
            'product_description':forms.TextInput(attrs={'class':'form-control'}),
            'product_price':forms.NumberInput(attrs={'class':'form-control'}),
            'product_stock':forms.TextInput(attrs={'class':'form-control'}),
            'product_category':forms.Select(attrs={'class':'form-control'}),
        }

class Order_form(forms.ModelForm):
    class Meta:
        model=Ordermodel
        fields=['order_address']
        labels={'order_address':'Address'}
        widgets={
            'order_address':forms.Textarea(attrs={'class':'form-control','rows':'3'})
        }