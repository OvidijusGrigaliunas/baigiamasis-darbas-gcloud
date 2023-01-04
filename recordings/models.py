from django.db import models
from django.contrib.auth.models import User as AuthUser


class User(models.Model):
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
    birthdate = models.DateField(default='2000-01-01')


class Category(models.Model):
    category_name = models.CharField(max_length=64)
    category_desc = models.TextField()


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    record_date = models.DateTimeField()


class Record_Data(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    gyro_x = models.DecimalField(max_digits=13, decimal_places=9)
    gyro_y = models.DecimalField(max_digits=13, decimal_places=9)
    gyro_z = models.DecimalField(max_digits=13, decimal_places=9)
    accel_x = models.DecimalField(max_digits=13, decimal_places=9)
    accel_y = models.DecimalField(max_digits=13, decimal_places=9)
    accel_z = models.DecimalField(max_digits=13, decimal_places=9)
    time = models.PositiveBigIntegerField()
