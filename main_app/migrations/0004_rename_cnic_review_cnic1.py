# Generated by Django 4.1.7 on 2023-09-19 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_review_cnic'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='cnic',
            new_name='cnic1',
        ),
    ]
