from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from .models import Products,Category,CartItem,WishlistItem
from django.contrib.auth.models import User
from django.db.models import Q
from userprofile.models import Orders,AddressD


# Create your views here.
def home(request):
    prod = Products.objects.all()
    context ={
        'products':prod
    } 
    return render(request ,'store/store.html',context)


def shop(request):
    categories=Category.objects.all()
    products = Products.objects.all()
    context={
        'categories':categories,
        'products':products
    }
    return render(request ,'store/shop.html',context=context)


def about(request):
    return render(request ,'store/about.html')



def blog(request):
    return render(request ,'store/blog.html')



def blog_details(request):
    return render(request ,'store/blog-details.html')



def contact(request):
    return render(request,'store/contact.html')



def checkout(request):
    cartitem = CartItem.objects.filter(user= request.user)
    total_price  = sum(item.product.price*item.quantity for item in cartitem)
    # order = Orders.objects.filter(user = request.user )
    Address  = AddressD.objects.filter(user = request.user).first()
    context={"cartitem":cartitem, 'total':total_price,'address':Address}
    print(Address)
    return render(request,'store/checkout.html',context)



def shop_details(request,slug):
    pro = get_object_or_404(Products, slug=slug)
    # pro = Products.objects.get(slug)
    cat=pro.category
    pro_cat = Products.objects.filter(category=cat)
    context = {
        'pro':pro ,
        'related':pro_cat
    }
    return render(request ,'store/shop-details.html',context)



def product_detail(request, slug):
    """
    
    """
    product = get_object_or_404(Products, slug=slug)
    category_item = Products.objects.filter(category=product.category)
    # p_id = product.id
    cartitem = CartItem.objects.filter(user=request.user,product=product).exists()
    # pro=cartitem.id
    wishitem = WishlistItem.objects.filter(user=request.user,product=product).exists()

    return render(request, 'store/shop-details.html', {'product': product, 'cartitem':cartitem, 'wishitem':wishitem, 'related':category_item })

def category_products(request, slug):
    category_title = get_object_or_404(Category,slug=slug)
    products = Products.objects.filter(category=category_title)
    return render(request, 'store/category_details.html', {
        'category': category_title,
        'products': products,
        'categories':Category.objects.all()
    })


def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    # price = [items.quantity*items.product.price for items in cart_items]
    total_price  = sum(item.product.price*item.quantity for item in cart_items)
    context = {
        # 'price':price,
        'cart_items':cart_items,
        'total_price':total_price
    }
    return render(request, 'store/shopping-cart.html',context)

def add_cart(request,product_id):
    product = Products.objects.get(id=product_id)
    product_slug = Products.objects.get(id=product_id)
    slug = product_slug.slug
    cart_item, created = CartItem.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('product_detail',slug)


def remove_cart(request,product_id):
    cart_item = CartItem.objects.get(id = product_id)

    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def quan_add(request,product_id):
    cart_item = CartItem.objects.get(id = product_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def wish(request):
    wishitem = WishlistItem.objects.filter(user=request.user)
    context={
        'wishitem': wishitem
    }
    return render(request, 'store/wishlish.html', context=context)

def add_wish(request,product_id):
    product = Products.objects.get(id=product_id)
    product_slug = Products.objects.get(id=product_id)
    slug = product_slug.slug
    wishitem,created= WishlistItem.objects.get_or_create(product=product,user=request.user)
    wishitem.save()
    return redirect('product_detail',slug)



def rem_wish(request,product_id):
    wishlist = WishlistItem.objects.filter(id=product_id)
    wishlist.delete()
    return redirect('wish')

def clear_cart(request):
    products = CartItem.objects.all()
    # product = products.product
    products.delete()
    return redirect('cart')

def wish_cart(request,product_id):
    # rem_wish(request,product_id)
    wishitem = WishlistItem.objects.get(id=product_id)
    pro_id = wishitem.product.id
    wishitem.delete()
    
    product = Products.objects.get(id = pro_id)
    cartitem,created= CartItem.objects.get_or_create(product=product,user = request.user)
    cartitem.quantity=1
    cartitem.save()
    return redirect('wish')

def search(request):
    if request.method=='POST':
        query = request.POST.get('search','')
        products = Products.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        return render(request, 'store/shop.html', {
            'products': products,
            'categories': Category.objects.all(),
            'search_query': query
        })
    return redirect('shop')

def prfl(request,ran):
    rb = ran.split('-')
    print(rb[0],rb[1])
    product = Products.objects.filter(price__range=(rb[0],rb[1]))
    # print(product[0].title)
    return render(request,'store/category_details.html',{'products': product,'categories':Category.objects.all()})



# Loggers 
