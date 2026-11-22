"""Operações de negócio relacionadas aos eleitores."""

def cadastrar_eleitor(db, nome):
    """Cadastra um eleitor e retorna seu identificador."""

    nome_vazio = not nome
    espacos_nas_extremidades = nome != nome.strip()
    espacos_consecutivos = "  " in nome

    if nome_vazio or espacos_nas_extremidades or espacos_consecutivos:
        raise ValueError(
            "O nome não pode ser vazio, começar ou terminar com espaços "
            "nem conter espaços consecutivos."
        )

    conexao = db.conexao

    cursor = conexao.execute(
        """
        INSERT INTO eleitores (nome, situacao)
        VALUES (?, ?)
        """,
        (nome, "APTO")
    )

    conexao.commit()

    return cursor.lastrowid

def contar_eleitores_aptos(db):
    """Retorna a quantidade de eleitores aptos."""

    conexao = db.conexao

    cursor = conexao.execute(
        """
        SELECT COUNT(*)
        FROM eleitores
        WHERE situacao = ?
        """,
        ("APTO",)
    )

    return cursor.fetchone()[0]