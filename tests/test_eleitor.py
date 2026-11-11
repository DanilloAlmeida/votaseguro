import pytest

from votaseguro.database import Database
from votaseguro.eleitor import cadastrar_eleitor


def test_cadastrar_eleitor_valido(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        id_eleitor = cadastrar_eleitor(db, "João Silva")

        eleitor = db.conexao.execute(
            "SELECT * FROM eleitores WHERE id = ?",
            (id_eleitor,)
        ).fetchone()

        assert id_eleitor is not None
        assert eleitor["nome"] == "João Silva"
        assert eleitor["situacao"] == "VALIDA"

def test_cadastrar_eleitor_rejeita_nome_vazio(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError):
            cadastrar_eleitor(db, "")        