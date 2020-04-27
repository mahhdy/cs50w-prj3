from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render,redirect,reverse

# Create your views here.
def index(request):
    return render(request,'orders/index.html')
@login_required
def my_view2(request):
    pass
def my_view(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
