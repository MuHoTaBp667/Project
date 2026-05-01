# myproject/middleware.py
from django.shortcuts import render
from django.urls import reverse

class PasswordGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.password = "admin123"  # ваш пароль
        
    def __call__(self, request):
        # Пути, которые не требуют пароля
        public_paths = [
            '/static/', 
            '/admin/',
            '/logout/',  # Добавляем logout в исключения
        ]
        
        for path in public_paths:
            if request.path.startswith(path):
                return self.get_response(request)
        
        # Проверяем, есть ли доступ
        if request.session.get('has_access', False):
            return self.get_response(request)
        
        # Проверяем пароль
        if request.method == 'POST' and request.POST.get('password'):
            password = request.POST.get('password')
            remember = request.POST.get('remember')
            
            if password == self.password:
                if remember:
                    request.session.set_expiry(2592000)  # 30 дней
                request.session['has_access'] = True
                return self.get_response(request)
        
        # Показываем форму
        return render(request, 'gate.html')