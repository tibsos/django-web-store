# shop/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from .models import Category, Product, Cart, Favorite, CartItem
from django.http import HttpResponseRedirect

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
        products = products.filter(name__icontains=search_query)
    
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
    })

# Страница с товарами категории и подкатегории
def category_products(request, slug):
    categories = get_categories()
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
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

# Страница корзины
@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    
    # Вычисляем общую цену корзины и итоговую цену каждого товара
    total_price = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # Итоговая цена для каждого товара
        total_price += item.total_price  # Общая сумма корзины
    
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
