# Generated by Django 4.1.7 on 2023-07-16 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_delete_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='Pending', max_length=100, verbose_name=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')]),
        ),
    ]
