# shop/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Главная страница с товарами и категориями
    path('', views.product_list, name='product_list'),

    # Страница категории с товарами
    path('category/<slug:slug>/', views.category_products, name='category_products'),

    # Страница подробного описания товара
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # Страница корзины
    path('cart/', views.cart, name='cart'),

    # Страница избранного
    path('favorites/', views.favorites, name='favorites'),

    # Страница профиля пользователя
    path('profile/', views.profile, name='profile'),

    path('cart/', views.cart, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Добавляем путь для редактирования профиля

    path('profile/change-password/', auth_views.PasswordChangeView.as_view(), name='change_password'),
]
