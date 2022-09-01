from django.shortcuts import render,HttpResponse,redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegisterForm
# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            if email_not_present(email):
                form.save()
                messages.success(request,f'Account created Successfully for {username}!')
                return redirect('login')
            else:
                form = UserRegisterForm()
                return render(request, 'users/signup.html', {'form': form,'checker':1,'username':username,'email':email})

    else:
        form = UserRegisterForm()
    return render(request,'users/signup.html',{'form':form})


def email_not_present(em):
    if User.objects.filter(email=em).exists():
        return False
    else:
        return True