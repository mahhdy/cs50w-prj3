# Generated by Django 3.0.4 on 2020-04-28 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200427_0103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='topping_cout',
            new_name='topping_count',
        ),
        migrations.AlterField(
            model_name='food_type',
            name='picture',
            field=models.ImageField(default='foods/default.jpg', upload_to='foods/'),
        ),
    ]