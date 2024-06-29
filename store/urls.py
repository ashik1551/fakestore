from django.urls import path
from store import views


urlpatterns = [
    path('register/', views.User_regitration.as_view(),name='register'),
    path('login/', views.User_login.as_view(),name='login'),
    path('superuser/', views.Superuser_regitration.as_view(),name='superuser'),
    path('category/',views.Add_category.as_view(),name='category'),
    path('product/',views.Add_product.as_view(),name='product'),
    path('home/',views.Category_view.as_view(),name='home'),
    path('products/<int:pk>',views.Product_view.as_view(),name='products'),
    path('products_detail/<int:pk>',views.Product_detail.as_view(),name='products_detail'),
    path('products_update/<int:pk>',views.Product_update.as_view(),name='products_update'),
    path('addtocart/<int:pk>',views.Addtocart.as_view(),name='addtocart'),
    path('cart/',views.Cart.as_view(),name='cart'),
    path('cart_delete/<int:pk>',views.Cart_Delete.as_view(),name='cart_delete'),
    path('order/',views.Order.as_view(),name='order'),
    path('myorders/',views.Myorders.as_view(),name='myorders'),
    path('ordernow/<int:pk>',views.Ordernow.as_view(),name='ordernow'),
    path('buynow/<int:pk>',views.Ordernow_direct.as_view(),name='buynow'),
    path('logout/',views.Logout.as_view(),name='logout'),
]