from django.shortcuts import render
from app.forms import *
from app.models import *
from django.http import HttpResponse

from django.core.mail import send_mail
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required




# Create your views here.






def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufd.is_valid() and pfd.is_valid():
            NSUO=ufd.save(commit=False)
            password=ufd.cleaned_data['password']
            NSUO.set_password(password)
            NSUO.save()



            NSPO=pfd.save(commit=False)
            NSPO.username=NSUO
            NSPO.save()




            

            send_mail('Login confirmation',
                        'This is Sreenu' ,
                        'sreenusre77@gmail.com',
                        [NSUO.email],
                        fail_silently=False)



           
            return HttpResponse('user registration is done successfull')
        else:
            return HttpResponse('Not valid user information')

    return render(request,'registration.html',d)








def home(request):
    
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('In valid userdata')

    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



