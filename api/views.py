from django.shortcuts import render

from .serializers import CategorySerializer,ProductSerializer,CartSerializer,OrderSerializer,UserSerializer

from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from rest_framework.views import APIView

from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView,RetrieveAPIView

from rest_framework import status,permissions,authentication

from rest_framework.decorators import action

from .models import Categorymodel,Productmodel,Cartmodel,Ordermodel,User

from .permissions import IsOwner,IsOwnerOnly


class UserRegistrationView(APIView):

    def post(self,request,*args,**kwargs):

        serializer=UserSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(data=serializer.data)
        
        else:

            return Response(data=serializer.errors)

class CategoryViewSetView(ModelViewSet):

    queryset=Categorymodel.objects.all()

    serializer_class=CategorySerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

class ProductViewSetView(ModelViewSet):

    queryset=Productmodel.objects.all()

    serializer_class=ProductSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticatedOrReadOnly]

    @action(methods=['POST'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):

        id=kwargs.get('pk')

        product_data=Productmodel.objects.get(id=id)

        serializer=CartSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(cart_product=product_data,cart_user=request.user)

            return Response(data=serializer.data)
        
        else:

            return Response(data=serializer.errors)

class CartViewSetView(RetrieveUpdateDestroyAPIView):

    queryset=Cartmodel.objects.all()

    serializer_class=CartSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[IsOwner]


class OrderNowView(CreateAPIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):

        cart_id=kwargs.get('pk')

        cart_data=Cartmodel.objects.get(id=cart_id)

        product_data=cart_data.cart_product

        serializer=OrderSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(order_product=product_data,order_user=request.user)

            return Response(data=serializer.data)
        
        else:

            return Response(data=serializer.errors)
        
class OrderListView(ListAPIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):

        qs=Ordermodel.objects.filter(order_user=request.user)

        serializer=OrderSerializer(qs,many=True)

        return Response(data=serializer.data)

class OrderRetriveView(RetrieveAPIView):

    queryset=Ordermodel.objects.all()

    serializer_class=OrderSerializer

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[IsOwnerOnly]

class CartListView(ListAPIView):

    authentication_classes=[authentication.TokenAuthentication]

    permission_classes=[permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):

        qs=Cartmodel.objects.filter(cart_user=request.user)

        serializer=CartSerializer(qs,many=True)

        return Response(data=serializer.data)
    