from django.db import models
from django.contrib.auth.models import User

class Categorymodel(models.Model):
    category_name=models.CharField(max_length=100)
    category_image=models.ImageField(upload_to='images',null=True)

    @property
    def products(self):
        return Productmodel.objects.filter(product_category=self)

    def __str__(self):
        return self.category_name

class Productmodel(models.Model):
    product_name=models.CharField(max_length=100)
    product_image=models.ImageField(upload_to='images',null=True)
    product_description=models.TextField(max_length=200,null=True)
    product_price=models.IntegerField()
    product_stock=models.IntegerField()
    product_category=models.ForeignKey(Categorymodel,on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class Cartmodel(models.Model):
    cart_product=models.ForeignKey(Productmodel,on_delete=models.CASCADE)
    cart_user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart_date=models.DateTimeField(auto_now_add=True)
    cart_quantity=models.IntegerField()
    

class Ordermodel(models.Model):
    order_product=models.ForeignKey(Productmodel,on_delete=models.CASCADE)
    order_user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now_add=True)
    order_address=models.CharField(max_length=300,null=False)
    order_quantity=models.IntegerField()