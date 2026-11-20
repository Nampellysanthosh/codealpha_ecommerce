from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.home_view, name='products'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:pk>/', views.cart_add_view, name='cart_add'),
    path('cart/update/<int:pk>/', views.cart_update_view, name='cart_update'),
    path('cart/remove/<int:pk>/', views.cart_remove_view, name='cart_remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:pk>/', views.order_success_view, name='order_success'),
    path('orders/', views.orders_list_view, name='orders'),
    path('orders/<int:pk>/', views.order_detail_view, name='order_detail'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('category/<str:category>/', views.category_view, name='category'),
]
