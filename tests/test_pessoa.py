
import pytest

from votaseguro.database import Database
from votaseguro.pessoa import (
    cadastrar_pessoa,
    contar_pessoas_aptas
)


def test_cadastrar_pessoa_valida(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        pessoa_id = cadastrar_pessoa(db, "João da Silva")

        conexao = db.conexao
        pessoa = conexao.execute(
            """
            SELECT id, nome, papel, situacao
            FROM pessoas
            WHERE id = ?
            """,
            (pessoa_id,),
        ).fetchone()

        assert pessoa is not None
        assert pessoa["nome"] == "João da Silva"
        assert pessoa["papel"] == "ELEITOR"
        assert pessoa["situacao"] == "APTO"


def test_cadastrar_pessoa_rejeita_nome_vazio(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError):
            cadastrar_pessoa(db, "")


def test_cadastrar_pessoa_rejeita_espacos_excessivos(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError):
            cadastrar_pessoa(db, "João  Silva")


def test_contar_pessoas_aptas(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        cadastrar_pessoa(db, "João Silva")
        cadastrar_pessoa(db, "Maria Souza")
        cadastrar_pessoa(db, "Pedro Santos")

        quantidade = contar_pessoas_aptas(db)

        assert quantidade == 3
