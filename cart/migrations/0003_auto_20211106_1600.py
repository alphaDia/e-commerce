# Generated by Django 3.1 on 2021-11-06 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_auto_20211106_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product_color',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='product_size',
            field=models.CharField(blank=True, default=0, max_length=100, null=True),
        ),
    ]
