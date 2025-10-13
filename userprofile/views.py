from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from store.models import WishlistItem,CartItem
from .models import UserProfile,AddressD
# Create your views here.

def profile(request):
   user = UserProfile.objects.filter(id = request.user.id)
   wishitem = WishlistItem.objects.filter(user = request.user)
   cartitem = CartItem.objects.filter(user = request.user)
   addr = AddressD.objects.filter(user = request.user)
   wish = wishitem.count()
   cart = cartitem.count()
   print(addr)
#    print(user[0].img.url)
   return render(request,'userprofile/profile.html',{'user':user[0],'wish':wish,'cart':cart})

def update_profile(request):
    myuser = UserProfile.objects.get(username = request.user.username)
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob'] 
        image = request.FILES.get('image')
        phone = request.POST['phone'] 
        Gender = request.POST.get('gender') 
        # print(image)
        text = name.split()
        if len(text)==2:
                myuser.first_name=text[0]
                myuser.last_name=text[1]
        myuser.first_name=name
            
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
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        hno = request.POST.get('hno', '').strip()
        stno = request.POST.get('stno', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        country = request.POST.get('country', '').strip()
        zipcode = request.POST.get('zipcode', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Create address
        address = AddressD.objects.create(
            user=request.user,
            Title=name,
            flatno=hno,
            street=stno,
            city=city,
            state=state,
            country=country,
            pincode=zipcode
        )

        # Update phone if provided
        if phone:
            user_profile = request.user
            user_profile.phone = phone
            user_profile.save()

        return redirect('checkout')

    return render(request, 'store/address_form.html')
