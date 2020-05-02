# Generated by Django 3.0.4 on 2020-05-01 19:05

from django.conf import settings
from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0008_food_accepts_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='picture',
            field=models.ImageField(default='default.gif', upload_to='foods/'),
        ),
        migrations.AlterField(
            model_name='order',
            name='chef',
            field=models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=models.SET(orders.models.get_sentinel_user), related_name='chef', to=settings.AUTH_USER_MODEL),
        ),
    ]