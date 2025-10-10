from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from store.models import WishlistItem,CartItem
from .models import UserProfile,AddressD
# Create your views here.

def profile(request):
   user = UserProfile.objects.filter(id = request.user.id)
   wishitem = WishlistItem.objects.filter(id = request.user.id)
   cartitem = CartItem.objects.filter(id = request.user.id)
   addresses = AddressD.objects.filter(user=user)
   print(addresses)
   wish = wishitem.count()
   cart = cartitem.count()
#    print(user[0].img.url)
   return render(request,'userprofile/profile.html',{'user':user[0],'wish':wish,'cart':cart,'addresses':addresses})

def update_profile(request):
    myuser = UserProfile.objects.get(username = request.user.username)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob'] 
        image = request.FILES.get('image')
        phone = request.POST['phone'] 
        Gender = request.POST.get('gender') 
        print(image)
        # text = name.split()
        # if text[0]:
        #     myuser[0].first_name=text[0]
        # else:
        #     pass
        # if text[1]:
        #     myuser[0].last_name=text[1]
        # else:
        #     pass
        if image:
            myuser.img = image
        else:
            pass
        if dob:
            myuser.email = email
        else:
            pass
        if phone:
            myuser.phone = phone
        else:
            pass
        if Gender:
            myuser.gender = Gender
        else:
            pass

        # print(myuser.img, "myuser")
        
        myuser.save()
        return redirect('profile')
    return render(request,'userprofile/update_profile.html', {'user':myuser})

def add_address(request):
    user = UserProfile.objects.filter(username=request.user.username).first()
    print(user)
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name', '').strip()
        hno = request.POST.get('hno', '').strip()
        stno = request.POST.get('stno', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        country = request.POST.get('country', '').strip()
        zipcode = request.POST.get('zipcode', '').strip()
        phone = request.POST.get('phone', '').strip()
        
        # Create and populate address
        address = AddressD.objects.create(
            user=user,
            Title=name,
            flatno=hno,
            street=stno,
            city=city,
            state=state,
            country=country,
            pincode=zipcode
        )
        address.save()
        if phone:
            request.user.phone = phone
            request.user.save()
        return redirect('checkout')
    
    return render(request, 'store/address_form.html')