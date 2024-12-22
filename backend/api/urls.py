from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ServiceViewSet,
    ScheduleViewSet,
    CouponViewSet,
    ReportViewSet,
    SearchServicesView,
)

# Cria o roteador padrão para ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'services', ServiceViewSet, basename='service')
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'coupons', CouponViewSet, basename='coupon')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),  # Inclui as rotas geradas pelo roteador
    path('search-services/', SearchServicesView.as_view(), name='search-services'),
]
