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
import decimal

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect  # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Record, Record_Data, User, Category, Record_Data_Extra
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .utils import get_accelerometer_speed
import json


def index(request):
    records = Record.objects.select_related('category').filter(user=1).order_by('id')
    CONTEXT = {'records': records}
    return render(request, 'recordings/index.html', context=CONTEXT)


def record_data(request, record_id):
    recordings_data = Record_Data.objects.filter(record_id=record_id).values()
    data_interval = Record.objects.values('data_interval').get(id=record_id)['data_interval']
    return render(request, 'recordings/record_data.html',
                  {"records": recordings_data, "record_id": record_id, "interval": data_interval})


@login_required(login_url='')
def delete_record(request, record_id):
    user = request.user.id
    record = Record.objects.get(id=record_id)
    record_user = User.objects.get(id=record.user_id)
    if user == record_user.user_id:
        Record_Data.objects.filter(record_id=record_id).delete()
        Record.objects.filter(id=record_id).delete()
    return redirect('/statistics')


""" old version
def record_data(request, record_id):
    recordings_data = Record_Data.objects.filter(record_id=record_id).values()
    data_interval = Record.objects.values('data_interval').get(id=record_id)['data_interval']
    accelerometer_speed = get_accelerometer_speed(recordings_data.values("accel_x", "accel_y", "accel_z"),
                                                  data_interval)
    time_in_seconds = []
    for i in range(1, len(accelerometer_speed['x'])):
        time_in_seconds.append((i + 1) * data_interval / 1000)

    formatted_data = []
    for i in range(0, len(time_in_seconds) - 1):
        formatted_data.append(
            {"accel_x": accelerometer_speed["x"][i], "accel_y": round(accelerometer_speed["y"][i], 2),
             "accel_z": round(accelerometer_speed["z"][i], 2), "time": time_in_seconds[i]})

    return render(request, 'recordings/record_data.html', {"records": formatted_data})
"""


@api_view(['POST'])
def post_recording(request):
    record = json.loads(request.data['data'])
    user_id = Token.objects.values('user_id').get(key=record['token'])
    cur_user = User.objects.get(id=user_id['user_id'])
    cur_category = Category.objects.get(id=1)
    new_record = Record(user=cur_user, category=cur_category, record_date=timezone.now(),
                        data_interval=record['interval'])
    new_record.save()
    cur_record = Record.objects.get(id=new_record.id)
    recorded_data = []
    for n in range(0, len(record['accelerometerData'])):
        recorded_data.append({})
        try:
            recorded_data[n]['accel'] = record['accelerometerData'][n]
        except IndexError as e:
            recorded_data[n]['accel'] = {'x': None, 'y': None, 'z': None}
        try:
            recorded_data[n]['gyro'] = record['gyroscopeData'][n]
        except IndexError as e:
            recorded_data[n]['gyro'] = {'x': None, 'y': None, 'z': None}
        try:
            recorded_data[n]['magnet'] = record['magnetometerData'][n]
        except IndexError as e:
            recorded_data[n]['magnet'] = {'x': None, 'y': None, 'z': None}

    for data_row in recorded_data:
        print(data_row)
        new_record_data = Record_Data(record=cur_record,
                                      accel_x=data_row['accel']['x'],
                                      accel_y=data_row['accel']['y'],
                                      accel_z=data_row['accel']['z'],
                                      gyro_x=data_row['gyro']['x'],
                                      gyro_y=data_row['gyro']['y'],
                                      gyro_z=data_row['gyro']['z'],
                                      magnet_x=data_row['magnet']['x'],
                                      magnet_y=data_row['magnet']['y'],
                                      magnet_z=data_row['magnet']['z'],
                                      )
        new_record_data.save()
    print('Success')
    return Response('Success')


@api_view(['POST'])
def post_recording_extra(request):
    record = json.loads(request.data['data'])
    user_id = Token.objects.values('user_id').get(key=record['token'])
    cur_user = User.objects.get(id=user_id['user_id'])
    cur_category = Category.objects.get(id=1)
    new_record = Record(user=cur_user, category=cur_category, record_date=timezone.now(),
                        data_interval=record['interval'])
    new_record.save()
    cur_record = Record.objects.get(id=new_record.id)
    print(record['objektas'])
    for data_row in record['objektas']:
        print(data_row)
        new_record_data = Record_Data_Extra(record=cur_record,
                                            accel_x=float(data_row['acc']['x']),
                                            accel_y=float(data_row['acc']['y']),
                                            accel_z=float(data_row['acc']['z']),
                                            gyro_x=float(data_row['gyr']['x']),
                                            gyro_y=float(data_row['gyr']['y']),
                                            gyro_z=float(data_row['gyr']['z']),
                                            magnet_x=float(data_row['mag']['x']),
                                            magnet_y=float(data_row['mag']['y']),
                                            magnet_z=float(data_row['mag']['z']),
                                            temp=float(data_row['temp']),
                                            pressure=float(data_row['pres']),
                                            )
        new_record_data.save()
    print('Success')
    return Response('Success')
