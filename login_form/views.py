from django.shortcuts import render,redirect
from userprofile.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage
from .tokens import generate_tokens
# Create your views here.
def signup(request):
    if request.method=="POST":
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        con_password = request.POST['con_password']
        role = request.POST['role']
        if password!=con_password:
            messages.error(request,'password are not same')
            return render(request,'login_form/signup.html')
        
        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, 'login_form/signup.html')
        
        myuser = UserProfile.objects.create_user(username=username, email=email,password=password)
        # myuser.password = password
        if role == "Seller":
            myuser.is_vendor = True
        myuser.first_name=name
        myuser.is_active=True

        myuser.save()
        messages.success(request,"user successfully created")

        # sending confirmation  mail
        subject = "Welcome to the Eshop"
        message = "Hello "+myuser.first_name+"\n "+" this is the onfirmation that you have signin on Eshop"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list)
        current_site = get_current_site(request)
        email_subject = "Confirm your email!! This mail is to confirm your login"
        message2 = render_to_string('login_form/email_confirmation.html',{
            'name':myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_tokens.make_token(myuser), 
        })

        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently=True
        email.send()
        return redirect('signin')
    return render(request, 'login_form/signup.html')
    # else:
        
def signout(request):
    logout(request)
    # request.session.flush()
    return redirect('signin')

def signin(request):
   if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username,password=password)
        if user is not None:
            user.is_active=True
            login(request,user)
            f_name = user.first_name
            context={
                "fname":f_name
            }
            return render(request,'store/store.html',context)
        else:
            messages.error(request, "incorrect password or username")
            return redirect('signin')
    
   return render(request,'login_form/signin.html')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_tokens.check_token(myuser, token):
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('store')
    else:
        return render(request, 'activation_failed.html')

