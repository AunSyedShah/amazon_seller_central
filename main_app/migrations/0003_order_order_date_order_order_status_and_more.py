# Generated by Django 4.1.7 on 2023-07-16 11:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='Order Placed', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='main_app.product'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('order', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.order')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main_app.product')),
            ],
        ),
    ]
