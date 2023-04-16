from django.urls import path
from . import views

urlpatterns = [
    path('sayhello/',views.say_hello),
    #path('products/<int:id>/',views.product_detail),
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>', views.ProductDetail.as_view()),
    path('categories/<int:id>',views.category_detail, name='category-detail'),
]