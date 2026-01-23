from django.urls import path
from myapp import views

urlpatterns = [
    path('phones/', views.phone_list, name='phone_list'),
]
