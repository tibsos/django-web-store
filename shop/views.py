# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from .models import Category, Product, Cart, Favorite, CartItem
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib import messages
from .forms import CheckoutForm

from django.db.models import Avg
from .models import Product, Review
from .forms import ReviewForm

# Получаем категории для отображения в боковой панели
def get_categories():
    return Category.objects.all()

# Главная страница с товарами и категориями
def product_list(request):
    categories = get_categories()  # Получаем все категории
    products = Product.objects.all()
    
    # Поиск товаров по запросу
    search_query = request.GET.get('q', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |  # Поиск по названию
            Q(sku__icontains=search_query) |  # Поиск по артикулу
            Q(description__icontains=search_query)  # Поиск по описанию
        )
    
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,  # Передаем запрос для отображения в поле ввода
    })

# Страница с товарами категории и подкатегории
def category_products(request, slug=None):
    # Получаем все категории
    categories = get_categories()
    
    # Если slug передан, находим категорию по slug, иначе используем дефолтное значение
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category=category)
    else:
        category = None
        products = Product.objects.all()  # Получаем все продукты, если категория не выбрана

    # Фильтрация по выбранной категории из GET-запроса
    selected_category = request.GET.get('category')
    if selected_category:
        category = get_object_or_404(Category, slug=selected_category)
        products = products.filter(category=category)

    return render(request, 'category_products.html', {
        'category': category,
        'products': products,
        'categories': categories
    })

# Страница подробного описания товара
def product_detail(request, slug):
    categories = get_categories()
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.all()  # Отзывы товара
    price_history = product.price_history.all()  # История цен
    
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'price_history': price_history,
        'categories': categories
    })

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    # Вычисляем общую цену корзины и итоговую цену каждого товара
    total_price = 0
    for item in cart_items:
        total_price += item.total_price  # Используем геттер для total_price

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


# Обновление количества товара в корзине
@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        cart_item.quantity = quantity
        cart_item.save()
    
    return redirect('cart')

# Удаление товара из корзины
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    return redirect('cart')

# Страница избранного
@login_required
def favorites(request):
    categories = get_categories()
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites.html', {
        'favorites': favorites,
        'categories': categories
    })

# Страница профиля пользователя
@login_required
def profile(request):
    categories = get_categories()
    return render(request, 'profile.html', {
        'user': request.user,
        'categories': categories
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # После сохранения перенаправляем обратно в профиль
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Возвращаем JSON-ответ
    return HttpResponse("K")

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    # Вычисляем общую сумму корзины
    total_price = sum([item.product.price * item.quantity for item in cart_items])
    
    # Если корзина пуста, перенаправляем на страницу товаров
    if not cart_items:
        messages.error(request, "Ваша корзина пуста.")
        return redirect('product_list')

    # Обрабатываем форму оформления заказа
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Здесь логика для создания заказа, сохранения данных и т.д.
            # Например, создаем объект Order и сохраняем информацию
            # Очищаем корзину после оформления
            cart.cartitem_set.all().delete()
            messages.success(request, "Ваш заказ успешно оформлен!")
            return redirect('order_complete')  # Можно перенаправить на страницу подтверждения
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

def order_complete(request):
    return render(request, 'order_complete.html')

def product_detail(request, slug):
    # Fetch the product by slug
    product = get_object_or_404(Product, slug=slug)
    reviews = Review.objects.filter(product=product).order_by('-created_at')  # Сортировка отзывов по дате (новые сначала)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    # Обработка формы отзыва
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', slug=product.slug)  # Редирект с использованием slug
    else:
        form = ReviewForm()

    # Контекст для шаблона
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': round(average_rating, 1),  # Округление рейтинга до одного знака после запятой
        'form': form,
        'total_reviews': reviews.count(),  # Добавлено общее количество отзывов
    }

    return render(request, 'product_detail.html', context)