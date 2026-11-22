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
            self.criar_tabela_eleitores()
            self.criar_tabela_pessoas()
        return self.conexao

    def criar_tabela_eleicoes(self) -> None:
        """Abre a conexão e garante que as tabelas do sistema existam."""
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
                            'EM_APURACAO',
                            'APURADA'
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

    def criar_tabela_eleitores(self) -> None:        
        """Cria a tabela eleitores caso ela ainda não exista."""
        conexao = self.conexao
        if conexao is None:
            raise RuntimeError("Abra a conexão antes de criar as tabelas.")
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS eleitores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL CHECK (length(trim(nome)) > 0),
                situacao TEXT NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conexao.commit()

    def criar_tabela_pessoas(self) -> None:
        """Cria a tabela pessoas caso ela ainda não exista."""
        conexao = self.conexao

        if conexao is None:
            raise RuntimeError("Abra a conexão antes de criar as tabelas.")

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS pessoas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL
                    CHECK (length(trim(nome)) > 0),
                papel TEXT NOT NULL,
                situacao TEXT NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
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
