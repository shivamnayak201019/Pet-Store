# Generated by Django 5.0.4 on 2024-06-13 05:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0005_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentstatus', models.CharField(default='pending', max_length=100)),
                ('transactionid', models.CharField(max_length=200)),
                ('paymentmode', models.CharField(default='paypal', max_length=100)),
                ('customerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.customer1')),
                ('oid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.order')),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='orderdetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordernumber', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('totalprice', models.IntegerField()),
                ('created_at', models.DateField(auto_now=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('customerid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.customer1')),
                ('productid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='petapp.pet')),
                ('paymentid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='petapp.payment')),
            ],
            options={
                'db_table': 'orderdetail',
            },
        ),
    ]