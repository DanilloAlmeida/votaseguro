"""Operações de negócio relacionadas às eleições."""

from votaseguro.eleitor import contar_eleitores_aptos

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


def iniciar_eleicao(db, id_eleicao):
    """Inicia uma eleição, alterando seu status para 'EM_ANDAMENTO'."""

    eleicao = obter_eleicao(db, id_eleicao)

    if eleicao is None or eleicao["status"] != "CONFIGURADA":
        raise ValueError(
            "Eleição inexistente ou que não está configurada."
        )

    quantidade_eleitores = contar_eleitores_aptos(db)

    if quantidade_eleitores < 3:
        raise ValueError(
            "A eleição exige pelo menos três eleitores aptos."
        )

    conexao = db.conexao

    conexao.execute(
        """
        UPDATE eleicoes
        SET status = 'EM_ANDAMENTO'
        WHERE id = ?
        """,
        (id_eleicao,)
    )

    conexao.commit()
    

def encerrar_eleicao(db, id_eleicao):
    """Encerra uma eleição que esteja em andamento."""

    conexao = db.conexao

    cursor = conexao.execute(
        """
        UPDATE eleicoes
        SET status = 'EM_APURACAO',
            atualizada_em = CURRENT_TIMESTAMP
        WHERE id = ?
        AND status = 'EM_ANDAMENTO'
        """,
        (id_eleicao,),
    )

    if cursor.rowcount == 0:
        raise ValueError(
            "Eleição inexistente ou que não está em andamento."
        )

    conexao.commit()  