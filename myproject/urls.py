from django.urls import path
from myapp import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/', views.combined_view, name='combined_view'),  # ЕДИНСТВЕННЫЙ маршрут
]
