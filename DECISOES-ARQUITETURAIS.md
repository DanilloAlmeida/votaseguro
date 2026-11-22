from pathlib import Path

content = r"""# VotaSeguro — Registro de Decisões Arquiteturais

**Projeto:** VotaSeguro — Sistema Didático de Votação Eletrônica  
**Disciplina:** Segurança Computacional — UnB  
**Tecnologias:** Python e SQLite  
**Documento:** Decisões Arquiteturais  
**Versão:** 02  
**Data:** 22/11/2026

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

### DA-003 — Identificação das pessoas por ID interno

**Status:** Aceita.

**Contexto:**

O sistema necessita identificar individualmente as pessoas cadastradas, sem depender de documentos pessoais reais.

**Decisão:**

Utilizar o campo `id`, gerado automaticamente pelo SQLite, como identificador único de cada pessoa.

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

### DA-006 — Cadastro único e controle de participação por eleição

**Status:** Substituída parcialmente pela DA-008 e complementada pelas DA-010 e DA-011.

**Contexto:**

Uma mesma pessoa poderá participar de diferentes eleições, mas não poderá votar mais de uma vez na mesma eleição.

**Decisão:**

Manter um cadastro geral e único de pessoas, independente das eleições.

O controle de participação e de realização do voto será associado individualmente a cada eleição.

**Justificativa:**

Essa estrutura evita a duplicação dos dados cadastrais e permite controlar separadamente a participação da pessoa em diferentes eleições.

**Consequências:**

A estrutura de votos deverá garantir a unicidade da combinação entre o identificador da pessoa e o identificador da eleição.

---

### DA-007 — Validação do nome da pessoa

**Status:** Aceita.

**Contexto:**

Evitar inconsistências nos dados cadastrais causadas por espaços inseridos acidentalmente durante a digitação do nome.

**Decisão:**

Rejeitar nomes vazios, com espaços em branco nas extremidades ou com dois ou mais espaços consecutivos entre as partes do nome.

O sistema não realizará correções automáticas.

**Justificativa:**

Evitar que diferenças acidentais na digitação produzam cadastros inconsistentes e dificultem a localização de pessoas.

**Consequências:**

O usuário deverá corrigir a entrada e informar novamente o nome.

A validação será realizada pela camada de negócio.

---

### DA-008 — Cadastro global e situação eleitoral

**Status:** Aceita, complementada pelas DA-010 e DA-012.

**Contexto:**

O sistema precisa controlar a elegibilidade das pessoas sem criar associações individuais prévias entre pessoas e eleições para definir quem poderá votar.

Uma mesma pessoa poderá participar de diferentes eleições, mas não poderá votar mais de uma vez na mesma eleição.

**Decisão:**

Manter um cadastro global e único de pessoas, independente das eleições.

Toda pessoa cadastrada receberá inicialmente a situação `APTO`.

A situação poderá assumir os seguintes valores:

- `APTO`: pessoa habilitada a votar e, observadas as demais regras, a candidatar-se ou exercer a administração do sistema.
- `INAPTO`: pessoa impedida de votar, candidatar-se ou exercer a administração do sistema.

A situação eleitoral será independente do papel atual da pessoa, mas a condição `INAPTO` impedirá o exercício de qualquer papel além da manutenção do cadastro para consulta e preservação histórica.

A unicidade do voto será controlada individualmente por eleição, utilizando a combinação do identificador da pessoa e do identificador da eleição.

**Justificativa:**

A manutenção de um cadastro global simplifica o modelo de dados, evita duplicação de informações e centraliza o controle da elegibilidade.

O controle de unicidade por eleição permite que uma mesma pessoa participe de diferentes eleições, sem possibilidade de votar mais de uma vez na mesma eleição.

**Consequências:**

- A situação inicial será definida pela camada de negócio Python.
- O cadastro não dependerá de uma tabela de associação prévia entre pessoas e eleições para determinar a elegibilidade.
- A estrutura de votos deverá garantir a unicidade da combinação entre pessoa e eleição.
- Somente pessoas `APTO` poderão votar.
- As pessoas deverão possuir suas chaves cadastradas antes do início da votação, conforme os requisitos do projeto.

---

### DA-009 — Congelamento do cadastro durante eleições em andamento

**Status:** Aceita, ampliada pela DA-012.

**Contexto:**

O sistema precisa preservar a estabilidade do cadastro de pessoas e das condições de elegibilidade durante a votação.

Alterações cadastrais durante uma eleição poderiam modificar o conjunto de pessoas habilitadas e comprometer a consistência do processo eleitoral.

**Decisão:**

Enquanto existir pelo menos uma eleição com situação `EM_ANDAMENTO`, o cadastro global de pessoas permanecerá congelado.

Durante esse período, serão proibidas as seguintes operações:

- Inclusão de novas pessoas.
- Exclusão de pessoas.
- Alteração da situação eleitoral entre `APTO` e `INAPTO`.
- Alteração do papel entre `ELEITOR` e `ADMINISTRADOR`.
- Qualquer outra operação que modifique os dados cadastrais ou a elegibilidade das pessoas.

As operações de consulta ao cadastro continuarão permitidas.

O cadastro será liberado novamente quando não existir nenhuma eleição em situação `EM_ANDAMENTO`.

**Justificativa:**

O congelamento preserva o conjunto de pessoas habilitadas durante a votação, impedindo alterações que possam interferir na elegibilidade e na contagem de votos.

**Consequências:**

- A abertura de uma eleição deverá considerar as pessoas aptas existentes no momento de seu início.
- A quantidade de pessoas aptas permanecerá estável durante a votação.
- O encerramento antecipado poderá ocorrer quando todas as pessoas aptas tiverem votado.
- Se houver mais de uma eleição em andamento, o cadastro permanecerá congelado até que todas sejam encerradas.
- A regra deverá ser aplicada na camada de negócio a todas as operações de alteração cadastral, e não apenas à interface CLI.

---

### DA-010 — Cadastro único de pessoas e separação entre papel e candidatura

**Status:** Aceita.

**Contexto:**

O sistema precisa cadastrar pessoas que poderão atuar como eleitoras ou administradoras e também registrar candidaturas. Manter cadastros independentes para cada uma dessas condições provocaria duplicação de informações pessoais.

Também é necessário permitir que uma pessoa candidata continue exercendo seu direito de voto, desde que esteja apta.

**Decisão:**

Manter uma única entidade de cadastro, denominada `pessoas`.

Cada pessoa terá um papel cadastral, que poderá assumir os seguintes valores:

- `ELEITOR`: papel atribuído automaticamente no cadastro.
- `ADMINISTRADOR`: papel atribuído por uma operação autorizada de promoção.

A condição de candidato não será armazenada como um papel permanente da pessoa. Uma candidatura será registrada em uma estrutura própria, associando a pessoa à eleição específica.

Toda pessoa será cadastrada inicialmente com:

- `papel = ELEITOR`;
- `situacao = APTO`.

Uma pessoa poderá ser candidata em uma eleição e continuar sendo eleitora, podendo votar se estiver `APTO`.

**Justificativa:**

A separação entre o cadastro da pessoa e sua candidatura evita duplicação de dados e representa corretamente o fato de que uma candidatura pertence a uma eleição específica.

A separação entre papel e situação eleitoral também evita confundir autorização administrativa com habilitação para votar.

**Consequências:**

- Os dados pessoais serão mantidos em um único cadastro.
- A tabela de candidaturas deverá relacionar uma pessoa a uma eleição.
- A candidatura não deverá substituir o papel `ELEITOR` da pessoa.
- O modelo permitirá que uma pessoa participe como candidata em eleições diferentes, respeitadas as regras de elegibilidade e de incompatibilidade de papéis.
- A pessoa candidata poderá votar uma única vez em cada eleição em que estiver habilitada.

---

### DA-011 — Regras de elegibilidade e incompatibilidade entre administração e candidatura

**Status:** Aceita.

**Contexto:**

O sistema precisa impedir que pessoas sem habilitação eleitoral exerçam funções no processo e evitar que uma mesma pessoa seja administradora e candidata simultaneamente.

**Decisão:**

Somente pessoas com situação `APTO` poderão:

- Registrar voto.
- Ser cadastradas como candidatas.
- Exercer o papel de `ADMINISTRADOR`.

Uma pessoa não poderá ser simultaneamente `ADMINISTRADOR` e candidata.

Para que uma pessoa administradora possa se candidatar, deverá primeiro deixar o papel de `ADMINISTRADOR` e retornar ao papel `ELEITOR`.

Uma pessoa com situação `INAPTO` não poderá ser candidata nem administradora.

Quando uma pessoa que esteja como `ADMINISTRADOR` passar para `INAPTO`, seu papel será alterado automaticamente para `ELEITOR`, mantendo-se sua situação como `INAPTO`.

A alteração não excluirá o cadastro da pessoa nem seus registros históricos.

**Justificativa:**

A regra mantém a coerência entre habilitação eleitoral e participação nas funções do sistema, além de impedir o acúmulo das condições de administrador e candidato.

**Consequências:**

- A camada de negócio deverá validar a situação eleitoral antes de permitir voto, candidatura ou promoção a administrador.
- A camada de negócio deverá impedir a candidatura de uma pessoa que ainda esteja como administradora.
- A alteração para `INAPTO` deverá retirar as permissões administrativas, retornando o papel cadastral para `ELEITOR`.
- Os registros históricos de candidaturas serão preservados. A consequência operacional de uma inaptidão sobre uma candidatura já registrada deverá ser tratada sem apagar seu histórico.
- As alterações cadastrais deverão respeitar o congelamento definido na DA-009 e na DA-012.

---

### DA-012 — Congelamento de todas as alterações no cadastro de pessoas

**Status:** Aceita. Complementa e detalha a DA-009.

**Contexto:**

O modelo de cadastro passou a contemplar, além da situação eleitoral, o papel da pessoa e os vínculos de candidatura. É necessário garantir que nenhuma alteração nesses dados modifique as condições de participação durante uma eleição em andamento.

**Decisão:**

Enquanto existir pelo menos uma eleição em situação `EM_ANDAMENTO`, nenhuma alteração no cadastro global de pessoas poderá ser realizada.

Isso inclui:

- Cadastrar ou excluir pessoas.
- Alterar a situação eleitoral.
- Alterar o papel cadastral.
- Promover ou retirar uma pessoa do papel de administrador.
- Realizar operações que alterem a elegibilidade de uma pessoa.

As consultas continuarão permitidas.

O congelamento será encerrado somente quando não existir nenhuma eleição em andamento.

**Justificativa:**

A regra preserva a estabilidade do cadastro global e evita que mudanças de papel ou situação interfiram na votação.

**Consequências:**

- A verificação deverá considerar todas as eleições, e não apenas uma eleição específica.
- Se duas ou mais eleições estiverem em andamento, o cadastro continuará congelado até que todas deixem esse estado.
- A validação deverá estar centralizada na camada de negócio, de modo que qualquer interface utilize a mesma regra.

---

### DA-013 — Histórico de alterações de papel e situação eleitoral

**Status:** Aceita.

**Contexto:**

O sistema precisa preservar a rastreabilidade das mudanças realizadas no cadastro das pessoas, permitindo identificar o que foi alterado, quando ocorreu e quem foi responsável pela operação.

O cadastro principal deverá apresentar os valores atuais, enquanto os eventos anteriores deverão permanecer disponíveis para auditoria.

**Decisão:**

Manter registros históricos das alterações de papel e de situação eleitoral, sem sobrescrever ou excluir eventos anteriores.

O histórico de alterações de papel deverá registrar, no mínimo:

- Identificador da pessoa.
- Papel anterior.
- Papel novo.
- Data e hora da alteração.
- Identificador do responsável pela operação.
- Motivo da alteração.

O histórico de alterações de situação eleitoral deverá registrar, no mínimo:

- Identificador da pessoa.
- Situação anterior.
- Situação nova.
- Data e hora da alteração.
- Identificador do responsável pela operação.
- Motivo da alteração.

Quando uma pessoa `ADMINISTRADOR` passar para `INAPTO`, a operação deverá atualizar seu papel para `ELEITOR` e registrar a mudança de papel no histórico, além de registrar a alteração da situação eleitoral.

A atualização do cadastro e a gravação dos respectivos eventos históricos deverão ocorrer na mesma transação do banco de dados.

**Justificativa:**

O histórico permite reconstruir as alterações cadastrais e fornece rastreabilidade para auditorias. A separação dos históricos de papel e de situação mantém distintos dois conceitos de negócio.

**Consequências:**

- O cadastro principal armazenará apenas os valores atuais de papel e situação.
- Os históricos serão estruturas próprias, com registros preservados.
- Uma alteração cadastral não deverá ser considerada concluída se o respectivo registro histórico não puder ser gravado.
- As operações deverão identificar o responsável pela alteração.
- O motivo deverá ser informado e armazenado para permitir a compreensão posterior da operação.
- A modelagem e as permissões específicas de consulta aos históricos serão detalhadas durante a implementação.

---

## 3. Modelo inicial da entidade Pessoa

Com base nas decisões anteriores, a entidade `pessoas` deverá contemplar inicialmente os seguintes campos:

| Campo | Descrição |
|---|---|
| `id` | Identificador único gerado pelo SQLite |
| `nome` | Nome da pessoa |
| `papel` | Papel cadastral atual: `ELEITOR` ou `ADMINISTRADOR` |
| `situacao` | Situação eleitoral: `APTO` ou `INAPTO` |
| `criado_em` | Data e hora do cadastro |

Toda pessoa deverá ser cadastrada inicialmente com `papel = ELEITOR` e `situacao = APTO`.

A candidatura será representada separadamente, por meio de uma estrutura que relacione a pessoa à eleição correspondente.

Os históricos de papel e de situação eleitoral também serão mantidos em estruturas próprias.

A estrutura definitiva será implementada e validada durante o desenvolvimento dos módulos correspondentes.

---

## 4. Registro de novas decisões

As novas decisões deverão seguir o seguinte padrão:

- **Identificador:** DA-NNN.
- **Título:** descrição objetiva da decisão.
- **Status:** proposta, aceita, rejeitada ou substituída.
- **Contexto:** problema ou necessidade que motivou a decisão.
- **Decisão:** escolha realizada.
- **Justificativa:** razões que fundamentam a escolha.
- **Consequências:** impactos técnicos e operacionais da escolha.

Decisões substituídas deverão permanecer registradas, preservando o histórico arquitetural do projeto.

---

**Observação:** este documento deverá evoluir junto com o VotaSeguro. As decisões registradas representam o entendimento atual da equipe e poderão ser revistas mediante justificativa.
"""

path = Path("/mnt/data/DECISOES-ARQUITETURAIS-v02.md")
path.write_text(content, encoding="utf-8")
print(f"Arquivo criado: {path}")
print(f"Total de linhas: {len(content.splitlines())}")
