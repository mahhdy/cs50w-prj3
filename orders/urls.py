from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name=""),
    path("food_type/<int:id>/", views.food_types, name="courses"),
    path("food/<int:id>/", views.foods, name="foods"),
    path('order/add/',views.addOrder,name='addtobasket'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
