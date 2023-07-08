# Generated by Django 4.1.7 on 2023-06-12 17:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(blank=True, default='', max_length=100)),
                ('student_email', models.CharField(blank=True, default='', max_length=100)),
                ('student_phone', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, default='profile_pics/default.png', upload_to='profile_pics')),
                ('default_shipping_address', models.CharField(blank=True, default='', max_length=100)),
                ('default_billing_address', models.CharField(blank=True, default='', max_length=100)),
                ('date_of_birth', models.DateField(blank=True, default=None, null=True)),
                ('user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('order_total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('order_status', models.CharField(blank=True, default='', max_length=100)),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]