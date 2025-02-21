# Generated by Django 5.1.1 on 2025-01-24 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ALORA', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='decoration',
            name='decoration_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='food_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='halls',
            name='photo_url',
            field=models.FileField(upload_to=''),
        ),
    ]
