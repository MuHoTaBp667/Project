# myproject/middleware.py
from django.shortcuts import render, redirect
from django.urls import reverse

class PasswordGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Пути, которые не требуют пароля
        public_paths = ['/static/', '/admin/']
        
        for path in public_paths:
            if request.path.startswith(path):
                return self.get_response(request)
        
        # Проверяем авторизацию
        if request.session.get('user_role'):
            return self.get_response(request)
        
        # Страница входа
        if request.path == '/' or request.path == '/gate/':
            return self.get_response(request)
        
        # Все остальное - редирект на вход
        return redirect('gate_view')