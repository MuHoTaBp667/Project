from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import PsAors, PsAuths, PsEndpoints

# Расширяем админку пользователей
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('username', 'email')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Права доступа', {
            'fields': ('groups', 'user_permissions'),
        }),
    )

# Переопределяем админку групп
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Регистрируем модели пользователей
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)

# Настройка отображения моделей Asterisk с read-only доступом
@admin.register(PsEndpoints)
class PsEndpointsAdmin(admin.ModelAdmin):
    list_display = ('id', 'context', 'callerid', 'tnumber', 'transport')
    search_fields = ('id', 'callerid', 'tnumber')
    list_filter = ('context', 'transport')
    
    def get_readonly_fields(self, request, obj=None):
        # Проверяем, есть ли пользователь в группе "read_only"
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return []
    
    def has_add_permission(self, request):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

@admin.register(PsAors)
class PsAorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact', 'max_contacts', 'qualify_frequency')
    search_fields = ('id', 'contact')
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return []
    
    def has_add_permission(self, request):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

@admin.register(PsAuths)
class PsAuthsAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'auth_type', 'realm')
    search_fields = ('id', 'username')
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return []
    
    def has_add_permission(self, request):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_add_permission(request)
    
    def has_delete_permission(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if request.user.groups.filter(name='read_only').exists() and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)