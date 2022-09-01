from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from . forms import Profileform,Productform,Orderform
from . models import Profile,Product,Order,Comment
from . import signals
import json
from .models import comp,report
from . import forms, models
from .forms import StaffUserForm
from django.contrib.auth.models import Group
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='1':
            usercheck=True
            prod=Product.objects.all()
            order=Order.objects.filter(user=request.user)
            return render(request,"Portal/index.html",{'usercheck':usercheck,'order':order,'prod':prod})
        else:
            usercheck=False
            form=Productform()
            if request.method=="POST":
                form=Productform(request.POST,request.FILES)
                if form.is_valid():
                    instance=form.save(commit=False)
                    instance.user=request.user
                    instance.save()
                    messages.success(request,'Product was added successfully!')
                    return redirect('farmerproducts')
            return render(request,"Portal/index.html",{'usercheck':usercheck,'form':form})
    return render(request,"Portal/index.html")

def profile(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        form = Profileform(instance=profile)
        if request.method=="POST":
            form = Profileform(request.POST,instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request,'Your profile was saved succesfully !')
                return redirect('index')
        if(len(profile.first_name)>0):
            if profile.usertype=='1':
                order=Order.objects.filter(user=request.user)
                return render(request, 'Portal/profile.html', {'form': form,'profcheck':True,'order':order,'usercheck':True})
            else:
                return render(request, 'Portal/profile.html', {'form': form,'profcheck':True,'usercheck':False})
        else:
            return render(request, 'Portal/profile.html', {'form': form})
    else:
        return render(request, 'Portal/profile.html')

def cart(request,id=0):
    products=Product.objects.all()
    form=Orderform()
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='1':
            order=Order.objects.filter(user=request.user)
            if request.method == "GET":
                if id==0:
                    form = Orderform()
                    return render(request, 'Portal/cart.html',{'products': products, 'order': order, 'form': form,'usercheck':True})
                else:
                    if Order.objects.filter(pk=id,user=request.user).exists():
                        order1 = Order.objects.get(pk=id)
                        form = Orderform(instance=order1)
                        return render(request, 'Portal/cart.html', {'products': products, 'order':order,'form': form,'checker':1,'usercheck':True})
                    else:
                        return render(request, 'Portal/cart.html', {'products': products, 'order':order,'form': form,'usercheck':True})
            else:
                if id != 0:
                    order1 = Order.objects.get(pk=id)
                    form = Orderform(request.POST, instance=order1)
                    if form.is_valid():
                        form.save()
                        messages.success(request,'Your address was changed succesfully !')
                        return redirect('order')#order
                    return render(request, 'Portal/cart.html', {'products': products,'order':order,'form': form,'usercheck':True})
                else:
                    form = Orderform(request.POST)
                    if form.is_valid():
                        instance=form.save(commit=False)
                        instance.user=request.user
                        instance.save()
                        messages.success(request,'Your order is Placed Successfully ! It will be delivered within 10 days !')
                        return redirect('index')
                    return render(request, 'Portal/cart.html', {'products': products, 'form': form,'usercheck':True})
        else:
            return render(request, 'Portal/notallowed.html')
    return render(request, 'Portal/notallowed.html')


def order(request):
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='1':
            products = Product.objects.all()
            order = Order.objects.filter(user=request.user)
            order_list=[]
            id_list=[]
            tot_list=[]
            for i in order:
                id_list.append(i.id)
                str=i.data
                tot=i.total
                tot_list.append(tot)
                str_list=str.split(";")
                str_list.pop()
                dict_list = []
                for i in str_list:
                    dic=json.loads(i)
                    dict_list.append(dic)
                order_list.append(dict_list)
            # print(id_list)
            mylist=list(zip(order_list,id_list,tot_list))
            # print(mylist)
            # print(order_list)
            # i=1
            # for x in order_list:
            #     print('Order - ',i)
            #     i=i+1
            #     for y in x:
            #         print(y)
            return render(request,'Portal/myorders.html',{'products':products,'order':order,'mylist':mylist,'usercheck':True})
        else:
            return render(request,'Portal/notallowed.html')
    else:
        return render(request,'Portal/notallowed.html')


def cancel(request,id=0):
    if id!=0:
        if Order.objects.filter(pk=id).exists():
            Order.objects.get(pk=id).delete()
    return redirect('order')


def farmerorder(request):
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='2':
            farmerorders=Order.objects.all()
            order_list=[]
            customer_name_list=[]
            email_list=[]
            address_list=[]
            address_line_2_list=[]
            city_list=[]
            state_list=[]
            pin_code_list=[]
            phone_number_list=[]
            my_list=[]
            user=request.user
            user=str(user)
            for i in farmerorders:
                str1=i.data
                str_list=str1.split(";")
                str_list.pop()
                dict_list = []
                for k in str_list:
                    dic=json.loads(k)
                    dict_list.append(dic)
                order_list.append(dict_list)
                customer_name_list.append(i.name)
                email_list.append(i.email)
                address_list.append(i.address)
                address_line_2_list.append(i.address_line_2)
                city_list.append(i.city)
                state_list.append(i.state)
                pin_code_list.append(i.pin_code)
                phone_number_list.append(i.phone_number)
                
                my_list=list(zip(customer_name_list,email_list,address_list,address_line_2_list,city_list,state_list,pin_code_list,phone_number_list,order_list))
            # print(my_list)
            # print('ok')
            for x in my_list:
                x[8][:] = [y for y in x[8] if y.get('farmerusername') == user]
            #print(my_list)
            # for x in my_list:
            #     print(x[8])
            #     if(len(x[8])==0):
            #         my_list.remove(x)
            my_list[:]=[x for x in my_list if len(x[8])!=0]
            #print(my_list)
            return render(request,'Portal/yourorders.html',{'usercheck':False,'my_list':my_list})
        else:
            return render(request,'Portal/notallowed.html',{'usercheck':True})
    else:
        return render(request,'Portal/notallowed.html')



def farmerproducts(request,id=0):
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='2':
            prod=Product.objects.filter(user=request.user)
            if request.method=="GET":
                if id==0:
                    return render(request,'Portal/farmerproducts.html',{'prod':prod})
                else:
                    if Product.objects.filter(pk=id,user=request.user).exists():
                        prod1 = Product.objects.get(pk=id)
                        form = Productform(instance=prod1)
                        return render(request,'Portal/farmerproducts.html',{'form':form,'checker':1})
                    else:
                        return render(request,'Portal/farmerproducts.html',{'prod':prod})
            else:
                if id!=0:
                    prod1 = Product.objects.get(pk=id)
                    form = Productform(request.POST, request.FILES,instance=prod1)
                    if form.is_valid():
                        form.save()
                        messages.success(request,'Your product was changed succesfully !')
                        return redirect('farmerproducts')
                    return render(request,'Portal/farmerproducts.html',{'prod':prod,'form':form,'checker':1})
                else:
                    return render(request,'Portal/farmerproducts.html',{'prod':prod})
        else:
            return render(request,'Portal/notallowed.html',{'usercheck':True})
    else:
        return render(request,'Portal/notallowed.html')


def delprod(request,id=0):
    if id!=0:
        if Product.objects.filter(pk=id,user=request.user).exists():
            Product.objects.get(pk=id).delete()
    return redirect('farmerproducts')

def about(request):
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='1':
            order = Order.objects.filter(user=request.user)
            return render(request,"Portal/about.html",{'order':order,'usercheck':True})
        else:
            return render(request,"Portal/about.html",{'usercheck':False})
    else:
         return render(request,"Portal/about.html")

def contact(request):
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='1':
            order = Order.objects.filter(user=request.user)
            if(request.method=='POST'):
                name=request.POST['name']
                email=request.POST['email']
                subject=request.POST['sub']
                message=request.POST['message']
                mess_info=Comment(name=name,email=email,subject=subject,message=message)
                mess_info.save()
                messages.success(request, 'Your message sent succesfully !')
            return render(request,"Portal/contact.html",{'order':order,'usercheck':True})
        else:
            if(request.method=='POST'):
                name=request.POST['name']
                email=request.POST['email']
                subject=request.POST['sub']
                message=request.POST['message']
                mess_info=Comment(name=name,email=email,subject=subject,message=message)
                mess_info.save()
                messages.success(request, 'Your message sent succesfully !')
            return render(request,"Portal/contact.html",{'usercheck':False})
    else:
        messages.warning(request, 'Your are requested to login !')
        return render(request,"Portal/contact.html")





def add_staff(request):
    if request.user.is_authenticated:
        prof=Profile.objects.get(user=request.user)
        if prof.usertype=='2':
            userForm= forms.StaffUserForm()
            mydict={'userForm':userForm}
            if request.method=='POST':

                userForm= forms.StaffUserForm(request.POST)
                if userForm.is_valid():
                    user=userForm.save()
                    user.set_password(user.password)
                    user.save()
                    print(user)

                    my_worker_group = Group.objects.get_or_create(name='STAFF')
                    my_worker_group[0].user_set.add(user)
                    messages.success(request, 'Your staff account created successfully!')
                return render(request, 'staff_signup.html', context=mydict)
           # messages.success(request, 'Your staff account created successfully!')
            return render(request,'staff_signup.html',context=mydict)
        #messages.success(request, 'Your staff account created successfully!')
        return render(request, 'notfound.html')

def is_staff(user):
    return user.groups.filter(name='STAFF').exists()



def afterlogin_view(request):
    if is_staff(request.user):
        return redirect('staff-dashboard')

@login_required(login_url='login')
@user_passes_test(is_staff)
def staff_dashboard(request):
    return render(request,'Portal/staff_dashboard.html')

def viewworkers(request):
    products=models.Profile.objects.all()
    return render(request,'viewcustomers.html',{'products':products})

def viewproducts(request):
    products=models.Product.objects.all()
    return render(request,'viewproducts.html',{'products':products})

def a(request):
    return render(request,'1.html')





def add_comp(request):
    if request.method == "POST":
        jbtitle = request.POST.get('jbtitle')

        jbname = request.POST.get('jbname')
        jbdes = request.POST.get('jbdes')


        comp(jbtitle=jbtitle, jbdes=jbdes, jbname=jbname).save()
        return render(request, 'success.html')
    return render(request, 'addcomp.html')



def viewcomp(request):
    job_view = comp.objects.all() #.filter(status=True)
    return render(request, 'viewcomp.html', {'job_view': job_view})


def add_report(request):
    if request.method == "POST":
        jbtitle = request.POST.get('jbtitle')
        jbname = request.POST.get('jbname')
        jbdes = request.POST.get('jbdes')
        report(jbtitle=jbtitle, jbdes=jbdes, jbname=jbname).save()
        return render(request, 'Portal/staff_dashboard.html')
    return render(request, 'addreport.html')


def viewreport(request):
    job_view = report.objects.all() #.filter(status=True)
    return render(request, 'viewcomp.html', {'job_view': job_view})
