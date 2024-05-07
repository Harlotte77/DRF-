from django.db import models


# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=32, verbose_name="书籍名称")
    # null = True表示允许该字段为空
    price = models.IntegerField(verbose_name="价格", default=99, null=True)
    pub_date = models.DateField(verbose_name="出版日期")


class Publish(models.Model):
    name = models.CharField(max_length=32, verbose_name="出版社名称")
    addr = models.CharField(max_length=32, verbose_name="出版社地址")

class Author(models.Model):
    auth_name = models.CharField(max_length=32, verbose_name="作者姓名")
    age = models.IntegerField(verbose_name="作者年龄")
