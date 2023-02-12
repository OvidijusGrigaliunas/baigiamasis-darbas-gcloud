from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path('home_page', views.home_page, name='home_page'),
    path('settings', views.user_profile, name='user_profile'),
    path('personal_settings', views.personal_settings, name='personal_settings'),
    path('reload_page', views.page_reloader, name='page_reloader'),
]
