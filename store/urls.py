from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
from . import views

# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter() # nested router
router.register('products', views.ProductViewSet)


product_router = routers.NestedDefaultRouter(router, 
                'products',    
                lookup='product') # lookup becomes product_pk

product_router.register('reviews', views.ReviewViewSet, 
                        basename='product-review') 
                        # basename is the name used to address it in code

urlpatterns = router.urls + product_router.urls
"""
urlpatterns = [
    path('', include(router.urls))
    path('sayhello/',views.say_hello),
    #path('products/<int:id>/',views.product_detail),
    path('products/', views.ProductList.as_view()),
    path('products/<int:id>', views.ProductDetail.as_view()),
    path('categories/<int:id>',views.category_detail, name='category-detail'),
]
"""