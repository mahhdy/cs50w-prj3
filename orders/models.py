from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.conf import settings

# Create your models here.
fSize = (
    ('small', 'Small'),
    ('large', 'Large'),
)


order_status = (
    ('new', 'New'),
    ('ready', 'Ready'),
    ('completed', 'Completed'),
)

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Topping(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Food_type(models.Model):
    name = models.CharField(max_length=15)
    picture = models.ImageField(upload_to='foods/', default='default.jpg')

    def get_absolute_url(self):
        return reverse('course', kwargs={"pk": self.pk})

    def get_image_url(self):
        return settings.MEDIA_URL + self.image.url

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=30)
    size = models.CharField(max_length=5, choices=fSize)
    food_type = models.ForeignKey(Food_type,null=True,blank=True, on_delete=models.SET_NULL)
    topping_cout=models.PositiveIntegerField(default=0)
    price = models.DecimalField(decimal_places=2,max_digits=10)
    picture = models.ImageField(upload_to='foods/', default='default.jpg')
   # Metadata

    class Meta:
        ordering = ['-name']
   # Methods

    def get_absolute_url(self):
        return reverse('index')

    # def get_image_url(self):
    #     return settings.MEDIA_URL + 'foods/' + self.image.url

    def __str__(self):
        return self.food_type.name + "/" + self.name + self.size


class BasketManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(confirmed=False)


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,limit_choices_to={'is_customer': True},
         on_delete=models.SET(get_sentinel_user),related_name='customer')
    chef = models.ForeignKey(settings.AUTH_USER_MODEL,limit_choices_to={'is_staff': True},
                             on_delete=models.SET(get_sentinel_user), blank=True,related_name='chef')
    note = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=10,choices=order_status,default='new')
    order_details = models.ForeignKey('Order_detail',blank=True,null=True,on_delete=models.SET_NULL,related_name='details')
    def __str__(self):
        return self.status + "/" + self.customer + " (" + self.total + ")"

    class Meta:
        ordering = ['-date_added']
    objects = models.Manager()
    baskets = BasketManager()
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    order_total=property(get_total_cost)

class Order_detail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="order_items")
    toppings = models.ManyToManyField(Topping, default='None',blank=True)
    quantity = models.PositiveIntegerField(default=1)
    extra = models.CharField(max_length=200,blank=True)

    def __str__(self):
        return self.order__cutomer.name + "/ " + self.food.name
    def get_cost(self):
        return self.food.price * self.quantity
    item_total=property(get_cost)