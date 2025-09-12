# Script para popular a base com usuários e alguns produtos de exemplo.
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

# Produtos de exemplo
produtos = [
    ('Perfume Floral', 129.90, 10, 'Natura', 'Perfumaria', 'Perfumaria feminina', None, date(2026,1,1).isoformat()),
    ('Hidratante Corporal', 39.90, 25, 'Eudora', 'Cuidados com o Corpo', 'Hidratante', None, date(2026,6,30).isoformat()),
    ('Shampoo Nutritivo', 24.50, 40, 'Natura', 'Cabelo', 'Shampoo', None, date(2026,12,31).isoformat()),
]

for p in produtos:
    try:
        add_produto(*p)
    except Exception as e:
        print('Erro ao inserir produto seed:', e)

print('Seed finalizado.')
