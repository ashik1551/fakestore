from django.urls import path

from rest_framework.routers import DefaultRouter

from rest_framework.authtoken.views import ObtainAuthToken

from api import views



router=DefaultRouter()

router.register("category",views.CategoryViewSetView,basename="category")

router.register("product",views.ProductViewSetView,basename="product")

urlpatterns=[

    path('token/',ObtainAuthToken.as_view()),

    path('signup/',views.UserRegistrationView.as_view()),

    path('cart/<int:pk>/',views.CartViewSetView.as_view()),

    path('cart/',views.CartListView.as_view()),

    path('order/',views.OrderListView.as_view()),

    path('order/<int:pk>/',views.OrderRetriveView.as_view()),

    path('cart/<int:pk>/order/',views.OrderNowView.as_view()),

]+router.urls