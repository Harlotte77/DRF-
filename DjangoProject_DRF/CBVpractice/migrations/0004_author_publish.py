# Generated by Django 4.2.11 on 2024-04-26 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CBVpractice', '0003_alter_book_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth_name', models.CharField(max_length=32, verbose_name='作者姓名')),
                ('age', models.IntegerField(verbose_name='作者年龄')),
            ],
        ),
        migrations.CreateModel(
            name='Publish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='出版社名称')),
                ('addr', models.CharField(max_length=32, verbose_name='出版社地址')),
            ],
        ),
    ]
