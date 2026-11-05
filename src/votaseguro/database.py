"""Conexão com o banco SQLite e criação das tabelas do sistema."""

import sqlite3
from pathlib import Path


class Database:
    """Gerencia a conexão SQLite usada pelo VotaSeguro."""

    def __init__(self, caminho: str | Path = "votaseguro.db") -> None:
        self.caminho = Path(caminho)
        self.conexao: sqlite3.Connection | None = None

    def conectar(self) -> sqlite3.Connection:
        """Abre a conexão e garante que a tabela de eleições exista."""
        if self.conexao is None:
            self.conexao = sqlite3.connect(self.caminho)
            self.conexao.row_factory = sqlite3.Row
            self.criar_tabela_eleicoes()
        return self.conexao

    def criar_tabela_eleicoes(self) -> None:
        """Cria a tabela eleicoes caso ela ainda não exista."""
        conexao = self.conexao
        if conexao is None:
            raise RuntimeError("Abra a conexão antes de criar as tabelas.")

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS eleicoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
                    CHECK (length(trim(nome)) > 0),
                descricao TEXT,
                data_inicio TEXT,
                data_fim TEXT,
                status TEXT NOT NULL DEFAULT 'CONFIGURADA'
                    CHECK (
                        status IN (
                            'CONFIGURADA',
                            'EM_ANDAMENTO',
                            'ENCERRADA'
                        )
                    ),
                criada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                atualizada_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CHECK (
                    data_inicio IS NULL
                    OR data_fim IS NULL
                    OR data_fim > data_inicio
                )
            )
            """
        )
        conexao.commit()

    def fechar(self) -> None:
        """Fecha a conexão, se estiver aberta."""
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None

    def __enter__(self) -> "Database":
        self.conectar()
        return self

    def __exit__(self, *_: object) -> None:
        self.fechar()
