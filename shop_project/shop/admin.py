from django.contrib import admin

# Register your models here.

from .models import Profile, Product, Order, OrderItem

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone_number', 'address_city', 'registration_date')
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'phone_number', 'address_city')
    list_filter = ('registration_date',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'quantity', 'added_date')
    search_fields = ('name', 'description')
    list_filter = ('added_date',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'total_amount', 'order_date')
    search_fields = ('client__username',)
    list_filter = ('order_date',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity')
    search_fields = ('product__name', 'order__id')