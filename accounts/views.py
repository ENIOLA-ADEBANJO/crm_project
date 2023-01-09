from django.shortcuts import render, redirect
from .models import *
from .form import *
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout,login
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .decorator import *
from django.contrib.auth.models import Group
# Create your views here.

@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f'Succesfully registered {username}')
            return redirect('login')
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def dashboard(request):
    order = Order.objects.all()
    customer = Customer.objects.all()
    total_order  = order.count()
    order_delivered  = order.filter(status='Delivered').count()
    order_pending  = order.filter(status='Pending').count()
    context = {
        'customer': customer,
        'order': order,
        'total_order': total_order,
        'order_delivered': order_delivered,
        'order_pending': order_pending,
    }
    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    order = request.user.customer.order_set.all()
    total_order  = order.count()
    order_delivered  = order.filter(status='Delivered').count()
    order_pending  = order.filter(status='Pending').count()
    print('ORDERS:', order)
    context = {
        'order': order,
        'total_order': total_order,
        'order_delivered': order_delivered,
        'order_pending': order_pending,
    }
    return render(request, 'accounts/user.html', context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_setting(request):
# This gets the current user that is logged in the you pass the instance of that user
    user = request.user.customer
    form = CustomerForm(instance=user)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance= user)
        if form.is_valid():
            form.save()
    context = {
        'form':form
    }
    return render(request, 'accounts/user_setting.html', context)  

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id = pk)
    order= customer.order_set.all()
    total_order  = order.count()
    context = {
        'customer': customer,
        'order': order,
        'total_order': total_order
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    product = Product.objects.all()
    context = {
        'product': product
    }
    return render(request, 'accounts/product.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),  extra= 5)
    customer = Customer.objects.get(id = pk)
    form = OrderFormSet(instance=customer)
    if request.method == 'POST':
        form = OrderFormSet(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id = pk)
    form  = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'order': order
    }
    return render(request, 'accounts/delete_order.html', context)

