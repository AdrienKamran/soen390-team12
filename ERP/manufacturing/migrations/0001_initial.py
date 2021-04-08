# Generated by Django 3.1.7 on 2021-04-07 23:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacture_quantity', models.IntegerField(default=1)),
                ('manufacture_total_cost', models.DecimalField(decimal_places=2, max_digits=9)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('p_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.part')),
                ('w_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.warehouse')),
            ],
        ),
        migrations.CreateModel(
            name='ManufacturesPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.contain')),
                ('m_FK', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manufacturing.manufacture')),
            ],
        ),
        migrations.CreateModel(
            name='MadeOf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('part_FK_child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='madeof_child_part', to='inventory.part')),
                ('part_FK_parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='madeof_parent_part', to='inventory.part')),
            ],
        ),
    ]