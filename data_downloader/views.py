from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound  # noqa: 401
from django.shortcuts import get_object_or_404, render, redirect
from recordings.models import Record, Record_Data, User, Category
from django.http import FileResponse
from .utils import download_data
from .forms import DateSelectionForm


@login_required(login_url='')
def index(request):
    if request.user.username == 'admin':
        if request.method == 'POST':
            form = DateSelectionForm(request.POST)
            if form.is_valid():
                form_data: dict = form.cleaned_data
                download_data(form_data['date1'], form_data['date2'])
                return redirect(
                    'https://storage.cloud.google.com/baigiamasis-darbas-373611.appspot.com/data/user_data.csv')
        form = DateSelectionForm()
        CONTEXT = {'form': form}
        return render(request, 'data_downloader/index.html', context=CONTEXT)
    return redirect('/')
