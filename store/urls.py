from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from userprofile import views as view1

# app_name='store'

urlpatterns = [
    path('',views.home,name='store'),
    path('shop/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('blog-details/', views.blog_details, name='blog-details'),
    path('contact/', views.contact, name='contact'),
    path('cart/', views.cart, name='cart'),
    path('add/<int:product_id>', views.add_cart, name='add-cart'),
    path('rem/<int:product_id>', views.remove_cart, name='rem-cart'),
    path('qua/<int:product_id>', views.quan_add, name='quancart'),
    path('wish/',views.wish,name='wish'),
    path('addwish/<int:product_id>', views.add_wish,name='addwish'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop-details/', views.shop_details, name='shop-details'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_products, name='category-products'),
    path('remwish/<int:product_id>', views.rem_wish,name='remitem'),
    path('wish_cart/<int:product_id>', views.wish_cart,name='wish-cart'),
    path('clearcart/',views.clear_cart,name='clear-cart'),
    path('shop/search/',views.search,name='search'),
    # path('/search/',views.search,name='search'),
    path('<slug:slug>/search/',views.search,name='search'),
    path('filter/<str:ran>/', views.prfl,name="price-filter"),
    path('checkout/', views.checkout,name='Buy'),
    path('checkout/create_checkout_session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancel/', views.payment_cancel, name='payment_cancel')
    # path('profile/',view1.profile,name='profile')
    # path()
    # path('shop-details/<slug:slug>/', views.product_detail, name='product_detail'),
    # path('cart/', views.cart, name='cart'),
    # path('product/<int:id>/', views.product_detail, name='product-detail'),
]
