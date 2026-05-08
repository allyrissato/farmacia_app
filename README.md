# 💊 Nossa Farmácia — Sistema Web de Gestão Farmacêutica

Sistema web desenvolvido para simular uma farmácia digital integrada à distribuidora **REMÉDIO**, permitindo gerenciamento de produtos, controle de estoque e realização de compras online.

O projeto foi desenvolvido utilizando Python, Streamlit e SQLite, integrando front-end, back-end e banco de dados em uma única aplicação.

---

# 🚀 Tecnologias Utilizadas

- Python
- Streamlit
- SQLite
- SQL
- SHA-256
- CSS personalizado

---

# 🎯 Objetivo do Projeto

O sistema foi criado para simular um ambiente real de gestão farmacêutica, permitindo:

- Controle de estoque
- Gerenciamento de produtos
- Cadastro e autenticação de usuários
- Controle de compras
- Rastreabilidade de operações
- Atualização automática do estoque

---

# ✨ Funcionalidades

## 👤 Área do Cliente

- Cadastro de usuários
- Login no sistema
- Visualização de produtos
- Pesquisa de medicamentos
- Carrinho de compras
- Alteração de quantidades
- Finalização de pedidos

## 🛠️ Área do Funcionário

- Controle de estoque
- Atualização de produtos
- Gerenciamento de inventário
- Histórico de ações realizadas
- Administração do sistema

---

# 🔐 Segurança

O sistema possui:

- Criptografia de senhas utilizando SHA-256
- Controle de permissões por perfil
- Validação de usuários
- Restrição de acesso administrativo
- Controle de integridade de dados

---

# 🗂️ Estrutura do Projeto

```bash
farmacia_app/
│
├── app.py
├── database.py
├── produtos.py
├── style.css
│
├── images/
│   ├── amoxicilina.png
│   ├── antialergico.png
│   ├── aspirina.png
│   ├── buscopan.png
│   ├── dipirona.png
│   ├── dorflex.png
│   ├── ibuprofeno.png
│   ├── logo.png
│   ├── omeprazol.png
│   ├── paracetamol.png
│   └── vitamina_c.png
│
├── Programa em funcionamento.mp4
└── README.md
```

---

# 🧠 Arquitetura do Sistema

O projeto utiliza uma arquitetura integrada onde:

- O front-end captura as interações do usuário
- O back-end processa as regras de negócio
- O SQLite armazena os dados do sistema

Todo o fluxo da aplicação ocorre dentro do próprio Streamlit.

---

# 🗄️ Banco de Dados

O sistema utiliza SQLite para armazenamento das informações.

O banco de dados é criado e gerenciado automaticamente através do arquivo:

```bash
database.py
```

O sistema possui tabelas para:

- Usuários
- Produtos
- Histórico de ações

---

# ⚙️ Como Executar o Projeto

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seuusuario/nossa-farmacia.git
```

---

## 2️⃣ Entrar na pasta do projeto

```bash
cd farmacia_app
```

---

## 3️⃣ Instalar dependências

```bash
pip install streamlit
```

---

## 4️⃣ Executar aplicação

```bash
streamlit run app.py
```

---

# 📌 Funcionalidades Implementadas

✔ Cadastro de usuários  
✔ Login e autenticação  
✔ Controle de perfis  
✔ Cadastro de produtos  
✔ Pesquisa de produtos  
✔ Carrinho de compras  
✔ Finalização de pedidos  
✔ Controle de estoque  
✔ Histórico de ações  
✔ Interface personalizada com CSS  

---

# 📈 Melhorias Futuras

- Dashboard administrativo
- Relatórios em PDF
- Sistema de pedidos avançado
- API REST
- Deploy em nuvem
- Responsividade mobile
- Integração com pagamentos
- Upload de imagens de produtos

---

# 🎥 Demonstração

O repositório contém um vídeo demonstrando o funcionamento completo do sistema:

```bash
Programa em funcionamento.mp4
```

---

# 📷 Produtos do Sistema

## 💊 Medicamentos cadastrados

<img src="images/amoxicilina.png" width="120">
<img src="images/antialergico.png" width="120">
<img src="images/aspirina.png" width="120">
<img src="images/buscopan.png" width="120">
<img src="images/dipirona.png" width="120">

<br><br>

<img src="images/dorflex.png" width="120">
<img src="images/ibuprofeno.png" width="120">
<img src="images/omeprazol.png" width="120">
<img src="images/paracetamol.png" width="120">
<img src="images/vitamina_c.png" width="120">

---

# 🎓 Projeto Acadêmico

Projeto desenvolvido para a disciplina de Engenharia de Software do curso de Ciência da Computação da Universidade Paulista — UNIP.

---

# 👩‍💻 Desenvolvedoras

- Alianny Rissato da Silva
- Giovanna Dias de Souza
