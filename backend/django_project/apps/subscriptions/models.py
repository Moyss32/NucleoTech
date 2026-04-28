from django.db import models
from django.contrib.auth.models import User

class Assinatura(models.Model):
    nome = models.CharField(max_length=100)
    limite_mensal = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class UsuarioAssinatura(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='assinatura_perfil')
    plano = models.ForeignKey(Assinatura, on_delete=models.SET_NULL, null=True)
    data_inicio = models.DateTimeField(auto_now_add=True)
    uso_atual = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - {self.plano.nome if self.plano else 'Sem Plano'}"
