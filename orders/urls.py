from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name=""),
    path('login/',views.login_view,name='login'),
    path("food_type/<int:id>/", views.food_types, name="courses"),
    path("food/<int:id>/", views.foods, name="foods"),
    path('order/add/',views.addOrder,name='addtobasket'),
    path('order/cart/',views.cart,name='cart'),
    path('order/orders/',views.allorders,name='orders'),
    path('order/submit/',views.submitOrder,name='submit'),
    path('order/<int:id>/',views.order,name='orderDetail'),
    path('order/myorder/',views.myorder,name='myorder'),
    path('order/profile/',views.profile,name='profile'),
    path('order/toppings/',views.toppings,name='toppings'),
    path('logout/',views.logout_view,name='logout'),
    path('regnew/',views.signup,name='registnew'), 

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
