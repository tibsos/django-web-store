from django.urls import path

from .views import *

urlpatterns = [

    path('login', log_in),
    path('register', register),
    path('logout', log_out),

]