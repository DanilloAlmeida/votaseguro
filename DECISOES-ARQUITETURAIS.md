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

**Status:** Substituída pela DA-008.

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

**Status:** Substituída pela DA-008.

**Contexto:**

Um mesmo eleitor poderá participar de diferentes eleições, mas não poderá votar mais de uma vez na mesma eleição.

**Decisão:**

Manter o cadastro geral do eleitor independente das eleições.

O controle de participação e de realização do voto será associado individualmente a cada eleição.

**Justificativa:**

Essa estrutura evita a duplicação dos dados cadastrais e permite controlar separadamente a participação do eleitor em diferentes eleições.

**Consequências:**

A modelagem deverá contemplar uma estrutura de relacionamento entre eleitores e eleições, permitindo registrar se determinado eleitor já votou em determinada eleição.

---

### DA-007 — Validação do nome do eleitor

**Status:** Aceita.

**Contexto:**

Evitar inconsistências nos dados cadastrais causadas por espaços inseridos acidentalmente durante a digitação do nome.

**Decisão:**

Rejeitar nomes vazios, com espaços em branco nas extremidades ou com dois ou mais espaços consecutivos entre as partes do nome.

O sistema não realizará correções automáticas.

**Justificativa:**

Evitar que diferenças acidentais na digitação produzam cadastros inconsistentes e dificultem a localização de eleitores.

**Consequências:**

O usuário deverá corrigir a entrada e informar novamente o nome.

A validação será realizada pela camada de negócio.

---

### DA-008 — Cadastro global e situação dos eleitores

**Status:** Aceita.

**Contexto:**

O sistema precisa controlar a elegibilidade dos eleitores sem criar associações individuais de participação entre eleitores e eleições.

Um mesmo eleitor poderá participar de diferentes eleições, mas não poderá votar mais de uma vez na mesma eleição.

**Decisão:**

Manter um cadastro global e único de eleitores, independente das eleições.

Todo eleitor cadastrado receberá inicialmente a situação `APTO`.

A situação poderá assumir os seguintes valores:

- `APTO`: eleitor autorizado a participar das eleições.
- `INAPTO`: eleitor impedido de participar das eleições.

Somente o administrador poderá alterar a situação de um eleitor.

Todo eleitor com situação `APTO` estará automaticamente habilitado a participar de qualquer eleição em andamento, desde que possua seu par de chaves cadastrado antes do início da votação.

Não haverá associação individual prévia entre eleitores e eleições para definir a participação.

A unicidade do voto será controlada individualmente por eleição, utilizando a combinação do identificador do eleitor e do identificador da eleição.

**Justificativa:**

A manutenção de um cadastro global simplifica o modelo de dados, evita duplicação de informações e centraliza o controle da elegibilidade.

O controle de unicidade por eleição permite que um mesmo eleitor participe de diferentes eleições, sem possibilidade de votar mais de uma vez na mesma eleição.

**Consequências:**

- A situação inicial dos eleitores será definida pela camada de negócio Python.
- O cadastro não dependerá de uma tabela de associação entre eleitores e eleições.
- A estrutura de votos deverá garantir a unicidade da combinação entre eleitor e eleição.
- A situação global do eleitor será utilizada para determinar sua elegibilidade nas eleições que forem iniciadas.
- Os eleitores deverão possuir suas chaves cadastradas antes do início da votação.

---

### DA-009 — Congelamento do cadastro de eleitores durante eleições em andamento

**Status:** Aceita.

**Contexto:**

O sistema precisa preservar a estabilidade do cadastro de eleitores e das condições de elegibilidade durante a votação.

Alterações cadastrais durante uma eleição poderiam modificar o conjunto de eleitores habilitados e comprometer a consistência do processo eleitoral.

**Decisão:**

Enquanto existir pelo menos uma eleição com situação `EM_ANDAMENTO`, o cadastro geral de eleitores permanecerá congelado.

Durante esse período, serão proibidas as seguintes operações:

- Inclusão de novos eleitores.
- Exclusão de eleitores.
- Alteração da situação de eleitores entre `APTO` e `INAPTO`.

As operações de consulta ao cadastro continuarão permitidas.

O cadastro será liberado novamente quando não existir nenhuma eleição em situação `EM_ANDAMENTO`.

**Justificativa:**

O congelamento preserva o conjunto de eleitores habilitados durante a votação, impedindo alterações que possam interferir na elegibilidade e na contagem de votos.

**Consequências:**

- A abertura de uma eleição deverá considerar os eleitores aptos existentes no momento de seu início.
- A quantidade de eleitores aptos permanecerá estável durante a votação.
- O encerramento antecipado poderá ocorrer quando todos os eleitores aptos tiverem votado.
- Se houver mais de uma eleição em andamento, o cadastro permanecerá congelado até que todas sejam encerradas.

---

## 3. Modelo inicial da entidade Eleitor

Com base nas decisões anteriores, a entidade `eleitores` deverá contemplar inicialmente os seguintes campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador único gerado pelo SQLite |
| `nome` | Nome do eleitor |
| `situacao` | Situação global do eleitor: `APTO` ou `INAPTO` |
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