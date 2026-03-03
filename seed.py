from app import create_app, db
from app.models.models import Product, User
from app import bcrypt

app = create_app()

def seed():
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if products already exist
        if Product.query.count() > 0:
            print("Banco de dados já contém produtos.")
            return

        # Initial Products
        products = [
            Product(
                name="NucleoERP Enterprise",
                description="Sistema completo de gestão empresarial com módulos de financeiro, estoque e vendas.",
                price=2499.90,
                category="Sistemas Empresariais",
                benefits="Otimização de processos, relatórios em tempo real, integração total.",
                specifications="Requer Windows 10+, 8GB RAM, 500MB de disco."
            ),
            Product(
                name="OfficePro Suite 2026",
                description="Conjunto de ferramentas de produtividade para escritório, incluindo editor de texto e planilhas.",
                price=599.00,
                category="Ferramentas de Produtividade",
                benefits="Interface intuitiva, compatibilidade universal, suporte a nuvem.",
                specifications="Multiplataforma (Windows, macOS, Linux)."
            ),
            Product(
                name="CyberShield Antivirus",
                description="Proteção avançada contra malwares, ransomwares e ameaças digitais em tempo real.",
                price=149.90,
                category="Soluções Tecnológicas",
                benefits="Proteção 24/7, baixo consumo de recursos, firewall inteligente.",
                specifications="Licença anual para até 3 dispositivos."
            ),
            Product(
                name="CloudSync Pro",
                description="Serviço de armazenamento e sincronização de arquivos em nuvem com criptografia de ponta a ponta.",
                price=29.90,
                category="Ferramentas de Produtividade",
                benefits="Acesso de qualquer lugar, backup automático, compartilhamento seguro.",
                specifications="1TB de armazenamento, suporte a versionamento."
            ),
            Product(
                name="DevStack IDE Premium",
                description="Ambiente de desenvolvimento integrado para programadores profissionais com suporte a múltiplas linguagens.",
                price=899.00,
                category="Ferramentas de Produtividade",
                benefits="Autocompletar inteligente, depurador avançado, integração com Git.",
                specifications="Requer 16GB RAM para melhor performance."
            )
        ]

        db.session.bulk_save_objects(products)
        
        # Create an admin user if not exists
        if not User.query.filter_by(email='admin@nucleotech.com').first():
            hashed_pw = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(username='admin', email='admin@nucleotech.com', password=hashed_pw, is_admin=True)
            db.session.add(admin)
            print("Usuário admin criado: admin@nucleotech.com / admin123")

        db.session.commit()
        print("Banco de dados semeado com sucesso!")

if __name__ == '__main__':
    seed()
