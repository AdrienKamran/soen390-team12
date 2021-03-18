# Generated by Django 3.1.7 on 2021-03-18 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_defective', models.BooleanField(default=False)),
                ('p_serial', models.BigIntegerField(default=10000)),
                ('p_in_inventory', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.TextField(choices=[('PENDING', 'PENDING'), ('SHIPPED', 'SHIPPED'), ('RECEIVED', 'RECEIVED')], default='PENDING')),
                ('order_quantity', models.IntegerField(default=1)),
                ('order_total_cost', models.DecimalField(decimal_places=2, max_digits=9)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=80, unique=True)),
                ('p_unit_value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
                ('p_size', models.IntegerField(blank=True, default=1, null=True)),
                ('p_color', models.CharField(blank=True, max_length=7, null=True, unique=True)),
                ('p_finish', models.TextField(blank=True, choices=[('Matte', 'Matte'), ('Glossy', 'Glossy'), ('Chrome', 'Chrome')], default='Glossy', null=True)),
                ('p_grade', models.TextField(blank=True, choices=[('Aluminum', 'Aluminum'), ('Steel', 'Steel'), ('Carbon', 'Carbon')], default='Aluminum', null=True)),
                ('p_type', models.TextField(choices=[('Raw Material', 'Raw Material'), ('Part', 'Part'), ('Product', 'Product')], default='Part')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v_name', models.CharField(max_length=80, unique=True)),
                ('v_price_multiplier', models.DecimalField(decimal_places=5, max_digits=9)),
                ('v_address', models.CharField(max_length=120)),
                ('v_city', models.CharField(max_length=120)),
                ('v_province', models.CharField(max_length=120)),
                ('v_postal_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('w_name', models.CharField(max_length=80, unique=True)),
                ('w_address', models.CharField(max_length=120)),
                ('w_city', models.CharField(max_length=120)),
                ('w_province', models.CharField(max_length=120)),
                ('w_postal_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='SellsPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_quantity', models.IntegerField(default=100)),
                ('p_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.part')),
                ('v_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('prod_type', models.TextField(choices=[('Mountain Bike', 'Mountain Bike'), ('Road Bike', 'Road Bike'), ('Hybrid Bike', 'Hybrid Bike')], default='Hybrid Bike')),
                ('prod_weight', models.DecimalField(decimal_places=2, max_digits=9)),
                ('p_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.part')),
            ],
        ),
        migrations.CreateModel(
            name='OrdersPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.contain')),
                ('o_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='p_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.part'),
        ),
        migrations.AddField(
            model_name='order',
            name='v_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.vendor'),
        ),
        migrations.AddField(
            model_name='order',
            name='w_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse'),
        ),
        migrations.AddField(
            model_name='contain',
            name='p_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.part'),
        ),
        migrations.AddField(
            model_name='contain',
            name='w_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse'),
        ),
    ]
