from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Service, Schedule, Coupon, Report

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializador para o modelo personalizado de usuário."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_client', 'is_professional', 'is_owner']

class ServiceSerializer(serializers.ModelSerializer):
    """Serializador para o modelo de serviços."""

    class Meta:
        model = Service
        fields = ['id', 'title', 'description', 'price', 'image', 'created_at']

class ScheduleSerializer(serializers.ModelSerializer):
    """Serializador para o modelo de agendamentos."""
    client = UserSerializer(read_only=True)  # Apenas leitura para evitar que clientes enviem dados inválidos
    professional = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(is_professional=True))
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = Schedule
        fields = ['id', 'client', 'professional', 'service', 'date', 'time', 'created_at']
        read_only_fields = ['created_at']

    def create(self, validated_data):
        """Adiciona o cliente autenticado ao criar um agendamento."""
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            validated_data['client'] = request.user
        return super().create(validated_data)

class CouponSerializer(serializers.ModelSerializer):
    """Serializador para o modelo de cupons."""

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'discount_percentage', 'valid_from', 'valid_to', 'is_active']

class ReportSerializer(serializers.ModelSerializer):
    """Serializador para o modelo de relatórios."""
    professional = UserSerializer(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'professional', 'total_earnings', 'generated_at']
        read_only_fields = ['generated_at']
