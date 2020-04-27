from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, reverse
from .models import Food_type, Food

# Create your views here.


def index(request):
    context = {
        "types": Food_type.objects.all()
    }
    return render(request, 'orders/index.html', context)


def food_types(request, food_type_id):
    try:
        ftypes = Food_type.objects.get(pk=food_type_id)
    except Food_type.DoesNotExist:
        raise Http404("Food Type does not exist")
    context = {
        "food_types": ftypes,
        'foods': Food.objects.filter(food_type=ftypes).all(),
    }
    return render(request, 'orders/courses.html', context)
def foods(request, food_id):
    try:
        food = Food.objects.get(pk=food_id)
    except Food.DoesNotExist:
        raise Http404("Food does not exist")
    context = {
        "food": food,
    }
    return render(request, 'orders/food.html', context)

@login_required
def my_view2(request):
    pass


def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
