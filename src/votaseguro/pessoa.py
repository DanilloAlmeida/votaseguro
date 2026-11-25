
"""Operações de negócio relacionadas às pessoas."""


def cadastrar_pessoa(db, nome):
    """Cadastra uma pessoa e retorna seu identificador."""

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
        INSERT INTO pessoas (nome, papel, situacao)
        VALUES (?, ?, ?)
        """,
        (nome, "ELEITOR", "APTO"),
    )

    conexao.commit()

    return cursor.lastrowid

def contar_pessoas_aptas(db):
    """Retorna a quantidade de pessoas aptas a votar."""

    conexao = db.conexao

    cursor = conexao.execute(
        """
        SELECT COUNT(*)
        FROM pessoas
        WHERE papel = ?
        AND situacao = ?
        """,
        ("ELEITOR", "APTO"),
    )

    return cursor.fetchone()[0]