# Generated by Django 3.0.4 on 2020-05-04 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20200502_1507'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, default=0.5, max_digits=4)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_details',
        ),
        migrations.AlterField(
            model_name='order_detail',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered', to='orders.Food'),
        ),
    ]
