# Generated by Django 5.1.1 on 2025-01-28 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALORA', '0003_bookings_event_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='food_value',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
