# Generated by Django 3.1.7 on 2021-03-16 00:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesorder',
            name='date',
        ),
        migrations.AddField(
            model_name='salesorder',
            name='date_created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='address_line',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='type',
            field=models.CharField(choices=[('Company', 'Company'), ('Individual', 'Individual')], max_length=100),
        ),
        migrations.AlterField(
            model_name='customer',
            name='zip_code',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='delivery_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='salesorder',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('SHIPPED', 'SHIPPED'), ('RECEIVED', 'RECEIVED')], max_length=100),
        ),
    ]