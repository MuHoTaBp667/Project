from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import PsAors, PsAuths, PsEndpoints
from .forms import AddUserForm
from django.db import IntegrityError
from django.http import HttpResponse
from datetime import datetime
import os


def gate_view(request):
    """Страница входа с паролем"""
    if request.session.get('user_role'):
        return redirect('combined_view')
    
    error = None
    
    if request.method == 'POST':
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        if password == 'admin123':
            request.session['user_role'] = 'admin'
            request.session['username'] = 'Администратор'
        elif password == 'reader123':
            request.session['user_role'] = 'reader'
            request.session['username'] = 'Читатель'
        else:
            error = 'Неверный пароль!'
            return render(request, 'gate.html', {'error': error})
        
        if not remember:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(30 * 24 * 60 * 60)
        
        return redirect('combined_view')
    
    return render(request, 'gate.html', {'error': error})


def combined_view(request):
    if not request.session.get('user_role'):
        return redirect('gate_view')
    
    user_role = request.session.get('user_role')
    
    edit_id = request.GET.get('edit_id')
    editing_user = None
    form = AddUserForm()
    
    aors_data = PsAors.objects.all().values('id', 'contact', 'max_contacts')
    auth_data = PsAuths.objects.all().values('id')
    endpoints_data = PsEndpoints.objects.all().values('id', 'context', 'callerid', 'tnumber', 'transport')
    
    if edit_id:
        if user_role == 'admin':
            try:
                editing_user = PsEndpoints.objects.get(id=edit_id)
                form = AddUserForm(instance=editing_user)
            except PsEndpoints.DoesNotExist:
                messages.error(request, 'Пользователь не найден')
        else:
            messages.warning(request, 'У вас нет прав на редактирование!')
            return redirect('combined_view')
    
    if request.method == 'POST':
        if user_role != 'admin':
            messages.error(request, 'У вас нет прав на изменение данных!')
            return redirect('combined_view')
        
        user_id = request.POST.get('id')
        
        if user_id and PsEndpoints.objects.filter(id=user_id).exists():
            endpoint = PsEndpoints.objects.get(id=user_id)
            form = AddUserForm(request.POST, instance=endpoint)
            
            if form.is_valid():
                form.save()
                messages.success(request, f'Пользователь {user_id} успешно обновлен!')
                return redirect('combined_view')
        else:
            form = AddUserForm(request.POST)
            if form.is_valid():
                id_value = form.cleaned_data['id']
                
                try:
                    PsAors.objects.create(id=id_value, contact='', max_contacts=2)
                    PsAuths.objects.create(id=id_value)
                    form.save()
                    
                    # ГЕНЕРАЦИЯ И СОХРАНЕНИЕ CFG ФАЙЛА
                    tnumber = form.cleaned_data.get('tnumber', '')
                    
                    config_content = f"""#version:1.0.0.1


account.1.enable = 1
account.1.label = {id_value}
account.1.display_name = {form.cleaned_data.get('callerid', id_value)}
account.1.auth_name = {id_value}
account.1.user_name = {id_value}
account.1.password = StrongSIPPassword123
account.1.sip_server.1.address = 192.168.1.50
account.1.sip_server.1.port = 5060

## Общие параметры телефона ##
lang.wui = Russian
lang.gui = Russian
local_time.time_zone = +3
local_time.ntp_server1 = pool.ntp.org

## Смена стандартного пароля администратора web-интерфейса ##
security.user_password = admin:NewAdminPassword987

# ID: {id_value}
# CallerID: {form.cleaned_data.get('callerid', id_value)}
# TNumber: {tnumber if tnumber else 'Не указан'}
# Дата: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                    
                    # СОХРАНЯЕМ ФАЙЛ НА ДИСК (без скачивания)
                    config_dir = '/home/muhotabp/mac_cfg'
                    os.makedirs(config_dir, exist_ok=True)
                    
                    file_path = os.path.join(config_dir, f'{id_value}.cfg')
                    with open(file_path, 'w') as f:
                        f.write(config_content)
                    
                    messages.success(request, f'Пользователь {id_value} успешно создан!')
                    return redirect('combined_view')
                    
                except IntegrityError as e:
                    messages.error(request, f'Ошибка: {e}')
    
    context = {
        'aors': aors_data,
        'auth': auth_data,
        'endpoints_data': endpoints_data,
        'form': form,
        'edit_mode': bool(edit_id) and user_role == 'admin',
        'editing_user': editing_user,
        'user_role': user_role,
        'is_admin': user_role == 'admin',
        'is_reader': user_role == 'reader',
    }
    return render(request, 'combined_view.html', context)


def custom_logout(request):
    request.session.flush()
    return redirect('gate_view')


def delete_user(request, user_id):
    if request.session.get('user_role') != 'admin':
        messages.error(request, 'У вас нет прав на удаление пользователей!')
        return redirect('combined_view')
    
    if request.method == 'POST':
        try:
            endpoint = get_object_or_404(PsEndpoints, id=user_id)
            deleted_id = endpoint.id
            
            PsAors.objects.filter(id=user_id).delete()
            PsAuths.objects.filter(id=user_id).delete()
            endpoint.delete()
            
            messages.success(request, f'Пользователь {deleted_id} успешно удален!')
        except Exception as e:
            messages.error(request, f'Ошибка при удалении: {e}')
    
    return redirect('combined_view')