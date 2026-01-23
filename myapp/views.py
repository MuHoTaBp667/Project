from django.shortcuts import render
from .models import Phone

def phone_list(request):
    phones = Phone.objects.all()  # Получаем все записи из таблицы phones
    return render(request, 'phones/list.html', {'phones': phones})
