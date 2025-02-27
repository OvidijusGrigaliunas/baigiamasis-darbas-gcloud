from django.db import models
from django.contrib.auth.models import User as AuthUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


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
    data_interval = models.IntegerField()


class Record_Data(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    gyro_x = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    gyro_y = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    gyro_z = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    accel_x = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    accel_y = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    accel_z = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    magnet_x = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    magnet_y = models.DecimalField(max_digits=13, decimal_places=9, null=True)
    magnet_z = models.DecimalField(max_digits=13, decimal_places=9, null=True)


class Record_Data_Extra(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    gyro_x = models.DecimalField(max_digits=13, decimal_places=9)
    gyro_y = models.DecimalField(max_digits=13, decimal_places=9)
    gyro_z = models.DecimalField(max_digits=13, decimal_places=9)
    accel_x = models.DecimalField(max_digits=13, decimal_places=9)
    accel_y = models.DecimalField(max_digits=13, decimal_places=9)
    accel_z = models.DecimalField(max_digits=13, decimal_places=9)
    magnet_x = models.DecimalField(max_digits=13, decimal_places=9)
    magnet_y = models.DecimalField(max_digits=13, decimal_places=9)
    magnet_z = models.DecimalField(max_digits=13, decimal_places=9)
    temp = models.DecimalField(max_digits=5, decimal_places=2)
    pressure = models.DecimalField(max_digits=13, decimal_places=6)
