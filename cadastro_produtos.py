import sqlite3

BANCO = "produtos.db"

def criar_tabela():
    with sqlite3.connect(BANCO) as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL
            )
        """)

def cadastrar():
    nome = input("Nome do produto: ").strip()

    if not nome:
        print("O nome não pode ficar vazio.")
        return

    try:
        preco = float(input("Preço: R$ ").replace(",", "."))
        quantidade = int(input("Quantidade: "))

        if preco < 0 or quantidade < 0:
            print("Preço e quantidade não podem ser negativos.")
            return

    except ValueError:
        print("Preço ou quantidade inválidos.")
        return

    with sqlite3.connect(BANCO) as conexao:
        conexao.execute(
            "INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)",
            (nome, preco, quantidade)
        )

    print("Produto cadastrado com sucesso!")

def listar():
    with sqlite3.connect(BANCO) as conexao:
        produtos = conexao.execute(
            "SELECT * FROM produtos ORDER BY id"
        ).fetchall()

    if not produtos:
        print("Nenhum produto cadastrado.")
        return

    print("\n--- LISTA DE PRODUTOS ---")

    for produto in produtos:
        print(
            f"ID: {produto[0]} | Nome: {produto[1]} | "
            f"Preço: R$ {produto[2]:.2f} | "
            f"Quantidade: {produto[3]}"
        )

def atualizar():
    try:
        codigo = int(input("ID do produto: "))
        quantidade = int(input("Nova quantidade: "))

        if quantidade < 0:
            print("A quantidade não pode ser negativa.")
            return

    except ValueError:
        print("Digite números válidos.")
        return

    with sqlite3.connect(BANCO) as conexao:
        resultado = conexao.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?",
            (quantidade, codigo)
        )

    if resultado.rowcount:
        print("Produto atualizado!")
    else:
        print("Produto não encontrado.")

def excluir():
    try:
        codigo = int(input("ID do produto para excluir: "))
    except ValueError:
        print("ID inválido.")
        return

    with sqlite3.connect(BANCO) as conexao:
        resultado = conexao.execute(
            "DELETE FROM produtos WHERE id = ?",
            (codigo,)
        )

    if resultado.rowcount:
        print("Produto excluído!")
    else:
        print("Produto não encontrado.")


def menu():
    criar_tabela()

    while True:
        print("\n=== CADASTRO DE PRODUTOS ===")
        print("1 - Cadastrar produto")
        print("2 - Listar produtos")
        print("3 - Atualizar quantidade")
        print("4 - Excluir produto")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            listar()
        elif opcao == "3":
            atualizar()
        elif opcao == "4":
            excluir()
        elif opcao == "0":
            print("Programa encerrado!")
            break
        else:
            print("Opção inválida.")


menu()
