import sqlite3
import os
import hashlib

# Pastas/Arquivo
DATABASE_DIR = "data"
DATABASE = os.path.join(DATABASE_DIR, "estoque.db")
ASSETS_DIR = "assets"

# Assegura diretórios
if not os.path.exists(DATABASE_DIR):
    os.makedirs(DATABASE_DIR)
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL,
            marca TEXT,
            estilo TEXT,
            tipo TEXT,
            foto TEXT,
            data_validade TEXT
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'staff'  -- 'admin' or 'staff'
        );
    """)
    conn.commit()
    # If role column missing from legacy DB, try to add it
    try:
        cols = [c[1] for c in conn.execute("PRAGMA table_info(users)").fetchall()]
        if 'role' not in cols:
            cursor.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'staff'")
            conn.commit()
    except Exception:
        pass
    conn.close()

# ---------- Produtos CRUD ----------
def add_produto(nome, preco, quantidade, marca, estilo, tipo, foto, data_validade):
    conn = get_db_connection()
    conn.execute("""
        INSERT INTO produtos (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade))
    conn.commit()
    conn.close()

def get_all_produtos():
    conn = get_db_connection()
    produtos = conn.execute("SELECT * FROM produtos").fetchall()
    conn.close()
    return [dict(p) for p in produtos]

def get_produto_by_id(produto_id):
    conn = get_db_connection()
    p = conn.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()
    conn.close()
    return dict(p) if p else None

def update_produto(produto_id, nome, preco, quantidade, marca, estilo, tipo, foto, data_validade):
    conn = get_db_connection()
    conn.execute("""
        UPDATE produtos SET
            nome = ?, preco = ?, quantidade = ?, marca = ?, estilo = ?, tipo = ?, foto = ?, data_validade = ?
        WHERE id = ?
    """, (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade, produto_id))
    conn.commit()
    conn.close()

def is_image_used_elsewhere(photo_name, excluding_produto_id=None):
    if not photo_name:
        return False
    conn = get_db_connection()
    if excluding_produto_id is None:
        rows = conn.execute("SELECT COUNT(*) as c FROM produtos WHERE foto = ?", (photo_name,)).fetchone()
    else:
        rows = conn.execute("SELECT COUNT(*) as c FROM produtos WHERE foto = ? AND id != ?", (photo_name, excluding_produto_id)).fetchone()
    conn.close()
    return rows['c'] > 0

def delete_produto(produto_id):
    # When deleting, remove associated image file only if no other product uses it.
    produto = get_produto_by_id(produto_id)
    if not produto:
        return
    photo = produto.get('foto')
    conn = get_db_connection()
    conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    conn.close()
    if photo:
        photo_path = os.path.join(ASSETS_DIR, photo)
        try:
            if os.path.exists(photo_path) and not is_image_used_elsewhere(photo, excluding_produto_id=produto_id):
                os.remove(photo_path)
        except Exception:
            pass

# ---------- CSV Export/Import ----------
def export_produtos_to_csv(csv_path):
    import csv
    produtos = get_all_produtos()
    if not produtos:
        raise ValueError('Nenhum produto para exportar')
    keys = ['id','nome','preco','quantidade','marca','estilo','tipo','foto','data_validade']
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for p in produtos:
            writer.writerow({k: p.get(k) for k in keys})

def import_produtos_from_csv(csv_path):
    import csv
    from datetime import datetime
    conn = get_db_connection()
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # basic validation and conversion
            nome = row.get('nome')
            preco = float(row.get('preco') or 0)
            quantidade = int(float(row.get('quantidade') or 0))
            marca = row.get('marca')
            estilo = row.get('estilo')
            tipo = row.get('tipo')
            foto = row.get('foto') or None
            data_validade = row.get('data_validade') or None
            conn.execute("""INSERT INTO produtos (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (nome, preco, quantidade, marca, estilo, tipo, foto, data_validade))
    conn.commit()
    conn.close()

# ---------- Usuários ----------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def add_user(username, password, role='staff'):
    conn = get_db_connection()
    hashed = hash_password(password)
    conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, role))
    conn.commit()
    conn.close()

def get_user(username):
    conn = get_db_connection()
    u = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(u) if u else None

def get_all_users():
    conn = get_db_connection()
    rows = conn.execute("SELECT id, username, role FROM users").fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ---------- PDF Report ----------
def generate_stock_pdf(output_path):
    # uses reportlab
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    produtos = get_all_produtos()

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2*cm, height - 2*cm, "Relatório de Estoque - Cores e Fragrâncias by Berenice")
    c.setFont("Helvetica", 10)
    y = height - 3*cm
    for p in produtos:
        line = f"ID: {p.get('id')} | {p.get('nome')} - R$ {float(p.get('preco')):.2f} | Qtd: {p.get('quantidade')} | Marca: {p.get('marca')} | Validade: {p.get('data_validade') or '-'}"
        c.drawString(2*cm, y, line)
        y -= 0.7*cm
        if y < 2*cm:
            c.showPage()
            y = height - 2*cm
    c.save()
