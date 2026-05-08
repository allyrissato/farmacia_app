def inserir_produtos_iniciais(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM produtos")
    if cursor.fetchone()[0] > 0:
        return

    produtos = [
        ("Dipirona", 10.0, 5),
        ("Paracetamol", 8.0, 10),
        ("Ibuprofeno", 15.0, 7),
        ("Vitamina C", 20.0, 3),
        ("Amoxicilina", 30.0, 2),
        ("Aspirina", 12.0, 6),
        ("Dorflex", 18.0, 4),
        ("Buscopan", 22.0, 5),
        ("Omeprazol", 25.0, 8),
        ("Antialérgico", 17.0, 6),
    ]

    cursor.executemany("""
    INSERT INTO produtos (nome, preco, estoque)
    VALUES (?, ?, ?)
    """, produtos)

    conn.commit()