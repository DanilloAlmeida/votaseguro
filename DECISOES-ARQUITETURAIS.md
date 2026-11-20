# VotaSeguro — Registro de Decisões Arquiteturais

**Projeto:** VotaSeguro — Sistema Didático de Votação Eletrônica  
**Disciplina:** Segurança Computacional — UnB  
**Tecnologias:** Python e SQLite  
**Documento:** Decisões Arquiteturais  
**Versão:** 01  
**Data:** 10/11/2026

---

## 1. Objetivo

Este documento registra as principais decisões arquiteturais tomadas durante o desenvolvimento do VotaSeguro, apresentando seus respectivos contextos, justificativas e consequências.

O objetivo é manter um histórico das escolhas técnicas realizadas, facilitar a compreensão da arquitetura e garantir que todos os integrantes do grupo conheçam e consigam justificar as decisões adotadas.

As decisões deverão ser revisadas sempre que houver mudanças significativas nos requisitos ou na arquitetura do sistema.

---

## 2. Decisões arquiteturais

### DA-001 — Utilização de Python e SQLite

**Status:** Aceita.

**Contexto:**

O projeto necessita de uma implementação didática, com estrutura simples, de fácil execução e compatível com diferentes sistemas operacionais.

**Decisão:**

Utilizar Python como linguagem de programação e SQLite como sistema gerenciador de banco de dados.

**Justificativa:**

A combinação permite desenvolver uma aplicação leve, sem necessidade de instalar ou administrar um servidor de banco de dados, facilitando a execução em Windows, Linux e macOS.

---

### DA-002 — Separação entre regras de negócio e persistência de dados

**Status:** Aceita.

**Contexto:**

O sistema precisa manter suas regras de negócio organizadas, evitando que diferentes interfaces ou componentes implementem as mesmas regras de maneira independente.

**Decisão:**

Centralizar as regras de negócio em módulos Python, mantendo o SQLite responsável pela persistência e pela integridade estrutural dos dados.

**Justificativa:**

Essa abordagem favorece a separação de responsabilidades, reduz a duplicidade de código e facilita futuras alterações na aplicação.

Também permite que diferentes interfaces, como CLI e uma eventual aplicação Web, utilizem a mesma camada de negócio.

**Consequências:**

- As interfaces deverão utilizar as operações disponibilizadas pela camada de negócio.
- As regras de negócio não deverão ser reproduzidas individualmente em cada interface.
- O banco de dados continuará aplicando restrições estruturais necessárias à integridade dos registros.

---

### DA-003 — Identificação dos eleitores por ID interno

**Status:** Aceita.

**Contexto:**

O sistema necessita identificar individualmente os eleitores, sem depender de documentos pessoais reais.

**Decisão:**

Utilizar o campo `id`, gerado automaticamente pelo SQLite, como identificador único do eleitor.

Não serão utilizados CPF, número de título eleitoral ou outros documentos pessoais reais.

**Justificativa:**

A utilização de um identificador interno atende às necessidades didáticas do projeto, reduz a coleta de dados pessoais e simplifica o modelo de dados.

---

### DA-004 — Situação inicial dos eleitores

**Status:** Aceita.

**Contexto:**

O sistema precisa controlar a habilitação dos eleitores para participar das eleições.

**Decisão:**

Todo eleitor cadastrado deverá receber inicialmente a situação `VALIDA`.

A definição dessa situação será responsabilidade da operação de cadastro implementada na camada de negócio Python.

A alteração posterior da situação deverá ocorrer por meio de uma operação específica.

**Justificativa:**

A regra de inicialização da situação representa uma decisão de negócio e, portanto, deverá ser centralizada no código da aplicação.

Essa abordagem evita distribuir a mesma regra entre diferentes componentes.

---

### DA-005 — Responsabilidades do SQLite na validação dos dados

**Status:** Aceita.

**Contexto:**

É necessário definir quais validações devem ser realizadas pela aplicação e quais devem ser garantidas pelo banco de dados.

**Decisão:**

O SQLite deverá ser responsável pelas restrições de integridade estrutural, enquanto as regras de domínio serão centralizadas na camada de negócio Python.

**Justificativa:**

Essa divisão procura evitar a duplicação de regras de negócio em diferentes camadas, mantendo o banco responsável pela consistência estrutural dos dados.

**Consequências:**

As alterações nas regras de domínio deverão ser realizadas prioritariamente na camada de negócio, sem necessidade de modificar restrições do banco que apenas reproduzam essas regras.

---

### DA-006 — Cadastro único de eleitores e controle de participação por eleição

**Status:** Aceita como diretriz de modelagem.

**Contexto:**

Um mesmo eleitor poderá participar de diferentes eleições, mas não poderá votar mais de uma vez na mesma eleição.

**Decisão:**

Manter o cadastro geral do eleitor independente das eleições.

O controle de participação e de realização do voto será associado individualmente a cada eleição.

**Justificativa:**

Essa estrutura evita a duplicação dos dados cadastrais e permite controlar separadamente a participação do eleitor em diferentes eleições.

**Consequências:**

A modelagem deverá contemplar uma estrutura de relacionamento entre eleitores e eleições, permitindo registrar se determinado eleitor já votou em determinada eleição.

### DA-007 — Validação do nome do eleitor

**Contexto:**

Evitar inconsistências nos dados cadastrais causadas por espaços
inseridos acidentalmente durante a digitação do nome.

**Decisão:**

Rejeitar nomes vazios, com espaços em branco nas extremidades
ou com dois ou mais espaços consecutivos entre as partes do nome.
O sistema não realizará correções automáticas.

**Justificativa:**

Evitar que diferenças acidentais na digitação produzam cadastros
inconsistentes e dificultem a localização de eleitores.

**Consequências:**

O usuário deverá corrigir a entrada e informar novamente o nome.
A validação será realizada pela camada de negócio.

---

## 3. Modelo inicial da entidade Eleitor

Com base nas decisões anteriores, a entidade `eleitores` deverá contemplar inicialmente os seguintes campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador único gerado pelo SQLite |
| `nome` | Nome do eleitor |
| `situacao` | Situação atual do eleitor |
| `criado_em` | Data e hora do cadastro |

A estrutura definitiva será implementada e validada durante o desenvolvimento do módulo de eleitores.

---

## 4. Registro de novas decisões

As novas decisões deverão seguir o seguinte padrão:

- **Identificador:** DA-NNN.
- **Título:** descrição objetiva da decisão.
- **Status:** proposta, aceita, rejeitada ou substituída.
- **Contexto:** problema ou necessidade que motivou a decisão.
- **Decisão:** escolha realizada.
- **Justificativa:** razões que fundamentam a escolha.
- **Consequências:** impactos técnicos e operacionais da decisão.

Decisões substituídas deverão permanecer registradas, preservando o histórico arquitetural do projeto.

---

**Observação:** este documento deverá evoluir junto com o VotaSeguro. As decisões registradas representam o entendimento atual da equipe e poderão ser revistas mediante justificativa.