from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from store.models import WishlistItem,CartItem
from .models import UserProfile,AddressD
# Create your views here.

def profile(request):
   user = UserProfile.objects.filter(id = request.user.id)
   wishitem = WishlistItem.objects.filter(id = request.user.id)
   cartitem = CartItem.objects.filter(id = request.user.id)
   wish = wishitem.count()
   cart = cartitem.count()
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
    if request.method=="POST":
        name = request.POST['name']
        hno = request.POST['hno']
        stno = request.POST['stno']
        city = request.POST['city']
        state = request.POST['state']
        country = request.POST['country']
        zipcode = request.POST['zipcode']
        phone = request.POST['phone']
        address = AddressD.objects.create(user=request.user)
        address.Title = name
        address.flatno = hno
        address.street=stno
        address.city=city
        address.state=state
        address.country = country
        address.pincode = zipcode
        if phone:
            address.user.phone = phone
        else:
            pass
        address.save()
        return redirect('checkout')
    return render(request,'store/address_form.html')