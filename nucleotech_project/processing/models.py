from django.db import models
from users.models import User
from services.models import Service

class Uso_Servico(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    usage_date = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.usage_date}"

class Execucao_Local(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50)
    details = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.status}"

class Arquivo_Processado(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255)
    stored_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    file_size = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.original_filename

class Resultado_Processamento(models.Model):
    processed_file = models.ForeignKey(Arquivo_Processado, on_delete=models.CASCADE)
    service_used = models.ForeignKey(Service, on_delete=models.CASCADE)
    result_filename = models.CharField(max_length=255)
    result_file_type = models.CharField(max_length=50)
    result_file_size = models.IntegerField()
    processing_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.result_filename
