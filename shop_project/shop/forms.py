
from .models import Order
from .models import Product
from django.contrib.auth.models import User
from django import forms
from .models import Profile



class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Order
        fields = ['client', 'products', 'total_amount']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.request:
            self.fields['client'].initial = self.request.user
            self.fields['client'].disabled = True

    def save(self, commit=True):
        order = super().save(commit=False)
        if commit:
            order.save()
            self.save_m2m()
            total_amount = sum(product.price for product in order.products.all())
            order.total_amount = total_amount
            order.save()
        return order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # fields = '__all__'
        fields = ['name', 'description', 'price', 'quantity', 'photo']


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class ClientForm(forms.Form):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Телефон', max_length=15)
    address_city = forms.CharField(label='Город', max_length=100)

    def save(self):
        cleaned_data = self.cleaned_data
        user = User.objects.create_user(
            username=cleaned_data['email'],
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            email=cleaned_data['email'],
            password=None  # Пароль не обязателен (для примера)
        )
        Profile.objects.create(
            user=user,
            first_name=cleaned_data['first_name'],
            last_name=cleaned_data['last_name'],
            email=cleaned_data['email'],
            phone_number=cleaned_data['phone_number'],
            address_city=cleaned_data['address_city']
        )
        return user



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='Имя')
    last_name = forms.CharField(required=True, label='Фамилия')
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = Profile
        # fields = ['phone_number', 'address_city']
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address_city']

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        user.save()
        if commit:
            profile.save()
        return profile