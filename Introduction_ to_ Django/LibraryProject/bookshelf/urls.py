from django.urls import path
from . import views  # import views from the current app

urlpatterns = [
    path('', views.index, name='index'),  # example route
]
