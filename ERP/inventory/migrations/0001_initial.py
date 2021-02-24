# Generated by Django 3.1.7 on 2021-02-23 00:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=80, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RawMaterials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rm_name', models.CharField(max_length=80, unique=True)),
                ('rm_unit_cost', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field1', models.CharField(max_length=80)),
                ('field2', models.IntegerField()),
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
            name='MadeOfRM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rm_quantity', models.IntegerField(default=1)),
                ('product_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.products')),
                ('rm_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.rawmaterials')),
            ],
        ),
        migrations.CreateModel(
            name='MadeOfParts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_quantity', models.IntegerField(default=1)),
                ('product_1_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='madeofparts_parent_product', to='inventory.products')),
                ('product_2_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='madeofparts_child_part', to='inventory.products')),
            ],
        ),
        migrations.CreateModel(
            name='ContainsRM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rm_quantity', models.IntegerField(default=1)),
                ('rm_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.rawmaterials')),
                ('w_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='ContainsProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_quantity', models.IntegerField(default=1)),
                ('product_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.products')),
                ('w_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
            ],
        ),
    ]