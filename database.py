import sqlite3
import hashlib
from datetime import datetime

# conexão
def conectar():
    return sqlite3.connect("farmacia.db", check_same_thread=False)


# hash de senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


# criar tabelas
def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        preco REAL,
        estoque INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        email TEXT UNIQUE,
        senha TEXT,
        tipo TEXT
    )
    """)

    # 🔥 NOVA TABELA DE HISTÓRICO
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        acao TEXT,
        data TEXT
    )
    """)

    conn.commit()
    conn.close()


# 🔥 FUNÇÃO PARA REGISTRAR LOG
def registrar_log(conn, usuario, acao):
    cursor = conn.cursor()

    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    cursor.execute("""
    INSERT INTO historico (usuario, acao, data)
    VALUES (?, ?, ?)
    """, (usuario, acao, data))

    conn.commit()