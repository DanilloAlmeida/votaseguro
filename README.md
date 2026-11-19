# VotaSeguro

**Sistema Didático de Votação Eletrônica com Mecanismos Criptográficos**





## 1. Sobre o projeto

O VotaSeguro é um projeto acadêmico desenvolvido no contexto da disciplina **Segurança Computacional**, da Universidade de Brasília (UnB).

O objetivo é projetar e implementar um sistema didático de votação eletrônica que utilize mecanismos criptográficos para proteger os votos, verificar a integridade dos registros e permitir a auditoria independente dos resultados.

O desenvolvimento será realizado de forma incremental, priorizando a compreensão dos mecanismos implementados, a clareza da arquitetura e a existência de testes que permitam verificar o comportamento do sistema.

A aplicação utilizará uma interface de linha de comando (CLI), Python como linguagem principal e SQLite para persistência dos dados.

## 2. Objetivos

O projeto tem os seguintes objetivos:

- Implementar a cifragem de votos utilizando ElGamal exponencial.
- Realizar a apuração homomórfica dos votos, sem decifrar individualmente cada cédula.
- Distribuir o poder de decifração entre autoridades eleitorais.
- Utilizar assinaturas digitais para autenticação e verificação das cédulas.
- Manter um quadro público de registros encadeados por funções hash.
- Impedir votos duplicados e verificar a elegibilidade dos eleitores.
- Desenvolver um programa auditor independente do servidor de votação.
- Documentar as decisões técnicas, os testes realizados e as limitações da solução.

O desenvolvimento seguirá as orientações e os requisitos estabelecidos pelo professor na especificação do Trabalho Final.

## 3. Escopo e limitações

O VotaSeguro tem finalidade exclusivamente acadêmica e didática.

O projeto busca demonstrar a aplicação prática de conceitos de criptografia e segurança computacional em um sistema de votação.

A implementação não deve ser considerada adequada para eleições reais. A segurança de um sistema eleitoral depende de propriedades, mecanismos e processos adicionais que vão além da implementação isolada de algoritmos criptográficos.

Os requisitos serão desenvolvidos progressivamente. A documentação distinguirá funcionalidades planejadas, implementadas, testadas e ainda pendentes.

## 4. Tecnologias

| Tecnologia     | Finalidade                                               |
| -------------- | -------------------------------------------------------- |
| Python         | Linguagem principal                                      |
| SQLite         | Persistência e consulta dos dados                        |
| `hashlib`      | Funções hash                                             |
| `secrets`      | Geração de valores aleatórios criptograficamente seguros |
| `sqlite3`      | Acesso ao banco de dados SQLite                          |
| `cryptography` | Operações de assinatura digital RSA, conforme necessário |
| `unittest`     | Testes automatizados                                     |
| Git            | Controle de versão                                       |
| GitHub         | Hospedagem do repositório e colaboração                  |

A implementação do ElGamal exponencial e da apuração homomórfica será desenvolvida no próprio projeto, utilizando primitivas matemáticas básicas do Python.

Não serão utilizadas bibliotecas prontas que implementem o protocolo completo de votação ou a cifragem homomórfica exigida pelo trabalho.

As dependências externas serão mantidas sob controle e documentadas.

## 5. Visão geral da aplicação

A aplicação será organizada em torno do ciclo de vida de uma eleição.

O menu principal deverá permitir:

1. Gerenciar eleições.
2. Cadastrar eleitores.
3. Cadastrar autoridades eleitorais.
4. Consultar o quadro público.
5. Acessar a auditoria de eleições.
6. Encerrar a aplicação.

O gerenciamento de uma eleição permitirá configurar os candidatos, preparar os participantes e controlar o início e o encerramento da votação.

Durante a votação, o sistema permitirá registrar cédulas, respeitando as regras de elegibilidade e unicidade.

Após o encerramento, será possível realizar a apuração com a participação das autoridades e disponibilizar os dados públicos necessários à auditoria.

A organização definitiva dos menus e dos componentes será documentada em `docs/ESPECIFICACAO_DO_MVP.md`.

## 6. Arquitetura prevista

A aplicação será organizada em componentes com responsabilidades bem definidas.

| Componente                | Responsabilidade                                                  |
| ------------------------- | ----------------------------------------------------------------- |
| Interface CLI             | Receber comandos e apresentar informações ao usuário              |
| Gerenciamento de eleições | Controlar a configuração e o estado de cada eleição               |
| Cadastro de eleitores     | Manter os participantes autorizados e suas chaves públicas        |
| Cédulas                   | Representar os votos e seus registros criptográficos              |
| Módulo criptográfico      | Implementar o ElGamal exponencial e a apuração homomórfica        |
| Autoridades eleitorais    | Participar da geração da chave conjunta e da apuração             |
| Quadro público            | Manter os registros das cédulas e o encadeamento por hashes       |
| Banco de dados            | Persistir os dados estruturados de cada eleição                   |
| Auditor independente      | Verificar os dados públicos sem depender da confiança no servidor |

Essa arquitetura é uma proposta inicial e poderá ser refinada durante o desenvolvimento.

O banco SQLite será utilizado para persistência e consultas. Os dados públicos necessários à auditoria poderão ser exportados em formatos documentados, permitindo verificar uma eleição independentemente do servidor de votação.

A persistência local, por si só, não garante a integridade dos dados. Essa propriedade dependerá dos mecanismos criptográficos e dos procedimentos de verificação implementados.

## 7. Plano de desenvolvimento

O projeto será desenvolvido em fases progressivas, cada uma com objetivos e critérios de conclusão verificáveis.

### Fase 0 — Planejamento e ambiente

- [ ] Criar o repositório.
- [ ] Documentar o escopo inicial.
- [ ] Preparar o ambiente Python.
- [ ] Definir a estrutura do projeto.
- [ ] Estabelecer as primeiras convenções de desenvolvimento.

### Fase 1 — Fluxo básico de votação

- [ ] Criar a interface de linha de comando.
- [ ] Configurar eleições e candidatos.
- [ ] Cadastrar eleitores e autoridades.
- [ ] Implementar o ciclo de vida da eleição.
- [ ] Registrar votos e impedir duplicidades.
- [ ] Persistir os dados no SQLite.

Esta fase utilizará inicialmente uma lógica simplificada, sem alegar que o sistema já oferece as garantias criptográficas exigidas.

### Fase 2 — ElGamal exponencial e apuração homomórfica

- [ ] Implementar a cifragem de votos binários.
- [ ] Implementar a multiplicação de cifras.
- [ ] Validar a apuração de totais.
- [ ] Criar testes automatizados para os cálculos.
- [ ] Utilizar parâmetros criptográficos adequados na versão de segurança.

### Fase 3 — Autoridades eleitorais

- [ ] Implementar a geração da chave conjunta.
- [ ] Implementar a participação das autoridades na apuração.
- [ ] Verificar o comportamento diante da ausência de uma autoridade.
- [ ] Testar a recuperação do resultado agregado.

### Fase 4 — Autenticação e quadro público

- [ ] Implementar assinaturas digitais RSA.
- [ ] Verificar as assinaturas das cédulas.
- [ ] Implementar a verificação de elegibilidade e unicidade.
- [ ] Criar recibos assinados.
- [ ] Implementar o quadro público encadeado por hashes.
- [ ] Testar a detecção de adulterações.

### Fase 5 — Auditor independente

- [ ] Implementar a verificação da cadeia de hashes.
- [ ] Verificar assinaturas e elegibilidade.
- [ ] Detectar votos duplicados.
- [ ] Verificar a consistência da apuração homomórfica.
- [ ] Exportar os dados públicos de uma eleição.
- [ ] Executar a auditoria sem depender do servidor de votação.

### Fase 6 — Validação e entrega acadêmica

- [ ] Revisar os testes automatizados.
- [ ] Preparar instruções de instalação e execução.
- [ ] Documentar a arquitetura e o modelo de ameaças.
- [ ] Registrar as limitações de segurança.
- [ ] Preparar o relatório técnico.
- [ ] Preparar o roteiro de demonstração.
- [ ] Validar o pacote final de entrega.

As fases poderão ser ajustadas conforme os resultados obtidos e o tempo disponível.

## 8. Ambiente de desenvolvimento

O Ubuntu será o ambiente principal de desenvolvimento.

Entretanto, o projeto buscará compatibilidade com Windows e macOS, evitando dependências específicas de um único sistema operacional.

Use Python 3 e um ambiente virtual para manter as dependências do projeto isoladas das bibliotecas do sistema.

No Ubuntu, instale o suporte a ambientes virtuais (caso ainda não esteja instalado):

```bash
sudo apt update
sudo apt install python3-venv
```

Na pasta do projeto, crie e ative o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

O ambiente virtual precisa ser ativado novamente em cada novo terminal. Não é necessário recriá-lo nem reinstalar as dependências. Para sair do ambiente, use `deactivate`.

## 9. Testes e validação

Os testes podem ser executados com o `unittest`, incluído na biblioteca padrão do Python:

```bash
python -m unittest discover -s tests
```

Também é possível executá-los com `pytest`. Com o ambiente virtual ativado, instale-o uma vez:

```bash
python -m pip install pytest
```

Depois, execute:

```bash
python -m pytest
```

Cada componente deverá possuir testes que verifiquem seu comportamento.

Os testes deverão abranger tanto os casos válidos quanto as tentativas de executar operações proibidas.

Entre os cenários previstos estão:

- Registro de uma cédula válida.
- Rejeição de um segundo voto do mesmo eleitor.
- Rejeição de uma cédula com assinatura inválida.
- Detecção de adulteração no quadro público.
- Apuração sem a participação de todas as autoridades.
- Verificação independente dos dados públicos.
- Recuperação correta dos totais da eleição.

A existência de testes bem-sucedidos não será interpretada, isoladamente, como prova de segurança do sistema.

## 10. Colaboração

O desenvolvimento começará individualmente, com a possibilidade de incorporar colaboradores posteriormente.

Para facilitar a participação de outros desenvolvedores:

- As funcionalidades serão divididas em componentes.
- As decisões técnicas serão documentadas.
- Os testes automatizados acompanharão a implementação.
- As alterações serão registradas por meio de commits claros.
- As novas funcionalidades deverão respeitar a arquitetura e os requisitos documentados.

Antes de contribuir, recomenda-se consultar a especificação do MVP e o plano de desenvolvimento.

## 11. Segurança e uso de inteligência artificial

Este é um projeto acadêmico cujo objetivo inclui a compreensão dos mecanismos implementados.

O código e a documentação deverão ser compreendidos pelos responsáveis pelo trabalho, que precisam conseguir explicar as decisões técnicas, os algoritmos e os resultados dos testes.

As ferramentas de inteligência artificial poderão ser utilizadas como apoio ao estudo, à análise e à revisão, respeitando as condições estabelecidas pelo professor para o Trabalho Final.

## 12. Entrega acadêmica

A entrega oficial será realizada pela plataforma Aprender3, conforme as instruções da disciplina.

O repositório GitHub será utilizado para o desenvolvimento e o controle de versão. O pacote de entrega deverá conter os arquivos necessários à execução, os testes, a documentação e o relatório técnico exigido.

Antes da entrega, o pacote será extraído em um ambiente separado e testado para verificar se as instruções de execução são suficientes.

## 13. Referências

- Especificação do Trabalho Final da disciplina Segurança Computacional — UnB, semestre 2026/2.
- Stallings, William. *Criptografia e Segurança de Redes: Princípios e Práticas*.
- Kurose, James F.; Ross, Keith W. *Redes de Computadores e a Internet*.
- Materiais e anotações de aula da disciplina.

---

**Status do projeto:** planejamento e definição do escopo.

**Próximo objetivo:** criar o ambiente inicial, documentar a especificação do MVP e estabelecer os primeiros testes automatizados.
