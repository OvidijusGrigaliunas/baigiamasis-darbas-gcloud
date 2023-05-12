from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, UserDataForm, DateSelectionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from recordings.models import User as User_Data, Record
from datetime import datetime
from .utils import get_admin_dashboard_stats


# Create your views here.
def index(request):
    return render(request, 'web/index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('page_reloader')
        return HttpResponse('Incorrect username or password')
    form = UserLoginForm()
    return render(request, 'web/login.html', {'form': form})


def page_reloader(request):
    return render(request, 'web/page_reloader.html')


def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            message = "<p class='text-center'>Successful registration</p>"
            return HttpResponse(message)
        # TODO Prideti info kai bloga form
        message = "<p class='text-center'>Something went wrong</p>"
        return HttpResponse(message)
    form = UserRegisterForm()
    return render(request, 'web/register.html', {'form': form})


def register_app(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            message = "<p class='text-center'>Successful registration</p>"
            return HttpResponse(message)
        message = "<p class='text-center'>Something went wrong</p>"
        return HttpResponse(message)
    form = UserRegisterForm()
    return render(request, 'web/register_app.html', {'form': form})


@login_required(login_url='')
def logout_user(request):
    logout(request)
    return redirect('index')


@login_required(login_url='')
def user_profile(request):
    return render(request, 'web/user_settings.html', {'user': request.user.username})


@login_required(login_url='')
def personal_settings(request):
    current_user = request.user

    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            obj, created = User_Data.objects.update_or_create(
                user=current_user, defaults={'weight': form_data['weight'],
                                             'height': form_data['height'],
                                             'birthdate': form_data['birthdate']})
    user_data = User_Data.objects.filter(user=current_user)
    if user_data.exists():
        user_data_values = user_data.values()[0]
        form = UserDataForm(initial={'weight': user_data_values['weight'],
                                     'height': user_data_values['height'], 'birthdate': user_data_values['birthdate']})
    else:
        form = UserDataForm()
    return render(request, 'web/personal_settings.html', {'form': form})


def home_page(request):
    return render(request, 'web/home_page.html')


@login_required(login_url='')
def statistics_page(request):
    current_user = request.user
    records = Record.objects.filter(user=current_user.id).values()
    record_data = []
    for record in records:
        record_data.append({'date': record['record_date'], 'id': record['id']})
    return render(request, 'web/statistics.html', {'record_data': record_data})


@login_required(login_url='')
def admin_dashboard(request):
    if request.user.username == 'admin':
        filter = {'from': datetime.today().strftime('%Y-%m-%d'), 'to': datetime.today().strftime('%Y-%m-%d')}
        if request.method == 'POST':
            form = DateSelectionForm(request.POST)
            if form.is_valid():
                form_data: dict = form.cleaned_data
                filter['from'] = form_data['date1']
                filter['to'] = form_data['date2']
        form = DateSelectionForm(initial={'date1': filter['from'],
                                          'date2': filter['to']})
        statistics = get_admin_dashboard_stats(filter)
        CONTEXT = {'form': form, 'statistics': statistics}
        return render(request, 'web/admin_dashboard.html', CONTEXT)
    return redirect(home_page)
