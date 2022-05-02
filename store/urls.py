from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list),
    path('products/<int:id>/', views.product_detail),
    path('collections/', views.collection_list),
    path('collections/<int:value>', views.collection_detail),
    path('collections/<str:value>', views.collection_detail)
]
