# Generated by Django 4.2.11 on 2024-04-25 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CBVpractice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='price',
            field=models.IntegerField(default=99, verbose_name='价格'),
        ),
    ]