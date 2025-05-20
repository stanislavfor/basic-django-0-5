# from django.contrib.auth import logout
# from .models import Order
# from .forms import OrderForm
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from .models import Product
# from .forms import ProductForm
# from django.shortcuts import render
# # from django.http import HttpResponseRedirect
# from django.urls import reverse
# # from django.views.generic.edit import FormView
# from .forms import ClientProfileForm
# from .models import Profile
# from .models import OrderItem
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect
# from .forms import ProfileForm
# from django.shortcuts import get_object_or_404
# from .forms import ClientForm
# from django.utils import timezone
# from datetime import timedelta
# from django import forms
# from django.views.decorators.http import require_POST

from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from django import forms
from .models import Order, Product, Profile, OrderItem
from .forms import OrderForm, ProductForm, ProfileForm, ClientForm


# Представление для главной страницы (/)
def home_page(request):
    return render(request, 'index.html')

# Order - Представление для добавления нового заказа
class AddOrder(CreateView):
    model = Order
    template_name = 'add_order.html'
    form_class = OrderForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

# Order - Представление для редактирования заказа
class EditOrder(UpdateView):
    model = Order
    template_name = 'edit_order.html'
    success_url = '/'
    form_class = OrderForm

def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders_list')  # Перенаправление на страницу со списком заказов
    else:
        form = OrderForm(instance=order)
    return render(request, 'update_order.html', {'form': form, 'order': order})

# Order - Представление для удаления заказа
class DeleteOrder(DeleteView):
    model = Order
    success_url = '/'

# Product - Представление для добавления нового продукта
class AddProduct(CreateView):
    model = Product
    template_name = 'add_product.html'
    success_url = '/'
    form_class = ProductForm

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('products_list')  # Перенаправление на страницу со списком товаров
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Product - Представление для редактирования продукта
class EditProduct(UpdateView):
    model = Product
    template_name = 'edit_product.html'
    success_url = '/'
    form_class = ProductForm

# Product - Представление для удаления продукта
class DeleteProduct(DeleteView):
    model = Product
    success_url = '/'

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('products_list')
    return render(request, 'delete_product.html', {'product': product})

@login_required
def profile(request):
    return render(request, 'profile.html')

@require_POST
def custom_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на login.html

@login_required
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})

# Client - Добавление профиля нового пользователя

def add_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clients_list')  # Перенаправление на страницу со списком клиентов
    else:
        form = ClientForm()
    return render(request, 'add_client.html', {'form': form})


# Login
@login_required(login_url='/accounts/login/')
def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = OrderForm()
    return render(request, 'add_order.html', {'form': form})


@login_required
def client_orders(request):
    # Текущий пользователь
    user = request.user
    # Заказы пользователя
    orders = Order.objects.filter(client=user)

    last_7_days = timezone.now() - timedelta(days=7)
    products_last_7_days = OrderItem.objects.filter(
        order__in=orders,
        order__order_date__gte=last_7_days
    ).values_list('product__name', flat=True).distinct()

    last_30_days = timezone.now() - timedelta(days=30)
    products_last_30_days = OrderItem.objects.filter(
        order__in=orders,
        order__order_date__gte=last_30_days
    ).values_list('product__name', flat=True).distinct()

    last_365_days = timezone.now() - timedelta(days=365)
    products_last_365_days = OrderItem.objects.filter(
        order__in=orders,
        order__order_date__gte=last_365_days
    ).values_list('product__name', flat=True).distinct()

    context = {
        'products_last_7_days': products_last_7_days,
        'products_last_30_days': products_last_30_days,
        'products_last_365_days': products_last_365_days,
    }
    return render(request, 'client_orders.html', context)


class ClientSelectionForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Profile.objects.all(), label="Выбрать клиента")
    period = forms.ChoiceField(choices=[
        ('7', 'Последние 7 дней'),
        ('30', 'Последние 30 дней'),
        ('365', 'Последние 365 дней'),
    ], label="Выберите период")

@login_required
def clients_orders(request):
    form = ClientSelectionForm(request.POST or None)
    client = None
    orders = None
    products = None

    if form.is_valid():
        client_profile = form.cleaned_data['client']
        client = client_profile.user
        period = int(form.cleaned_data['period'])

        orders = Order.objects.filter(client=client)

        # Товары из заказов за выбранный период
        last_period = timezone.now() - timedelta(days=period)
        products = OrderItem.objects.filter(
            order__in=orders,
            order__order_date__gte=last_period
        ).values_list('product__name', flat=True).distinct()

    context = {
        'form': form,
        'client': client,
        'products': products,
        'period': period if 'period' in locals() else None,
    }

    return render(request, 'clients_orders.html', context)


@login_required(login_url='/accounts/login/')
def update_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('/')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'update_profile.html', {'form': form})


# Отдельные страницы

def clients_list(request):
    clients = Profile.objects.all()
    context = {'clients': clients}
    return render(request, 'clients_list.html', context)

def products_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products_list.html', context)

def products_total(request):
    products = Product.objects.all()  # Все продукты из базы данных
    context = {'products': products}
    return render(request, 'products_total.html', context)

def orders_list(request):
    orders = Order.objects.select_related('client').all()
    context = {'orders': orders}
    return render(request, 'orders_list.html', context)

def client_detail(request, client_id):
    client = get_object_or_404(Profile, id=client_id)
    return render(request, 'client_detail.html', {'client': client})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

