from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('data_view/', views.data_view, name='data_view'),
    path('data_view_detail/<int:pk>', views.data_view_detail, name='data_view_detail'),
    path('data/api/', views.ConsumerDataView.as_view(), name='api_view')


]