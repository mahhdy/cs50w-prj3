from django.http import HttpResponse, QueryDict, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Food_type, Food, Topping
import sys
# Create your views here.


def index(request):
    context = {
        "types": Food_type.objects.all(),
        'foods': Food.objects.all(),
        'toppings': Topping.objects.all(),
    }
    return render(request, 'orders/index.html', context)


def logOut(request):
    return render(request, 'users/logout.html')


def toppings(request):
    return JsonResponse(list(Topping.objects.values()),safe=False)


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


def addOrder(request):
    if request.method == 'POST':
        l = request.POST
        return JsonResponse({'data': 'Love', 'received': l.dict()})
    return False


def cart(request):
    return render(request, 'orders/cart.html', {})


def profile(request):
    return render(request, 'orders/profile.html', {})


@login_required
def my_view2(request):
    pass


def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
