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

from django.http import HttpResponse, HttpResponseRedirect  # noqa: 401
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Record, Record_Data, User, Category
from rest_framework.authtoken.models import Token
from django.utils import timezone
from .utils import get_accelerometer_speed


def index(request):
    records = Record.objects.select_related('category').filter(user=1).order_by('id')
    CONTEXT = {'records': records}
    return render(request, 'recordings/index.html', context=CONTEXT)


# TODO: Pritaikyti naujiem duomenim
def record_data(request, record_id):
    recordings_data = Record_Data.objects.filter(record_id=record_id).values()
    data_interval = Record.objects.get(id=record_id).values('data_interval')['data_interval']
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


@api_view(['POST'])
def post_recording(request):
    try:
        record = request.data['data']
        user_id = Token.objects.values('user_id').get(key=record['token'])
        print(user_id)
        cur_user = User.objects.get(id=user_id['user_id'])
        cur_category = Category.objects.get(id=1)
        new_record = Record(user=cur_user, category=cur_category, record_date=timezone.now(), data_interval=100)
        new_record.save()
        cur_record = Record.objects.get(id=new_record.id)
        recorded_data = []

        for n in range(0, len(record['accelerometerData'])):
            recorded_data.append({'accel': record['accelerometerData'][n],
                                  'gyro': record['gyroscopeData'][n],
                                  'magnet': record['magnetometerData'][n]})
        for data_row in recorded_data:
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
        return Response('Success')
    except ValueError as e:
        return Response('a')
    except AttributeError as e:
        return Response('a')
    except TypeError as e:
        return Response('a')
    except TimeoutError as e:
        return Response('a')
