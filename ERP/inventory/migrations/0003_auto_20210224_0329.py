# Generated by Django 3.1.7 on 2021-02-24 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_products_p_unit_cost'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContainsProducts',
            new_name='ContainsParts',
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Parts',
        ),
        migrations.RenameField(
            model_name='madeofparts',
            old_name='product_1_FK',
            new_name='part_1_FK',
        ),
        migrations.RenameField(
            model_name='madeofparts',
            old_name='product_2_FK',
            new_name='part_2_FK',
        ),
        migrations.RenameField(
            model_name='madeofrm',
            old_name='product_FK',
            new_name='part_FK',
        ),
    ]
