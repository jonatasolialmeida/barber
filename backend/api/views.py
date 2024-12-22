from rest_framework import viewsets, permissions, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Service, Schedule, Coupon, Report
from .serializers import (
    UserSerializer,
    ServiceSerializer,
    ScheduleSerializer,
    CouponSerializer,
    ReportSerializer,
)
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Permissão para donos do estabelecimento."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_owner or request.method in permissions.SAFE_METHODS

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar usuários."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_owner:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar serviços."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class ScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar agendamentos."""
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_client:
            return Schedule.objects.filter(client=user)
        elif user.is_professional:
            return Schedule.objects.filter(professional=user)
        elif user.is_owner:
            return Schedule.objects.all()
        return Schedule.objects.none()

    def perform_create(self, serializer):
        """Associa o cliente autenticado ao criar um agendamento."""
        serializer.save(client=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_schedule(self, request):
        """Retorna a agenda do usuário autenticado."""
        if request.user.is_client:
            schedules = Schedule.objects.filter(client=request.user)
        elif request.user.is_professional:
            schedules = Schedule.objects.filter(professional=request.user)
        else:
            schedules = Schedule.objects.none()
        serializer = self.get_serializer(schedules, many=True)
        return Response(serializer.data)

class CouponViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciar cupons."""
    queryset = Coupon.objects.filter(is_active=True, valid_to__gte=now())
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para relatórios dos profissionais."""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_professional:
            return Report.objects.filter(professional=self.request.user)
        elif self.request.user.is_owner:
            return Report.objects.all()
        return Report.objects.none()

class SearchServicesView(generics.ListAPIView):
    """View para buscar serviços."""
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']
