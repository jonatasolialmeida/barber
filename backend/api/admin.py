from django.contrib import admin
from .models import Service, Schedule, Coupon, Report, User
from django.contrib.auth.admin import UserAdmin

# Registro de Usuários
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_owner', 'is_professional', 'is_client')
    list_filter = ('is_active', 'is_staff', 'is_owner', 'is_professional', 'is_client')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_owner', 'is_professional', 'is_client')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_owner', 'is_professional', 'is_client')}),
    )

# Registro do modelo de serviço
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'value', 'image', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

# Registro do modelo de agendamento
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('client', 'professional', 'service', 'scheduled_time', 'status')
    list_filter = ('status', 'scheduled_time')
    search_fields = ('client__username', 'professional__username', 'service__title')
    ordering = ('-scheduled_time',)

# Registro do modelo de cupons
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_value', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('is_active', 'valid_from', 'valid_to')
    search_fields = ('code',)
    ordering = ('-valid_from',)

# Registro do modelo de relatórios
class ReportAdmin(admin.ModelAdmin):
    list_display = ('professional', 'total_earnings', 'report_date')
    list_filter = ('report_date',)
    search_fields = ('professional__username',)
    ordering = ('-report_date',)

# Registro das classes no Django Admin
admin.site.register(User, CustomUserAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Report, ReportAdmin)
