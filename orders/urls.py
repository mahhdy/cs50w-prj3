from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.index, name=""),
    path("food_type/<int:pk>/", views.food_types, name="courses"),
    path("food/<int:pk>/", views.foods, name="foods"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
