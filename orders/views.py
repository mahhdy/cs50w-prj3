from django.http import HttpResponse, QueryDict, JsonResponse, Http404
from users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import SignUpForm
from django.conf import settings
from django.core import serializers
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Food_type, Food, Topping,Order,Order_detail,order_status,Extra
from django.db.models import Q
import sys,json
# Create your views here.

@login_required
def addOrder(request):
    if request.method == 'POST':
        openOrder, created=Order.baskets.get_or_create(customer=request.user)
        openOrder.note=request.POST.get('obj', None)
        openOrder.save()
        
        return JsonResponse({'data': 'Love', 'received': openOrder.note})
    return False

@login_required
def submitOrder(request):
    if request.method == 'POST':
        newOrder, created=Order.baskets.get_or_create(customer=request.user)
        details=json.loads(request.POST.get('obj', None))
        for d in details:
            ex=d['topping'] if d['topping'] else ''
            ex+=d['extra'] if d['extra'] else ''
            f=Food.objects.get(pk=d['id'])
            a=Order_detail.objects.create(order=newOrder,extra=ex,food=f,quantity=d['quantity'])
            if f.topping_count:
                t=d['topping'].split('+')
                for x in range(f.topping_count):
                    try:
                        b=Topping.objects.get(name=t[x].strip())
                        a.toppings.add(b)
                    except Exception as e:
                        print(e)
            a.save()
            newOrder.details=a
        newOrder.status='initiated'
        newOrder.confirmed=True
        newOrder.save()
        return JsonResponse({'orderNo': newOrder.id})
    return False

    
def signup(request):
    template = 'users/register.html'
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, template, {'form': form})


def index(request):
    context = {
        "types": Food_type.objects.all(),
        'foods': Food.objects.all(),
    }
    if request.user.is_authenticated:
        unconfirmed=Order.baskets.filter(customer=request.user)
        if unconfirmed.exists():
            a=unconfirmed.values('note')[0]
            context['basket']=a['note']
    return render(request, 'orders/index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        return render(request, 'users/login.html', {'message': 'please try again!'})
    else:
        return render(request, 'users/login.html',)
    return reverse('index')


def logout_view(request):
    logout(request)
    return redirect("/")


def extras(request):
    return JsonResponse(list(Extra.objects.values()), safe=False)


def toppings(request):
    return JsonResponse(list(Topping.objects.values()), safe=False)


def food_types(request, id=None):
    ftypes = get_object_or_404(Food_type, id=id)
    context = {
        "food_types": ftypes,
        'foods': Food.objects.filter(food_type=ftypes),
        'toppings': Topping.objects.all(),
    }
    return render(request, 'orders/courses.html', context)


def foods(request, id=None):
    return render(request, 'orders/food.html', {"food": get_object_or_404(Food, id=id), })




def cart(request):
    return render(request, 'orders/cart.html', {})


@login_required
def myorder(request):
    u = request.user
    order=Order.objects.filter(customer=u).exclude(status='new')    
    return render(request, 'orders/orders.html', {'order':order,'s':order_status})

@login_required
def order(request, id=None):
    u = request.user
    if u.is_staff:
        order=get_object_or_404(Order,~Q(status='new'),id=id)
    else:
        order=get_object_or_404(Order,~Q(status='new'),customer=u,id=id)
    return render(request, 'orders/order.html', {'k':order})

@login_required
def allorders(request):
    u = request.user
    if u.is_staff:
        order=Order.objects.exclude(status='new')
    else:
        order=Order.objects.filter(customer=u).exclude(status='new')
    return render(request, 'orders/orders.html', {'order':order,'s':order_status})


@login_required
def profile(request):
    return render(request, 'orders/profile.html', {})


@login_required
def my_view2(request):
    pass


def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
