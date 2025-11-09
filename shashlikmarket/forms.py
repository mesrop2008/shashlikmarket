from django import forms
import re
from django.core.exceptions import ValidationError
class OrderForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100, 
        label='Ваше имя',
        widget=forms.TextInput(attrs={'class': 'w-full border px-3 py-2 rounded', 'placeholder': 'Введите ваше имя'})
    )
    
    customer_phone = forms.CharField(
        max_length=20,
        label='Ваш телефон', 
        widget=forms.TextInput(attrs={'class': 'w-full border px-3 py-2 rounded', 'placeholder': '+7 (___) ___-__-__'})
    )

    DELIVERY_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
    ]
    
    delivery_type = forms.ChoiceField(
        choices=DELIVERY_CHOICES,
        label='Способ получения',
        widget=forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded'})  
    )

    customer_address = forms.CharField(
        max_length=100,
        label='Адрес доставки', 
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full border px-3 py-2 rounded', 'placeholder': 'Улица, дом, квартира'})
    )

    PAY_CHOICES = [
        ('cash', 'Наличными курьеру'),
        ('card', 'Переводом курьеру')
    ]

    pay_type = forms.ChoiceField(
        choices=PAY_CHOICES,
        label='Способ оплаты',
        widget=forms.Select(attrs={'class': 'w-full border px-3 py-2 rounded'}) 
    )

    def clean_customer_phone(self):
        phone = self.cleaned_data.get('customer_phone', '').strip()

        # Удаляем пробелы, дефисы и скобки
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)

        # Разрешаем форматы, начинающиеся с +7, 7 или 8
        if re.match(r'^\+?7\d{10}$', clean_phone):
            normalized_phone = '+7' + clean_phone[-10:]
        elif re.match(r'^8\d{10}$', clean_phone):
            normalized_phone = '+7' + clean_phone[1:]
        else:
            raise ValidationError(
                'Введите корректный номер: +7 (XXX) XXX-XX-XX или 8XXXXXXXXXX'
            )

        return normalized_phone
    def clean(self):
        cleaned_data = super().clean()
        delivery_type = cleaned_data.get('delivery_type')
        customer_address = cleaned_data.get('customer_address')

        # Require address for delivery
        if delivery_type == 'delivery' and not customer_address:
            raise ValidationError({
                'customer_address': 'Укажите адрес для доставки'
            })

        return cleaned_data

