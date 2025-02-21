# Generated by Django 5.1.1 on 2025-01-21 06:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Decoration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decoration_image', models.ImageField(upload_to='image/')),
                ('decoration_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_image', models.ImageField(upload_to='image/')),
                ('food_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Halls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hall_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=200)),
                ('capacity', models.IntegerField()),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10)),
                ('photo_url', models.ImageField(upload_to='image/')),
                ('hall_description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=100)),
                ('event_date', models.DateField()),
                ('event_description', models.TextField(blank=True, null=True)),
                ('event_status', models.CharField(max_length=100)),
                ('hall_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALORA.halls')),
            ],
        ),
        migrations.CreateModel(
            name='Bookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_date', models.DateField(auto_now_add=True)),
                ('payment_status', models.CharField(max_length=100)),
                ('photography', models.CharField(blank=True, max_length=100, null=True)),
                ('photography_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_payment', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('decoration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALORA.decoration')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALORA.events')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALORA.food')),
                ('hall_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ALORA.halls')),
            ],
        ),
        migrations.CreateModel(
            name='User_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
