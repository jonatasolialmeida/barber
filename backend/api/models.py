from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Modelo personalizado para usuários."""
    is_client = models.BooleanField(default=False, verbose_name=_("Cliente"))
    is_professional = models.BooleanField(default=False, verbose_name=_("Profissional"))
    is_owner = models.BooleanField(default=False, verbose_name=_("Dono do Estabelecimento"))

class Service(models.Model):
    """Modelo para serviços da barbearia."""
    title = models.CharField(max_length=100, verbose_name=_("Título"))
    description = models.TextField(blank=True, verbose_name=_("Descrição"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Preço"))
    image = models.ImageField(upload_to='services/', blank=True, null=True, verbose_name=_("Imagem"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))

    def __str__(self):
        return self.title

class Schedule(models.Model):
    """Modelo para agendamentos."""
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='schedules', limit_choices_to={'is_client': True},
        verbose_name=_("Cliente")
    )
    professional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='appointments', limit_choices_to={'is_professional': True},
        verbose_name=_("Profissional")
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_("Serviço"))
    date = models.DateField(verbose_name=_("Data"))
    time = models.TimeField(verbose_name=_("Horário"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))

    class Meta:
        unique_together = ('professional', 'date', 'time')
        verbose_name = _("Agendamento")
        verbose_name_plural = _("Agendamentos")

    def __str__(self):
        return f"{self.client.username} - {self.service.title} em {self.date} às {self.time}"

class Coupon(models.Model):
    """Modelo para cupons de desconto."""
    code = models.CharField(max_length=50, unique=True, verbose_name=_("Código"))
    discount_percentage = models.PositiveIntegerField(verbose_name=_("Desconto (%)"))
    valid_from = models.DateTimeField(verbose_name=_("Válido de"))
    valid_to = models.DateTimeField(verbose_name=_("Válido até"))
    is_active = models.BooleanField(default=True, verbose_name=_("Ativo"))

    def __str__(self):
        return self.code

class Report(models.Model):
    """Modelo para relatórios de ganhos dos profissionais."""
    professional = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reports', limit_choices_to={'is_professional': True},
        verbose_name=_("Profissional")
    )
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Ganhos Totais"))
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Gerado em"))

    def __str__(self):
        return f"Relatório de {self.professional.username} - {self.generated_at.date()}"
