from django.urls import path
from myapp import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', views.combined_view, name='combined_view'),
    path('', views.combined_view, name='home'),
    path('logout/', views.custom_logout, name='logout'),  # Своя вьюха
    path('delete/<str:user_id>/', views.delete_user, name='delete_user'),
]