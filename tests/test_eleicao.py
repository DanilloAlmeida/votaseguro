"""Testes das operações e regras de negócio das eleições."""

import pytest
from votaseguro.database import Database
from votaseguro.eleicao import cadastrar_eleicao,listar_eleicoes, obter_eleicao

def test_cadastrar_eleicao_valida(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        id_eleicao = cadastrar_eleicao(
            db,
            nome="Eleição Teste 01",
            descricao="Descrição da eleição teste 01",
        )
        assert id_eleicao is not None

        conexao = db.conexao
        assert conexao is not None

        eleicao = conexao.execute(
            "SELECT * FROM eleicoes WHERE id = ?", (id_eleicao,)
        ).fetchone()

        assert eleicao is not None
        assert eleicao["nome"] == "Eleição Teste 01"
        assert eleicao["descricao"] == "Descrição da eleição teste 01"
        assert eleicao["status"] == "CONFIGURADA"

def test_rejeitar_nome_vazio_ou_com_espacos(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError, match="nome"):
            cadastrar_eleicao(
                db,
                nome="   ",
            )

def test_listar_eleicoes(tmp_path):                
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        # Cadastrar algumas eleições
        cadastrar_eleicao(db, nome="Eleição Teste 02")
        cadastrar_eleicao(db, nome="Eleição Teste 03")
        cadastrar_eleicao(db, nome="Eleição Teste 04")

        # Listar todas as eleições
        eleicoes = listar_eleicoes(db)
        assert len(eleicoes) == 3
        assert eleicoes[0]["nome"] == "Eleição Teste 02"
        assert eleicoes[1]["nome"] == "Eleição Teste 03"
        assert eleicoes[2]["nome"] == "Eleição Teste 04"

def test_obter_eleicao_por_id(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        # Cadastrar uma eleição
        id_eleicao = cadastrar_eleicao(db, nome="Eleição Teste 05")

        # Obter a eleição pelo ID
        eleicao = obter_eleicao(db, id_eleicao)
        assert eleicao is not None
        assert eleicao["id"] == id_eleicao
        assert eleicao["nome"] == "Eleição Teste 05"
        