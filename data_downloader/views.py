from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound  # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from recordings.models import Record, Record_Data, User, Category
from django.http import FileResponse
from .utils import download_data

def index(request):
    records = Record.objects.select_related('category').filter(user=1).order_by('id')
    CONTEXT = {'records': records}
    return render(request, 'data_downloader/index.html', context=CONTEXT)


def data_download_url(request):
    download_data()
    return redirect('https://storage.cloud.google.com/baigiamasis-darbas-373611.appspot.com/data/user_data.csv')

