# shop/models.py
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True, verbose_name="URL-метка")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Изображение категории")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name="Родительская категория")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    stock = models.IntegerField(verbose_name="Количество в наличии")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Артикул")
    warranty_period = models.CharField(max_length=100, blank=True, verbose_name="Гарантийный срок")
    dimensions = models.JSONField(blank=True, null=True, verbose_name="Габариты товара")  # Высота, вес, длина и т.д.
    characteristics = models.JSONField(blank=True, null=True, verbose_name="Характеристики товара")  # Дополнительные характеристики
    images = models.ManyToManyField('ProductImage', blank=True, verbose_name="Изображения товара")
    related_products = models.ManyToManyField('self', blank=True, symmetrical=False, verbose_name="Похожие товары")  # Похожие товары
    slug = models.SlugField(unique=True, verbose_name="URL-метка")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='products/', verbose_name="Изображение")
    alt_text = models.CharField(max_length=255, blank=True, verbose_name="Текст для изображения")

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return self.alt_text if self.alt_text else f"Image {self.id}"


class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history', verbose_name="Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")

    class Meta:
        verbose_name = "История цен"
        verbose_name_plural = "История цен"
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.product.name} - {self.price} с {self.start_date} по {self.end_date or 'настоящее время'}"


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Review {self.id} - {self.rating} stars"


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    customer_name = models.CharField(max_length=200, verbose_name="Имя клиента")
    customer_email = models.EmailField(verbose_name="Электронная почта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Корзина {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        # Убедитесь, что total_price не сохраняется напрямую
        super().save(*args, **kwargs)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Избранное: {self.product.name} для {self.user.username}"

    @classmethod
    def toggle_favorite(cls, user, product):
        favorite, created = cls.objects.get_or_create(user=user, product=product)
        if not created:
            favorite.delete()
            return {'success': True, 'action': 'removed'}
        return {'success': True, 'action': 'added'}
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop_profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username
