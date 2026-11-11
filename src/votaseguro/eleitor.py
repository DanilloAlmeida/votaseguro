"""Operações de negócio relacionadas aos eleitores."""

def cadastrar_eleitor(db, nome):
    """Cadastra um eleitor e retorna seu identificador."""

    if not nome or not nome.strip():
        raise ValueError("O nome do eleitor não pode ser vazio.")

    conexao = db.conexao

    cursor = conexao.execute(
        """
        INSERT INTO eleitores (nome, situacao)
        VALUES (?, ?)
        """,
        (nome, "VALIDA")
    )

    conexao.commit()

    return cursor.lastrowid