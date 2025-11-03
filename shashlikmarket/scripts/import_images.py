import os
import sys
import django
import cloudinary.uploader

sys.path.append(r'C:\Users\mesrop\Desktop\shaslikmarket\shaslikmarket\mysite')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from shashlikmarket.models import Products 


STATIC_IMAGES = r'C:\Users\mesrop\Desktop\shaslikmarket\shaslikmarket\mysite\shashlikmarket\static\images'


print(f"Ищем файлы в: {STATIC_IMAGES}")

for product in Products.objects.all():
    if product.imagepath:
        filename = os.path.basename(product.imagepath)
        local_path = os.path.join(STATIC_IMAGES, filename)
        
        print(f"Проверяем: {local_path}")
        
        if os.path.exists(local_path):
            result = cloudinary.uploader.upload(local_path, folder="products")
            url = result["secure_url"]
            product.imagepath = url
            product.save(update_fields=["imagepath"])
            print(f"✓ {product.name} → {url}")
        else:
            print(f"✗ Файл {filename} не найден")