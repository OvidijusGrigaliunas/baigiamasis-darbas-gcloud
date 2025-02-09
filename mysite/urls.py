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

# [START gaestd_py_django_local_static]
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
                  path("recordings/", include("recordings.urls")),
                  path("admin/", admin.site.urls),
                  path('', include('web.urls')),
                  path("data-downloader/", include("data_downloader.urls")),
                  path('api-token-auth/', views.obtain_auth_token),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# [END gaestd_py_django_local_static]
