'''
Responsabilidade:  Verificar a persistência dos dados
'''

import sqlite3

from votaseguro.database import Database


def test_criar_tabela_eleicoes(tmp_path):
    caminho_banco = tmp_path / "teste.db"

    with Database(caminho_banco) as db:
        conexao = db.conexao
        assert conexao is not None

        tabela = conexao.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND name = 'eleicoes'
            """
        ).fetchone()

        assert tabela is not None

        colunas = conexao.execute(
            "PRAGMA table_info(eleicoes)"
        ).fetchall()

        nomes_colunas = [coluna["name"] for coluna in colunas]

        assert "id" in nomes_colunas
        assert "nome" in nomes_colunas
        assert "status" in nomes_colunas
        assert "criada_em" in nomes_colunas
        assert "atualizada_em" in nomes_colunas

import sqlite3

import pytest

from votaseguro.database import Database

def test_rejeita_nome_vazio(tmp_path):
    with Database(tmp_path / "teste.db") as db:
        conexao = db.conexao
        assert conexao is not None

        with pytest.raises(sqlite3.IntegrityError):
            conexao.execute(
                "INSERT INTO eleicoes (nome) VALUES (?)",
                ("   ",),
            )


def test_rejeita_status_invalido(tmp_path):
    with Database(tmp_path / "teste.db") as db:
        conexao = db.conexao
        assert conexao is not None

        with pytest.raises(sqlite3.IntegrityError):
            conexao.execute(
                "INSERT INTO eleicoes (nome, status) VALUES (?, ?)",
                ("Eleição de teste", "CANCELADA"),
            )


def test_rejeita_data_final_anterior_ao_inicio(tmp_path):
    with Database(tmp_path / "teste.db") as db:
        conexao = db.conexao
        assert conexao is not None

        with pytest.raises(sqlite3.IntegrityError):
            conexao.execute(
                """
                INSERT INTO eleicoes (nome, data_inicio, data_fim)
                VALUES (?, ?, ?)
                """,
                (
                    "Eleição de teste",
                    "2026-11-10T10:00:00",
                    "2026-11-09T10:00:00",
                ),
            )

def test_criar_tabela_pessoas(tmp_path):
    caminho_db = tmp_path / "teste.db"

    with Database(caminho_db) as db:
        cursor = db.conexao.execute(
            """
            PRAGMA table_info(pessoas)
            """
        )

        colunas = {
            linha["name"]
            for linha in cursor.fetchall()
        }

        assert colunas == {
            "id",
            "nome",
            "papel",
            "situacao",
            "criado_em",
        }
