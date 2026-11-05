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