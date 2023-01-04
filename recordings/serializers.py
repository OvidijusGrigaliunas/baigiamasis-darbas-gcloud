from rest_framework import serializers
from .models import Record, Record_Data


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class RecordDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record_Data
        fields = '__all__'
