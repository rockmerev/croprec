
from django.urls import path
from app import views

urlpatterns = [
    path('form', views.crop_recommendation, name='crop_recommendation'),
    path('',views.home_view,name='home'),
    path('yield',views.yield_prediction_view,name='yield'),
]
