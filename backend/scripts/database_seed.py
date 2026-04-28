import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(__file__), '../django_project'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from apps.services.models import Servico, Aplicativo, ServicoApp
from apps.subscriptions.models import Assinatura

def seed():
    print("Iniciando seed do banco de dados...")
    
    # Criar Aplicativo
    app, _ = Aplicativo.objects.get_or_create(
        nome="NucleoTech Web",
        descricao="Plataforma principal NucleoTech"
    )
    
    # Criar Serviços
    servicos_data = [
        {'nome': 'Remover Fundo', 'slug': 'remove-bg', 'descricao': 'Remove o fundo de imagens usando IA.'},
        {'nome': 'Upscale', 'slug': 'upscale', 'descricao': 'Aumenta a resolução da imagem.'},
        {'nome': 'Converter Imagem', 'slug': 'convert-image', 'descricao': 'Converte imagens entre formatos.'},
        {'nome': 'Gerar Thumbnail', 'slug': 'thumbnail', 'descricao': 'Gera miniaturas de imagens.'},
        {'nome': 'Converter Áudio', 'slug': 'convert-audio', 'descricao': 'Converte arquivos de áudio.'},
    ]
    
    for s_data in servicos_data:
        servico, created = Servico.objects.get_or_create(
            slug=s_data['slug'],
            defaults={'nome': s_data['nome'], 'descricao': s_data['descricao']}
        )
        ServicoApp.objects.get_or_create(servico=servico, app=app)
        if created:
            print(f"Serviço criado: {servico.nome}")

    # Criar Planos
    planos_data = [
        {'nome': 'Gratuito', 'limite_mensal': 10, 'preco': 0.00, 'descricao': 'Plano básico para testes.'},
        {'nome': 'Pro', 'limite_mensal': 100, 'preco': 49.90, 'descricao': 'Plano para profissionais.'},
        {'nome': 'Enterprise', 'limite_mensal': 1000, 'preco': 199.90, 'descricao': 'Plano para empresas.'},
    ]
    
    for p_data in planos_data:
        plano, created = Assinatura.objects.get_or_create(
            nome=p_data['nome'],
            defaults={
                'limite_mensal': p_data['limite_mensal'],
                'preco': p_data['preco'],
                'descricao': p_data['descricao']
            }
        )
        if created:
            print(f"Plano criado: {plano.nome}")

    print("Seed finalizado com sucesso!")

if __name__ == '__main__':
    seed()
