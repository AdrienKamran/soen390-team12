# Generated by Django 3.1.7 on 2021-03-12 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20210225_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contains',
            name='p_quantity',
        ),
        migrations.AddField(
            model_name='contains',
            name='p_defective',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contains',
            name='p_serial',
            field=models.BigIntegerField(default=10000),
        ),
    ]
