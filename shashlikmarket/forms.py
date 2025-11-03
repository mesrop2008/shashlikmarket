from django import forms

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