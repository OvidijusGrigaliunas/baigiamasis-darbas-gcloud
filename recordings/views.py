# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.http import HttpResponse, HttpResponseRedirect  # noqa: 401
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Record, Record_Data, User, Category
from django.utils import timezone
from datetime import datetime
from .serializers import RecordSerializer, RecordDataSerializer
import json


def index(request):
    records = Record.objects.select_related('category').filter(user=1).order_by('id')
    CONTEXT = {'records': records}
    return render(request, 'recordings/index.html', context=CONTEXT)


def record_data(request, record_id):
    recording_data = Record_Data.objects.filter(record_id=record_id).order_by('time')
    return render(request, 'recordings/record_data.html', {'records': recording_data})


# path('records/<int:record_id>/', views.record_data, name='record_data'),


# ./cloud_sql_proxy -instances="baigiamasis-darbas-373611:europe-north1:namudarbas"=tcp:5432
# export GOOGLE_CLOUD_PROJECT=baigiamasis-darbas-373611
# export USE_CLOUD_SQL_AUTH_PROXY=true

@api_view(['POST'])
def post_recording(request):
    record = request.data
    cur_user = User.objects.get(id=1)
    cur_category = Category.objects.get(id=1)
    new_record = Record(user=cur_user, category=cur_category, record_date=timezone.now())
    new_record.save()
    cur_record = Record.objects.get(id=new_record.id)
    for record_data in record:
        accel_data = record_data['accelerometer']
        new_record_data = Record_Data(record=cur_record, accel_x=accel_data['x-axis'], accel_y=accel_data['y-axis'],
                                      accel_z=accel_data['z-axis'],
                                      gyro_x=0, gyro_y=0, gyro_z=0, time=record_data['time'])
        new_record_data.save()
    return Response('Success')
