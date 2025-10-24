from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import stripe
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from .models import Products,Category,CartItem,WishlistItem, Seller
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from userprofile.models import Orders,AddressD
# from .models import Seller
from userprofile.models import UserProfile

# Create your views here.
def home(request):
    print(request.user.is_vendor)
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
    Address  = AddressD.objects.filter(user = request.user)
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


def seller_pro(request):
        
        if request.user.is_vendor:
            try:
                seller = Seller.objects.get(user=request.user)
                print(seller)
            except Seller.DoesNotExist:
                return redirect("store")
            products = Products.objects.filter(seller=seller)
            # print()
            print(seller.user.id)
            print(seller.user.is_authenticated)
            context = { 
                "user": seller,
                "products": products,
            }
            return render(request, "store/profile_ven.html", context)
        return redirect("store")


stripe.api_key = settings.STRIPE_SECRET_KEY
def create_checkout_session(request):
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Your Product Name',
                    },
                    'unit_amount': 2000,  # price in cents
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='https://your-domain.com/success/',
        cancel_url='https://your-domain.com/cancel/',
    )
    return JsonResponse({'id': checkout_session.id})




<<<<<<< HEAD
=======
def payment_success(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price  = sum(item.product.price*item.quantity for item in cart_items)*100
    intent = stripe.PaymentIntent.create(amount=total_price,currency="inr",metadata={"user_id": str(request.user.id)})
    adress = AddressD.objects.create(user=request.user,Title="Home",flatno="239/5",street='neear soni temple',city='Ajmer',state='Rajasthan',country='India',pincode=305001)
    t_id  = intent.id
    order = Orders.objects.create(buyer=request.user,seller=request.user,address=adress,Transaction_id = t_id)
    print(order.Transaction_id)
    return render(request, 'store/payment_success.html')
>>>>>>> 8544a79 (final commit on payment gateway)


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': 'Invalid signature'}, status=400)
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase...
    return JsonResponse({'status': 'success'})




# Loggers 
