import os
import sys
import django

# Add the project directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'django_project'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from apps.services.models import Servico, Aplicativo, ServicoApp
from apps.subscriptions.models import Assinatura

def seed():
    print("Iniciando seed do banco de dados...")
    
    # 1. Aplicativo
    app, _ = Aplicativo.objects.get_or_create(
        nome="FileProcessor Pro",
        defaults={'descricao': "Plataforma completa de processamento de arquivos."}
    )
    
    # 2. Serviços
    servicos = [
        {'nome': 'Remover Fundo', 'slug': 'remove-bg', 'descricao': 'Remove o fundo de imagens usando IA.'},
        {'nome': 'Upscale IA', 'slug': 'upscale', 'descricao': 'Aumenta a resolução de imagens usando IA.'},
        {'nome': 'Converter Imagem', 'slug': 'convert-image', 'descricao': 'Converte imagens entre diferentes formatos.'},
        {'nome': 'Gerar Thumbnail', 'slug': 'thumbnail', 'descricao': 'Gera miniaturas de imagens.'},
        {'nome': 'Converter Áudio', 'slug': 'convert-audio', 'descricao': 'Converte arquivos de áudio entre diferentes formatos.'},
    ]
    
    for s in servicos:
        servico, created = Servico.objects.get_or_create(
            slug=s['slug'],
            defaults={'nome': s['nome'], 'descricao': s['descricao']}
        )
        ServicoApp.objects.get_or_create(servico=servico, app=app)
        if created:
            print(f"Serviço criado: {s['nome']}")

    # 3. Planos (Assinaturas)
    planos = [
        {
            'nome': 'Gratuito', 
            'limite_mensal': 10, 
            'limite_diario': 2, 
            'limite_tamanho_arquivo_mb': 5, 
            'preco': 0.00, 
            'descricao': 'Plano básico para testes.',
            'acesso_upscale': False
        },
        {
            'nome': 'Pro', 
            'limite_mensal': 100, 
            'limite_diario': 10, 
            'limite_tamanho_arquivo_mb': 50, 
            'preco': 29.90, 
            'descricao': 'Plano ideal para profissionais.',
            'acesso_upscale': True,
            'stripe_price_id': 'price_pro_placeholder'
        },
        {
            'nome': 'Enterprise', 
            'limite_mensal': 1000, 
            'limite_diario': 50, 
            'limite_tamanho_arquivo_mb': 500, 
            'preco': 99.90, 
            'descricao': 'Para grandes volumes de processamento.',
            'acesso_upscale': True,
            'prioridade_fila': 1,
            'stripe_price_id': 'price_enterprise_placeholder'
        },
    ]
    
    for p in planos:
        assinatura, created = Assinatura.objects.update_or_create(
            nome=p['nome'],
            defaults=p
        )
        if created:
            print(f"Plano criado: {p['nome']}")
        else:
            print(f"Plano atualizado: {p['nome']}")

    print("Seed concluído com sucesso!")

if __name__ == '__main__':
    seed()
