"""Operações de negócio relacionadas às eleições."""

def cadastrar_eleicao(
    db,
    nome,
    descricao=None,
    data_inicio=None,
    data_fim=None,):

    """Cadastra uma eleição e retorna seu identificador."""

    if not nome or not nome.strip():
        raise ValueError("O nome da eleição não pode ser vazio ou apenas espaços em branco.")

    conexao = db.conexao

    cursor = conexao.execute(
        """
        INSERT INTO eleicoes (
            nome,
            descricao,
            data_inicio,
            data_fim
        )
        VALUES (?, ?, ?, ?)
        """,
        (nome, descricao, data_inicio, data_fim),
    )

    conexao.commit()

    return cursor.lastrowid

def listar_eleicoes(db):
    """Retorna uma lista de todas as eleições cadastradas."""
    conexao = db.conexao
    cursor = conexao.execute("SELECT * FROM eleicoes ORDER BY id")
    return cursor.fetchall()

def obter_eleicao(db, id_eleicao):
    """Retorna os detalhes de uma eleição específica pelo seu ID."""
    conexao = db.conexao
    cursor = conexao.execute(
        "SELECT * FROM eleicoes WHERE id = ?", (id_eleicao,)
    )
    return cursor.fetchone()