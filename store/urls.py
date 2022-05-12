from django.urls import path
from . import views
# from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from pprint import pprint
from rest_framework_nested import routers 

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet, basename='collections')
# router.register('reviews', views.ReviewViewSet, basename='reviews')
router.register('carts', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('orders', views.OrderViewSet, basename='order')


products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

#pprint(router.urls)


urlpatterns = [
    # path('products/', views.product_list), # function based view
    # path('products/', views.ProductList.as_view()),  # class based view
    # path('products/<int:id>/', views.product_detail), # function based view
    # path('products/<int:pk>/', views.ProductDetail.as_view()),  # class based view
    # path('collections/', views.collection_list), # function based view
    # path('collections/', views.CollectionList.as_view()), # class based view
    # path('collections/<int:value>', views.collection_detail), # function based view
    # path('collections/<str:value>', views.collection_detail),  # function based view
    # path('collections/<int:pk>', views.CollectionDetail.as_view()), # class based view NB: i need to call pk instead of id for convention otherwise I should add a look_up terms
    # path('reviews/', views.ReviewList.as_view()), # class based view
    # path('reviews/<int:pk>', views.ReviewDetail.as_view()) # class based view
    path('', include(router.urls)), # routing a ViewSet
    path('', include(products_router.urls)), 
    path('', include(carts_router.urls)), 
]
