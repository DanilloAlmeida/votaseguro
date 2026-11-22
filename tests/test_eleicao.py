"""Testes das operações e regras de negócio das eleições."""

import pytest
from votaseguro.database import Database
from votaseguro.eleitor import cadastrar_eleitor
from votaseguro.eleicao import (
    cadastrar_eleicao,
    listar_eleicoes,
    obter_eleicao,
    iniciar_eleicao,
    encerrar_eleicao,
)

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

def test_iniciar_eleicao(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        # Iniciar a eleição
        conexao = db.conexao

        # Cadastrar uma eleição
        id_eleicao = cadastrar_eleicao(
                    db,
                    nome="Eleição Teste 06",
                    descricao="Descrição da eleição teste 06",
                )
        cadastrar_tres_eleitores_aptos(db)
        iniciar_eleicao(db, id_eleicao)

        # Verificar se o status foi atualizado corretamente
        eleicao = obter_eleicao(db, id_eleicao)

        assert eleicao["nome"] == "Eleição Teste 06"
        assert eleicao["descricao"] == "Descrição da eleição teste 06"
        assert eleicao["status"] == "EM_ANDAMENTO"

def test_encerrar_eleicao(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        # Cadastrar uma eleição
        id_eleicao = cadastrar_eleicao(
            db,
            nome="Eleição Teste 07",
            descricao="Descrição da eleição teste 07",
        )

        # Iniciar a eleição
        cadastrar_tres_eleitores_aptos(db)
        iniciar_eleicao(db, id_eleicao)

        # Encerrar a eleição
        encerrar_eleicao(db, id_eleicao)

        # Verificar se o status foi atualizado corretamente
        eleicao = obter_eleicao(db, id_eleicao)

        assert eleicao["nome"] == "Eleição Teste 07"
        assert eleicao["descricao"] == "Descrição da eleição teste 07"
        assert eleicao["status"] == "EM_APURACAO"

def test_nao_encerrar_eleicao_configurada(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        id_eleicao = cadastrar_eleicao(db, "Eleição A")

        with pytest.raises(ValueError):
            encerrar_eleicao(db, id_eleicao)

        eleicao = obter_eleicao(db, id_eleicao)

        # Verificar se o status da eleição permanece como "CONFIGURADA"
        assert eleicao["status"] == "CONFIGURADA"      

def test_nao_encerrar_eleicao_ja_EM_APURACAO(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        id_eleicao = cadastrar_eleicao(db, "Eleição B")

        cadastrar_tres_eleitores_aptos(db)
        iniciar_eleicao(db, id_eleicao)
        encerrar_eleicao(db, id_eleicao)

        # Tentar encerrar novamente a eleição já EM_APURACAO
        with pytest.raises(ValueError):
            encerrar_eleicao(db, id_eleicao)

        eleicao = obter_eleicao(db, id_eleicao)

        # Verificar se o status da eleição permanece como "EM_APURACAO"
        assert eleicao["status"] == "EM_APURACAO"

def test_nao_iniciar_eleicao_ja_iniciada(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        id_eleicao = cadastrar_eleicao(db, "Eleição A")

        cadastrar_tres_eleitores_aptos(db)
        iniciar_eleicao(db, id_eleicao)

        with pytest.raises(ValueError):
            iniciar_eleicao(db, id_eleicao)

        eleicao = obter_eleicao(db, id_eleicao)

        assert eleicao["status"] == "EM_ANDAMENTO"

def test_nao_iniciar_eleicao_EM_APURACAO(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        id_eleicao = cadastrar_eleicao(db, "Eleição A")

        cadastrar_tres_eleitores_aptos(db)
        iniciar_eleicao(db, id_eleicao)
        encerrar_eleicao(db, id_eleicao)

        with pytest.raises(ValueError):
            iniciar_eleicao(db, id_eleicao)

        eleicao = obter_eleicao(db, id_eleicao)

        assert eleicao["status"] == "EM_APURACAO"

def test_nao_iniciar_eleicao_com_menos_de_tres_eleitores_aptos(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        cadastrar_eleitor(db, "João Silva")
        cadastrar_eleitor(db, "Maria Souza")

        id_eleicao = cadastrar_eleicao(db, "Eleição Teste")

        with pytest.raises(ValueError) as exc_info:
            iniciar_eleicao(db, id_eleicao)

        assert str(exc_info.value) == (
            "A eleição exige pelo menos três eleitores aptos."
        )

        eleicao = obter_eleicao(db, id_eleicao)

        assert eleicao["status"] == "CONFIGURADA"

def cadastrar_tres_eleitores_aptos(db):
    """Prepara o cadastro mínimo de eleitores para iniciar uma eleição."""
    cadastrar_eleitor(db, "João Silva")
    cadastrar_eleitor(db, "Maria Souza")
    cadastrar_eleitor(db, "Pedro Santos")        

def test_nao_iniciar_eleicao_inexistente_com_menos_de_tres_eleitores(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        with pytest.raises(ValueError) as exc_info:
            iniciar_eleicao(db, 999)

        assert str(exc_info.value) == (
            "Eleição inexistente ou que não está configurada."
        )