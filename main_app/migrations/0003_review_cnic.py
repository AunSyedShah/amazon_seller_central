# Generated by Django 4.1.7 on 2023-09-19 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='cnic',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]