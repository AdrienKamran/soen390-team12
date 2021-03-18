# Generated by Django 3.1.7 on 2021-03-18 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='p_FK',
        ),
        migrations.AddField(
            model_name='product',
            name='c_FK',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inventory.contain'),
            preserve_default=False,
        ),
    ]