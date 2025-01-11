from django.core.management.base import BaseCommand
from shop.models import Category, Product, ProductImage, Review, PriceHistory
import random
import uuid
from faker import Faker

fake = Faker()

def populate():
    print("Начало заполнения базы данных...")
    
    # Удаление старых данных
    Category.objects.all().delete()
    Product.objects.all().delete()
    ProductImage.objects.all().delete()
    Review.objects.all().delete()
    PriceHistory.objects.all().delete()

    # Создание категорий
    categories = []
    for _ in range(5):
        category = Category.objects.create(
            name=fake.word().capitalize(),
            slug=fake.slug(),
        )
        categories.append(category)

    # Создание товаров
    for _ in range(50):
        product = Product.objects.create(
            name=fake.word().capitalize(),
            description=fake.text(max_nb_chars=200),
            price=round(random.uniform(10, 1000), 2),
            category=random.choice(categories),
            stock=random.randint(10, 100),
            sku=str(uuid.uuid4())[:8],
            warranty_period=f"{random.randint(1, 24)} месяцев",
            slug=fake.slug(),
        )
        # Добавление изображений
        for _ in range(random.randint(1, 3)):
            image = ProductImage.objects.create(
                image=None,  # Здесь можно заменить на путь к изображению
                alt_text=fake.sentence(nb_words=5),
            )
            product.images.add(image)

    print("Заполнение базы данных завершено.")

class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными"

    def handle(self, *args, **kwargs):
        populate()
        self.stdout.write(self.style.SUCCESS("База данных успешно заполнена!"))
