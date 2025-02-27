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

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='record'),
    path('record/<int:record_id>/', views.record_data, name='record_data'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
    path('postrecord/', views.post_recording, name='postRecording'),
    path('postrecordextra/', views.post_recording_extra, name='postRecordingExtra')

]
