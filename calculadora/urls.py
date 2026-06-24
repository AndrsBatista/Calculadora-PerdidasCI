from django.urls import path
from . import views

app_name = 'calculadora'

urlpatterns = [
    path('', views.upload_view, name='upload'),
    path('descargar-excel/', views.descargar_excel, name='descargar_excel'),
]