from utils.database import create_tables, add_user, add_produto, add_marca, add_estilo, add_tipo
from datetime import date

# --- Adicionando as novas listas ao código ---
MARCAS = ["Eudora", "O Boticário", "Jequiti", "Avon", "Mary Kay", "Natura", "Quem Disse, Berenice?", "Chanel", "Nivea", "Sundown", "Seda", "L’Oréal", "Neutrogena", "La Roche-Posay"]
ESTILOS = [
    "Perfumaria", "Skincare", "Cabelo", "Corpo e Banho", "Make", "Masculinos", "Femininos Nina Secrets",
    "Marcas", "Infantil", "Casa", "Solar", "Maquiage", "Teen", "Kits e Presentes",
    "Cuidados com o Corpo", "Lançamentos", "Rosto"
]
TIPOS = [
    "Perfumaria masculina", "Perfumaria feminina", "Body splash", "Body spray", "Eau de parfum",
    "Desodorantes", "Perfumaria infantil", "Perfumaria vegana", "Familia olfativa",
    "Clareador de manchas", "Anti-idade", "Protetor solar facial", "Rosto",
    "Tratamento para o rosto", "Acne", "Limpeza", "Esfoliante", "Tônico facial",
    "Kits de tratamento", "Tratamento para cabelos", "Shampoo", "Condicionador",
    "Leave-in e Creme para Pentear", "Finalizador", "Modelador", "Acessórios",
    "Kits e looks", "Boca", "Olhos", "Pincéis", "Paleta", "Unhas", "Sobrancelhas",
    "Kits de tratamento", "Hidratante", "Cuidados pós-banho", "Cuidados para o banho",
    "Barba", "Óleo corporal", "Cuidados íntimos", "Unissex", "Bronzeamento",
    "Protetor solar", "Depilação", "Mãos", "Lábios", "Pés", "Pós sol",
    "Protetor solar corporal", "Colônias", "Estojo", "Sabonetes",
    "Creme hidratante para as mãos", "Creme hidratante para os pés", "Miniseries",
    "Kits de perfumes", "Antissinais", "Máscara", "Creme bisnaga",
    "Roll On Fragranciado", "Roll On On Duty", "Sabonete líquido",
    "Sabonete em barra", "Shampoo 2 em 1", "Spray corporal", "Booster de Tratamento",
    "Creme para Pentear", "Óleo de Tratamento", "Pré-shampoo",
    "Sérum de Tratamento", "Shampoo e Condicionador"
]
# --- Fim das listas ---

create_tables()

# Inserção de usuários de exemplo
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

# Inserção das novas categorias
print("\n--- Inserindo Marcas, Estilos e Tipos ---")
for marca in MARCAS:
    try:
        add_marca(marca)
    except Exception as e:
        print(f"Erro ao inserir marca '{marca}':", e)

for estilo in ESTILOS:
    try:
        add_estilo(estilo)
    except Exception as e:
        print(f"Erro ao inserir estilo '{estilo}':", e)

for tipo in TIPOS:
    try:
        add_tipo(tipo)
    except Exception as e:
        print(f"Erro ao inserir tipo '{tipo}':", e)

# Adicionando produtos de exemplo
print("\n--- Inserindo Produtos ---")
produtos = [
    ('Perfume Floral', 129.90, 10, 'Natura', 'Perfumaria', 'Perfumaria feminina', None, date(2026, 1, 1).isoformat()),
    ('Colônia Amadeirada', 159.90, 15, 'O Boticário', 'Perfumaria', 'Perfumaria masculina', None, date(2026, 3, 15).isoformat()),
    ('Body Splash Refrescante', 49.90, 30, 'Quem Disse, Berenice?', 'Perfumaria', 'Body splash', None, date(2026, 9, 20).isoformat()),
    ('Eau de Parfum Intenso', 250.00, 5, 'Chanel', 'Perfumaria', 'Eau de parfum', None, date(2027, 2, 10).isoformat()),
    ('Desodorante Roll-On', 15.00, 50, 'Nivea', 'Perfumaria', 'Desodorantes', None, date(2025, 12, 5).isoformat()),
    ('Hidratante Corporal', 39.90, 25, 'Eudora', 'Cuidados com o Corpo', 'Hidratante', None, date(2026, 6, 30).isoformat()),
    ('Protetor Solar FPS 50', 65.00, 20, 'Sundown', 'Cuidados com o Corpo', 'Protetor solar', None, date(2027, 4, 1).isoformat()),
    ('Sabonete Líquido Lavanda', 22.50, 40, 'Natura', 'Cuidados com o Corpo', 'Sabonetes', None, date(2026, 10, 15).isoformat()),
    ('Shampoo Nutritivo', 24.50, 40, 'Natura', 'Cabelo', 'Shampoo', None, date(2026, 12, 31).isoformat()),
    ('Creme para Pentear', 29.90, 30, 'Seda', 'Cabelo', 'Creme para Pentear', None, date(2026, 8, 25).isoformat()),
    ('Máscara de Hidratação', 35.00, 18, 'L’Oréal', 'Cabelo', 'Máscara', None, date(2027, 1, 20).isoformat()),
    ('Sérum Anti-idade', 89.90, 15, 'Neutrogena', 'Rosto', 'Anti-idade', None, date(2027, 5, 10).isoformat()),
    ('Creme Clareador', 75.00, 12, 'La Roche-Posay', 'Rosto', 'Clareador de manchas', None, date(2026, 11, 5).isoformat()),
]

for p in produtos:
    try:
        add_produto(*p)
        print(f"Produto seed '{p[0]}' inserido com sucesso.")
    except Exception as e:
        print(f'Erro ao inserir produto seed {p[0]}:', e)

print('\nSeed finalizado.')
