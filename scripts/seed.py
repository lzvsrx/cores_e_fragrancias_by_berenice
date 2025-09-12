from utils.database import create_tables, add_user, add_produto
from datetime import date

create_tables()

# Insere um admin de exemplo (username: admin, senha: admin123)
try:
    add_user('admin', 'admin123', role='admin')
    print('Admin seed criado: (admin / admin123)')
except Exception as e:
    print('Erro ao criar admin seed (talvez já exista):', e)

try:
    add_user('staff', 'staff123', role='staff')
    print('Staff seed criado: (staff / staff123)')
except Exception as e:
    print('Erro ao criar staff seed (talvez já exista):', e)

# Adicionando mais produtos de exemplo com as novas categorias
produtos = [
    # Produtos de Perfumaria
    ('Perfume Floral', 129.90, 10, 'Natura', 'Perfumaria', 'Perfumaria feminina', None, date(2026, 1, 1).isoformat()),
    ('Colônia Amadeirada', 159.90, 15, 'O Boticário', 'Perfumaria', 'Perfumaria masculina', None, date(2026, 3, 15).isoformat()),
    ('Body Splash Refrescante', 49.90, 30, 'Quem Disse, Berenice?', 'Perfumaria', 'Body splash', None, date(2026, 9, 20).isoformat()),
    ('Eau de Parfum Intenso', 250.00, 5, 'Chanel', 'Perfumaria', 'Eau de parfum', None, date(2027, 2, 10).isoformat()),
    ('Desodorante Roll-On', 15.00, 50, 'Nivea', 'Perfumaria', 'Desodorantes', None, date(2025, 12, 5).isoformat()),
    
    # Produtos de Cuidados com o Corpo
    ('Hidratante Corporal', 39.90, 25, 'Eudora', 'Cuidados com o Corpo', 'Hidratante', None, date(2026, 6, 30).isoformat()),
    ('Protetor Solar FPS 50', 65.00, 20, 'Sundown', 'Cuidados com o Corpo', 'Protetor solar', None, date(2027, 4, 1).isoformat()),
    ('Sabonete Líquido Lavanda', 22.50, 40, 'Natura', 'Cuidados com o Corpo', 'Sabonetes', None, date(2026, 10, 15).isoformat()),

    # Produtos para Cabelo
    ('Shampoo Nutritivo', 24.50, 40, 'Natura', 'Cabelo', 'Shampoo', None, date(2026, 12, 31).isoformat()),
    ('Creme para Pentear', 29.90, 30, 'Seda', 'Cabelo', 'Creme para Pentear', None, date(2026, 8, 25).isoformat()),
    ('Máscara de Hidratação', 35.00, 18, 'L’Oréal', 'Cabelo', 'Máscara', None, date(2027, 1, 20).isoformat()),

    # Produtos para Rosto
    ('Sérum Anti-idade', 89.90, 15, 'Neutrogena', 'Rosto', 'Anti-idade', None, date(2027, 5, 10).isoformat()),
    ('Creme Clareador', 75.00, 12, 'La Roche-Posay', 'Rosto', 'Clareador de manchas', None, date(2026, 11, 5).isoformat()),
]

for p in produtos:
    try:
        add_produto(*p)
        print(f"Produto seed '{p[0]}' inserido com sucesso.")
    except Exception as e:
        print(f'Erro ao inserir produto seed {p[0]}:', e)

print('Seed finalizado.')
