import streamlit as st
from database import conectar, criar_tabelas, hash_senha, registrar_log
from produtos import inserir_produtos_iniciais
import base64

# IMAGENS
imagens = {
    "Dipirona": "images/dipirona.png",
    "Paracetamol": "images/paracetamol.png",
    "Ibuprofeno": "images/ibuprofeno.png",
    "Vitamina C": "images/vitamina_c.png",
    "Amoxicilina": "images/amoxicilina.png",
    "Aspirina": "images/aspirina.png",
    "Dorflex": "images/dorflex.png",
    "Omeprazol": "images/omeprazol.png",
    "Buscopan": "images/buscopan.png",
    "Antialérgico": "images/antialergico.png",
}

# CONFIG
st.set_page_config(page_title="Farmácia Online", layout="centered")

# CSS
def carregar_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_css()

# BANCO
criar_tabelas()
conn = conectar()
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM produtos")
if cursor.fetchone()[0] == 0:
    inserir_produtos_iniciais(conn)

# ESTADO
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

if "carrinho" not in st.session_state:
    st.session_state.carrinho = {}

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "tipo_cadastro" not in st.session_state:
    st.session_state.tipo_cadastro = "cliente"

if "aba_funcionario" not in st.session_state:
    st.session_state.aba_funcionario = "estoque"

if "pesquisa" not in st.session_state:
    st.session_state.pesquisa = ""

if "mensagem" not in st.session_state:
    st.session_state.mensagem = ""

# LOGO
with open("images/logo.png", "rb") as img_file:
    logo_base64 = base64.b64encode(img_file.read()).decode()

st.markdown(f"""
<div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px;">
    <img src="data:image/png;base64,{logo_base64}" width="150">
</div>
""", unsafe_allow_html=True)

# ----------------------
# CADASTRO
# ----------------------
if st.session_state.pagina == "inicio":

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown('<div class="login-title">Criar Conta</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Preencha os dados abaixo</div>', unsafe_allow_html=True)

        nome = st.text_input("", placeholder="Nome completo")
        email = st.text_input("", placeholder="E-mail")
        senha = st.text_input("", placeholder="Senha", type="password")

        st.markdown("<br>", unsafe_allow_html=True)

        colA, colB = st.columns(2)

        with colA:

            if st.session_state.tipo_cadastro == "cliente":
                st.button("Cliente", use_container_width=True, disabled=True)

            else:
                if st.button("Cliente", use_container_width=True):
                    st.session_state.tipo_cadastro = "cliente"
                    st.rerun()

        with colB:

            if st.session_state.tipo_cadastro == "funcionario":
                st.button("Funcionário", use_container_width=True, disabled=True)

            else:
                if st.button("Funcionário", use_container_width=True):
                    st.session_state.tipo_cadastro = "funcionario"
                    st.rerun()

        if st.button("Criar conta", use_container_width=True):

            if nome == "" or email == "" or senha == "":
                st.warning("Preencha todos os campos!")

            elif "@" not in email or "." not in email:
                st.warning("Digite um e-mail válido!")

            else:

                cursor.execute(
                    "SELECT * FROM usuarios WHERE email=?",
                    (email,)
                )

                usuario_existente = cursor.fetchone()

                if usuario_existente:
                    st.error("Esse e-mail já está cadastrado!")

                else:

                    cursor.execute(
                        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                        (nome, email, hash_senha(senha), st.session_state.tipo_cadastro)
                    )

                    conn.commit()
                    st.success("Conta criada!")

        if st.button("Já tem conta? Fazer login", use_container_width=True):
            st.session_state.pagina = "login"
            st.rerun()

# ----------------------
# LOGIN
# ----------------------
elif st.session_state.pagina == "login":

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        st.markdown('<div class="login-title">Entrar</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">Digite seu e-mail e senha</div>', unsafe_allow_html=True)

        email = st.text_input("", placeholder="E-mail")
        senha = st.text_input("", placeholder="Senha", type="password")

        if st.button("Entrar", use_container_width=True):

            cursor.execute(
                "SELECT * FROM usuarios WHERE email=?",
                (email,)
            )

            usuario_email = cursor.fetchone()

            if not usuario_email:

                st.error("E-mail não cadastrado.")

            else:

                cursor.execute(
                    "SELECT * FROM usuarios WHERE email=? AND senha=?",
                    (email, hash_senha(senha))
                )

                user = cursor.fetchone()

                if user:
                    st.session_state.usuario = user
                    st.session_state.pagina = user[4]
                    st.rerun()

                else:
                    st.error("Senha incorreta.")

        if st.button("Voltar", use_container_width=True):
            st.session_state.pagina = "inicio"
            st.rerun()

# ----------------------
# CLIENTE
# ----------------------
elif st.session_state.pagina == "cliente" and st.session_state.usuario:

    nome_usuario = st.session_state.usuario[1]

    st.title("Nossa Farmácia — Loja")
    st.markdown(f"### 👋 Bem-vindo, {nome_usuario.capitalize()}!")

    # PESQUISA
    pesquisa = st.text_input(
        "",
        placeholder="🔍 Pesquisar produto..."
    )

    cursor.execute("SELECT * FROM produtos WHERE estoque > 0")
    produtos = cursor.fetchall()

    if pesquisa:

        produtos = [
            p for p in produtos
            if pesquisa.lower() in p[1].lower()
        ]

    for i in range(0, len(produtos), 2):

        cols = st.columns(2 if i + 1 < len(produtos) else 1)

        for j in range(len(cols)):

            if i + j < len(produtos):

                id, nome, preco, estoque = produtos[i + j]
                img = imagens.get(nome, "")

                with cols[j]:

                    col_img, col_info = st.columns([1, 2])

                    with col_img:

                        if img:
                            st.image(img, use_container_width=True)

                    with col_info:

                        st.markdown(f"""
                        <div class="card">
                            <h3>{nome}</h3>
                            <p>💰 R$ {preco}</p>
                            <p>📦 {estoque} disponíveis</p>
                        </div>
                        """, unsafe_allow_html=True)

                        if st.button("Adicionar", key=f"add_{id}"):

                            qtd_carrinho = st.session_state.carrinho.get(id, 0)

                            if qtd_carrinho < estoque:

                                st.session_state.carrinho[id] = qtd_carrinho + 1

                                st.toast(f"{nome} adicionado ao carrinho 🛒")

                            else:
                                st.warning(f"Estoque máximo disponível para {nome}.")

        st.markdown("<hr>", unsafe_allow_html=True)

    # CARRINHO
    st.markdown("## 🛒 Carrinho")

    if len(st.session_state.carrinho) == 0:
        st.info("Seu carrinho está vazio.")

    total = 0

    for id, qtd in list(st.session_state.carrinho.items()):

        cursor.execute(
            "SELECT nome, preco, estoque FROM produtos WHERE id=?",
            (id,)
        )

        nome_p, preco, estoque_atual = cursor.fetchone()

        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.markdown(
                f"<div class='carrinho'>{nome_p} — {qtd}x</div>",
                unsafe_allow_html=True
            )

        with col2:

            if st.button("➖", key=f"rem_{id}"):

                if qtd > 1:
                    st.session_state.carrinho[id] -= 1

                else:
                    del st.session_state.carrinho[id]

                st.rerun()

        with col3:

            if st.button("➕", key=f"add_cart_{id}"):

                if st.session_state.carrinho[id] < estoque_atual:
                    st.session_state.carrinho[id] += 1
                    st.rerun()

                else:
                    st.warning("Limite do estoque atingido.")

        with col4:

            if st.button("🗑", key=f"del_{id}"):

                del st.session_state.carrinho[id]
                st.rerun()

        total += preco * qtd

    st.markdown(f"## 💰 Total: R$ {total:.2f}")

    # FINALIZAR COMPRA
    if st.session_state.carrinho:

        if st.button("Finalizar Compra", use_container_width=True):

            for id, qtd in st.session_state.carrinho.items():

                cursor.execute(
                    "SELECT nome, estoque FROM produtos WHERE id=?",
                    (id,)
                )

                nome_produto, estoque_atual = cursor.fetchone()

                novo_estoque = max(0, estoque_atual - qtd)

                cursor.execute(
                    "UPDATE produtos SET estoque=? WHERE id=?",
                    (novo_estoque, id)
                )

                registrar_log(
                    conn,
                    nome_usuario,
                    f"comprou {qtd}x {nome_produto}"
                )

                if novo_estoque == 0:

                    registrar_log(
                        conn,
                        nome_usuario,
                        f"estoque de {nome_produto} acabou"
                    )

            conn.commit()

            st.session_state.carrinho = {}

            st.balloons()
            st.success("Compra realizada com sucesso!")
            st.rerun()

        if st.button("Limpar carrinho", use_container_width=True):

            st.session_state.carrinho = {}
            st.rerun()

    if st.button("Logout", use_container_width=True):

        st.session_state.usuario = None
        st.session_state.pagina = "inicio"
        st.rerun()
# ----------------------
# FUNCIONARIO
# ----------------------
elif st.session_state.pagina == "funcionario" and st.session_state.usuario:

    nome_usuario = st.session_state.usuario[1]

    st.title("Painel do Funcionário")
    st.markdown(f"### 👋 Bem-vindo, {nome_usuario.capitalize()}!")

    # MENU
    col1, col2 = st.columns(2)

    with col1:

        if st.session_state.aba_funcionario == "estoque":
            st.button("Estoque", use_container_width=True, disabled=True)

        else:
            if st.button("Estoque", use_container_width=True):
                st.session_state.aba_funcionario = "estoque"
                st.rerun()

    with col2:

        if st.session_state.aba_funcionario == "historico":
            st.button("Histórico", use_container_width=True, disabled=True)

        else:
            if st.button("Histórico", use_container_width=True):
                st.session_state.aba_funcionario = "historico"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ESTOQUE
    if st.session_state.aba_funcionario == "estoque":

        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

        for p in produtos:

            id, nome, preco, estoque = p
            img = imagens.get(nome, "")

            st.markdown('<div class="card">', unsafe_allow_html=True)

            col_img, col_info, col_input, col_btn = st.columns([1, 3, 2, 2])

            with col_img:

                if img:
                    st.image(img, width=80)

            with col_info:

                alerta = ""

                # ALERTA VERMELHO
                if estoque == 0:
                    alerta = "<span style='color:red; font-size:24px;'>❗</span>"

                # ALERTA AMARELO
                elif estoque <= 5:
                    alerta = "<span style='color:#facc15; font-size:24px;'>❗</span>"

                st.markdown(f"""
                <h3>{nome} {alerta}</h3>
                <p>R$ {preco}</p>
                <p>📦 Estoque atual: {estoque}</p>
                """, unsafe_allow_html=True)

            with col_input:

                novo = st.number_input(
                    "Qtd",
                    min_value=0,
                    value=estoque,
                    key=f"estoque_{id}",
                    label_visibility="collapsed"
                )

            with col_btn:

                if st.button("Atualizar", key=f"update_{id}", use_container_width=True):

                    cursor.execute(
                        "UPDATE produtos SET estoque=? WHERE id=?",
                        (novo, id)
                    )

                    conn.commit()

                    registrar_log(
                        conn,
                        nome_usuario,
                        f"alterou {nome} para {novo} unidades"
                    )

                    if novo == 0:

                        registrar_log(
                            conn,
                            nome_usuario,
                            f"estoque de {nome} acabou"
                        )

                    st.success("Atualizado!")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    # HISTÓRICO
    elif st.session_state.aba_funcionario == "historico":

        st.subheader("Histórico de alterações")

        cursor.execute(
            "SELECT usuario, acao, data FROM historico ORDER BY id DESC"
        )

        logs = cursor.fetchall()

        for user, acao, data in logs:

            st.markdown(f"""
            <div class="card">
                <b>{user}</b> → {acao}
                <br>
                <small style="color: #94a3b8;">{data}</small>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Logout", use_container_width=True):

        st.session_state.usuario = None
        st.session_state.pagina = "inicio"
        st.rerun()