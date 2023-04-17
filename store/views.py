from django.shortcuts import render
from django.http import HttpResponse
from .serializers import *
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.

# APIView provides handler methods (get, post, etc)
# Mixins provide actions (list, create, destroy, etc)
# generic views provide handlers
# ViewSets provide actions


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id', 'unit_price']

    def destroy(self, request, pk):
        if OrderItem.objects.filter(product=kwargs['pk']):
            return Response({'error': "This product is associated with an order item"},
                                status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ProductList(ListCreateAPIView):
    # more concise way
    # inheriting from concrete view classes
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # def get_serializer_context(self):
    #     return {'request':self.request}

    # def get_queryset(self):
    #     # if you have more logic to implement the queryset
    #     # remove the queryset line above
    #     return super().get_queryset()

    # def get_serializer_class(self):
    #     # if you want to add more logic to serializer class
    #     # remove the serializer line above
    #     return super().get_serializer_class()



class ProductList(APIView):
   
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    def post(self, request):
        serializer = PorductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer = ProductSerializer
    lookup_field = "id"


    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response({'error':' This product is associated with an orderitem'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

 

class ProductDetail(APIView):
    def get(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request, id):
        product = get_object_or_404(Product, pk=id)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) # 201 is default reponse
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitem_set.count() > 0:
            return Response({'error':' This product is associated with an orderitem'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def say_hello(request):
    return HttpResponse("Hello bro")

@api_view(['GET', 'POST'])
def product_list(request):
    # you need to add select related to queryset when getting object or str of
    # a related field
    if request.method == 'GET':
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PorductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE'])
def product_detail(request,id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':    
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data) # 201 is default reponse
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({'error':' This product is associated with an orderitem'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view()
def category_detail(request, id):
    return Response('ok')