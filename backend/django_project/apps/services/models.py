from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Aplicativo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class ServicoApp(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    app = models.ForeignKey(Aplicativo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('servico', 'app')
