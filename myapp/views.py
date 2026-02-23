from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PsAors, PsAuths, PsEndpoints
from .forms import AddUserForm
from django.db import IntegrityError

def combined_view(request):
    # Получаем ID для редактирования из GET параметра
    edit_id = request.GET.get('edit_id')
    editing_user = None
    form = AddUserForm()  # Пустая форма по умолчанию
    
    # Получаем данные из таблиц
    aors_data = PsAors.objects.all().values('id', 'contact', 'max_contacts')
    auth_data = PsAuths.objects.all().values('id')
    endpoints_data = PsEndpoints.objects.all().values('id', 'context', 'callerid', 'tnumber', 'transport')
    
    # Если есть edit_id - значит режим редактирования
    if edit_id:
        try:
            editing_user = PsEndpoints.objects.get(id=edit_id)
            form = AddUserForm(instance=editing_user)  # Заполняем форму данными
        except PsEndpoints.DoesNotExist:
            messages.error(request, 'Пользователь не найден')
    
    # Обработка POST запроса (создание или обновление)
    if request.method == 'POST':
        # Проверяем, это создание или обновление
        user_id = request.POST.get('id')
        
        if user_id and PsEndpoints.objects.filter(id=user_id).exists():
            # РЕЖИМ РЕДАКТИРОВАНИЯ - обновляем существующую запись
            endpoint = PsEndpoints.objects.get(id=user_id)
            form = AddUserForm(request.POST, instance=endpoint)
            
            if form.is_valid():
                form.save()
                messages.success(request, f'Пользователь {user_id} успешно обновлен!')
                return redirect('combined_view')
        else:
            # РЕЖИМ СОЗДАНИЯ - новая запись
            form = AddUserForm(request.POST)
            if form.is_valid():
                id_value = form.cleaned_data['id']
                
                try:
                    # Создаём записи во всех таблицах
                    PsAors.objects.create(id=id_value, contact='', max_contacts=2)
                    PsAuths.objects.create(id=id_value)
                    form.save()  # Сохраняем PsEndpoints
                    
                    messages.success(request, 'Пользователь успешно создан!')
                    return redirect('combined_view')
                except IntegrityError as e:
                    messages.error(request, f'Ошибка: {e}')
    
    context = {
        'aors': aors_data,
        'auth': auth_data,
        'endpoints_data': endpoints_data,
        'form': form,
        'edit_mode': bool(edit_id),  # True если редактируем
        'editing_user': editing_user,
    }
    return render(request, 'combined_view.html', context)