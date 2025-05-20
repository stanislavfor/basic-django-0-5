"""
URL configuration for shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import home_page, AddProduct, EditProduct, DeleteProduct, AddOrder, EditOrder, DeleteOrder, update_profile
from django.urls import include
from .views import clients_list
from .views import products_list
from .views import orders_list
from .views import client_detail
from .views import product_detail
from .views import order_detail
from .views import add_client
from .views import update_order
from .views import add_product
from .views import delete_product
from .views import products_total
from .views import client_orders
from .views import clients_orders
from .views import profile
from .views import custom_logout
from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),  # Панель администратора
#     path('', home_page, name='home'), # Главное правило для корня сайта
#     path('add-product/', add_product, name='add_product'),
#     path('edit-product/<int:pk>/', EditProduct.as_view(), name='edit_product'),
#     path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
#     # path('delete-product/<int:pk>/', DeleteProduct.as_view(), name='delete_product'),
#     path('add-order/', AddOrder.as_view(), name='add_order'),
#     path('edit-order/<int:pk>/', EditOrder.as_view(), name='edit_order'),
#     path('delete-order/<int:pk>/', DeleteOrder.as_view(), name='delete_order'),
#     path('update-profile/', update_profile, name='update_profile'),
#     path('accounts/', include('django.contrib.auth.urls')),  # Стандартная URL-аутентификация
#     path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Маршрут для login.html
#     path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Маршрут для login.html
#     path('accounts/profile/', profile, name='profile'),
#     path('accounts/logout/', custom_logout, name='custom_logout'),
#     path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logged_out'),
#     path('clients/', clients_list, name='clients_list'),
#     path('products/', products_list, name='products_list'),
#     path('products-total/', products_total, name='products_total'),
#     path('orders/', orders_list, name='orders_list'),
#     path('clients/<int:client_id>/', client_detail, name='client_detail'),
#     path('products/<int:product_id>/', product_detail, name='product_detail'),
#     path('orders/<int:order_id>/', order_detail, name='order_detail'),
#     path('add-client/', add_client, name='add_client'),
#     path('update-order/<int:order_id>/', update_order, name='update_order'),
#     path('client-orders/', client_orders, name='client_orders'),
#     path('clients-orders/', clients_orders, name='clients_orders'),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .views import home_page, AddProduct, EditProduct, DeleteProduct, AddOrder, EditOrder, DeleteOrder, update_profile
from django.urls import include
from .views import clients_list
from .views import products_list
from .views import orders_list
from .views import client_detail
from .views import product_detail
from .views import order_detail
from .views import add_client
from .views import update_order
from .views import add_product
from .views import delete_product
from .views import products_total
from .views import client_orders
from .views import clients_orders
from .views import profile
from .views import custom_logout
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),  # Панель администратора
                  path('', home_page, name='home'), # Главное правило для корня сайта
                  path('add-product/', add_product, name='add_product'),
                  path('edit-product/<int:pk>/', EditProduct.as_view(), name='edit_product'),
                  path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
                  # path('delete-product/<int:pk>/', DeleteProduct.as_view(), name='delete_product'),
                  path('add-order/', AddOrder.as_view(), name='add_order'),
                  path('edit-order/<int:pk>/', EditOrder.as_view(), name='edit_order'),
                  path('delete-order/<int:pk>/', DeleteOrder.as_view(), name='delete_order'),
                  path('update-profile/', update_profile, name='update_profile'),
                  path('accounts/', include('django.contrib.auth.urls')),  # Стандартная URL-аутентификация
                  path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Маршрут для login.html
                  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Маршрут для login.html
                  path('accounts/profile/', profile, name='profile'),
                  path('accounts/custom_logout/', custom_logout, name='custom_logout'),
                  path('clients/', clients_list, name='clients_list'),
                  path('products/', products_list, name='products_list'),
                  path('products-total/', products_total, name='products_total'),
                  path('orders/', orders_list, name='orders_list'),
                  path('clients/<int:client_id>/', client_detail, name='client_detail'),
                  path('products/<int:product_id>/', product_detail, name='product_detail'),
                  path('orders/<int:order_id>/', order_detail, name='order_detail'),
                  path('add-client/', add_client, name='add_client'),
                  path('update-order/<int:order_id>/', update_order, name='update_order'),
                  path('client-orders/', client_orders, name='client_orders'),
                  path('clients-orders/', clients_orders, name='clients_orders'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

