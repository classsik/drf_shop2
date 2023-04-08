from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    category = models.CharField(max_length=255)


class Cart(models.Model):
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')


class Order(models.Model):
    products = models.ManyToManyField(Product)
    total_price = models.IntegerField()
