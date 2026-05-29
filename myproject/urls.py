from django.urls import path
from myapp import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.gate_view, name='gate_view'), 
    path('users/', views.combined_view, name='combined_view'),  
    path('logout/', views.custom_logout, name='logout'),
    path('delete/<str:user_id>/', views.delete_user, name='delete_user'),
]