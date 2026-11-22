import pytest

from votaseguro.database import Database
from votaseguro.eleitor import (
    cadastrar_eleitor,
    contar_eleitores_aptos,
)

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
        assert eleitor["situacao"] == "APTO"

def test_cadastrar_eleitor_rejeita_nome_vazio(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError):
            cadastrar_eleitor(db, "")

def test_cadastrar_eleitor_rejeita_nome_com_apenas_espacos(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError):
            cadastrar_eleitor(db, "   ")

@pytest.mark.parametrize("nome", ["João  Silva", "João   Silva", "João    Silva"])

def test_cadastrar_eleitor_rejeita_nome_com_espacos_excessivos(tmp_path, nome):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError):
            cadastrar_eleitor(db, nome)

def test_contar_eleitores_aptos(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        cadastrar_eleitor(db, "João Silva")
        cadastrar_eleitor(db, "Maria Souza")
        cadastrar_eleitor(db, "Pedro Santos")

        quantidade = contar_eleitores_aptos(db)

        assert quantidade == 3