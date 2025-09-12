from utils.database import create_tables, add_user, add_marca, add_estilo, add_tipo

# Cria as tabelas no banco de dados, se elas ainda não existirem
create_tables()

# --- Inserção de usuários de exemplo ---
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

# --- Listas de dados para seed ---
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
# --- Fim das listas de dados ---

# --- Inserção das novas categorias no banco de dados ---
print("\n--- Inserindo Marcas, Estilos e Tipos ---")
for marca in MARCAS:
    try:
        add_marca(marca)
        print(f"Marca '{marca}' inserida com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir marca '{marca}':", e)

for estilo in ESTILOS:
    try:
        add_estilo(estilo)
        print(f"Estilo '{estilo}' inserido com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir estilo '{estilo}':", e)

for tipo in TIPOS:
    try:
        add_tipo(tipo)
        print(f"Tipo '{tipo}' inserido com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir tipo '{tipo}':", e)

print('\nSeed finalizado.')
