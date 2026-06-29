# Raízes do Nordeste — API Back-end

API REST desenvolvida para a rede de lanchonetes **Raízes do Nordeste**, como parte do Projeto Multidisciplinar — Trilha: Back-end (2026).

Repositório: [https://github.com/buttercupcloud/projeto-backend-raizes-nordeste](https://github.com/buttercupcloud/projeto-backend-raizes-nordeste)

---

## Contexto do Projeto

A Raízes do Nordeste é uma rede de lanchonetes em expansão que atende clientes por múltiplos canais (App, Totem, Balcão, Pick-up e Web). Esta API implementa o back-end central do sistema, cobrindo o fluxo crítico de **Pedido → Pagamento Mock → Atualização de Status**, com autenticação JWT, controle de perfis (roles), e conformidade com a LGPD.

---

## Arquitetura do Projeto (Camadas)

O projeto segue uma separação em camadas inspirada em Clean Architecture:

```
projeto_raizes/
├── domain/           # Entidades (modelos ORM) e schemas Pydantic
│   ├── models.py     # 12 tabelas: Usuario, Pedido, Produto, Estoque, Pagamento...
│   └── schemas.py    # Contratos de request/response (Pydantic)
├── infrastructure/   # Configuração do banco de dados (SQLAlchemy + MySQL)
│   └── database.py
├── application/      # (Reservado para serviços/casos de uso futuros)
├── api/              # Rotas/Controllers (FastAPI Routers)
│   ├── auth.py       # Autenticação JWT e controle de acesso por perfil
│   ├── usuarios.py   # Cadastro de usuários
│   ├── pedidos.py    # Criação e gestão de pedidos
│   └── pagamentos.py # Simulação de pagamento (mock)
├── main.py           # Ponto de entrada da aplicação
├── .env.example      # Modelo das variáveis de ambiente
├── requirements.txt  # Dependências do projeto
└── TESTES_raizes_do_nordeste.json  # Coleção Insomnia com todos os testes
```

---

## Requisitos

| Item | Versão |
|---|---|
| Python | 3.10 ou superior |
| MySQL | 8.0 ou superior |
| pip | Incluído com o Python |

---

## Como Configurar as Variáveis de Ambiente

1. Na raiz do projeto, crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

2. Edite o `.env` com suas configurações:

```env
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=mysql+pymysql://root:sua_senha@localhost:3306/raizes_db
```

> **Atenção:** o arquivo `.env` nunca deve ser enviado ao repositório (já está no `.gitignore`).

---

## Como Instalar as Dependências

Com o ambiente virtual ativo (recomendado), execute:

```bash
# Criar e ativar ambiente virtual (opcional mas recomendado)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

---

## Como Criar o Banco de Dados

1. Acesse o MySQL e crie o banco:

```sql
CREATE DATABASE raizes_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. As **tabelas são criadas automaticamente** pelo SQLAlchemy ao iniciar a API (linha `Base.metadata.create_all` em `main.py`). Não há arquivo de migration separado.

3. **Seed manual (dados iniciais para testes):** execute os seguintes comandos no MySQL Workbench ou via terminal após iniciar a API uma vez:

```sql
-- Inserir uma unidade
INSERT INTO unidade (nome, cidade, estado, ativa) VALUES ('Unidade Recife Centro', 'Recife', 'PE', 1);

-- Inserir produtos
INSERT INTO produto (nome, descricao, preco, categoria, ativo)
VALUES ('Cuscuz Recheado', 'Cuscuz com queijo e manteiga de garrafa', 15.90, 'Salgado', 1);

INSERT INTO produto (nome, descricao, preco, categoria, ativo)
VALUES ('Tapioca Nordestina', 'Tapioca com coco e manteiga', 12.50, 'Salgado', 1);

-- Inserir um usuário CLIENTE (senha: 123456 — armazenada como bcrypt hash)
INSERT INTO usuario (nome, cpf, senha_hash, perfil_role, consentimento, saldo_pontos)
VALUES ('Maria Silva', '12345678901',
'$2b$12$KIX9kL2z6lO8K1v2B3q4sO7J5m9p1N4v6R8u0T2w4Y6a8C0e2G4i6', 'CLIENTE', 1, 0);

-- Inserir um usuário GERENTE
INSERT INTO usuario (nome, cpf, senha_hash, perfil_role, consentimento, saldo_pontos)
VALUES ('João Gerente', '98765432100',
'$2b$12$KIX9kL2z6lO8K1v2B3q4sO7J5m9p1N4v6R8u0T2w4Y6a8C0e2G4i6', 'GERENTE', 1, 0);
```

> **Importante:** para gerar hashes bcrypt reais, use o endpoint `POST /usuarios` da própria API, que aplica o hash automaticamente.

---

## Como Iniciar a API

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

---

## Como Acessar a Documentação (Swagger / OpenAPI)

Com a API rodando, acesse no navegador:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`
- **JSON do schema:** `http://127.0.0.1:8000/openapi.json`

O Swagger é gerado automaticamente pelo FastAPI e reflete todos os endpoints implementados, com exemplos de request/response.

---

## Endpoints Implementados

| Método | Rota | Descrição | Auth |
|---|---|---|---|
| `POST` | `/usuarios` | Cadastrar novo usuário | Público |
| `POST` | `/auth/login` | Login — retorna token JWT | Público |
| `GET` | `/admin/relatorios` | Acesso restrito a gerentes | JWT (GERENTE/ADMIN) |
| `POST` | `/pedidos` | Criar pedido com itens | Público* |
| `POST` | `/pagamentos/mock` | Processar pagamento simulado | Público* |

> *Autenticação JWT implementada no módulo `/auth`. Os endpoints de pedidos e pagamentos validam regras de negócio e status do pedido.

### Campo `canalPedido` (Multicanalidade — Requisito Obrigatório)

Todo pedido exige o campo `canalPedido`, registrando a origem do atendimento:

```json
{
  "id_usuario": 1,
  "id_unidade": 1,
  "canalPedido": "APP",
  "itens": [
    { "id_produto": 1, "quantidade": 2 }
  ]
}
```

Valores válidos: `APP` | `TOTEM` | `BALCAO` | `PICKUP` | `WEB`

---

## Como Rodar os Testes (Coleção Insomnia)

O arquivo `TESTES_raizes_do_nordeste.json` na raiz do repositório contém todos os cenários de teste organizados.

### Passo a passo:

1. Abra o **Insomnia** (ou Postman — o arquivo é compatível)
2. Vá em **Application → Import Data → From File**
3. Importe o arquivo `TESTES_raizes_do_nordeste.json`
4. Garanta que a API está rodando em `http://127.0.0.1:8000`
5. **Execute na ordem abaixo:**

| Ordem | ID | Teste | Por quê esta ordem? |
|---|---|---|---|
| 1 | T01 | Cadastrar usuário | Cria o usuário necessário para o login |
| 2 | T02 | Login válido | Gera o `accessToken` usado nos testes seguintes |
| 3 | T03 | Acesso sem token (401) | Valida bloqueio sem autenticação |
| 4 | T04 | Acesso com perfil sem permissão (403) | Valida controle de roles |
| 5 | T05 | Criar pedido válido | Fluxo principal — pedido com canal APP |
| 6 | T06 | Criar pedido — produto inexistente (404) | Teste negativo de validação |
| 7 | T07 | Criar pedido — canal inválido (400) | Teste negativo de multicanalidade |
| 8 | T08 | Processar pagamento mock (aprovado) | Pagamento e atualização de status |
| 9 | T09 | Pagamento em pedido já pago (400) | Regra de negócio — idempotência |
| 10 | T10 | Pagamento — pedido inexistente (404) | Teste negativo de validação |

> **Atenção:** copie o `accessToken` retornado no T02 e cole no header `Authorization: Bearer <token>` dos testes que exigem autenticação (T03, T04 e `/admin/relatorios`).

---

## Segurança e LGPD

| Controle | Implementação |
|---|---|
| Hash de senha | `bcrypt` via `passlib` — nunca armazenado em texto plano |
| Autenticação | JWT (HS256) com expiração de 2 horas |
| Autorização por perfis | Roles: `CLIENTE`, `GERENTE`, `ADMIN` — verificadas no token |
| Consentimento LGPD | Campo `consentimento` (boolean) obrigatório no cadastro |
| Dados sensíveis | Senha nunca exposta em responses; apenas hash armazenado |
| Log de auditoria | Tabela `log_auditoria` modelada para rastrear ações sensíveis |
| Dados pessoais coletados | `nome`, `cpf` — finalidade: identificação e autenticação |

---

## Fluxo Crítico Implementado

```
[Cliente] → POST /usuarios → Cadastro com hash de senha
     ↓
POST /auth/login → Token JWT com role do usuário
     ↓
POST /pedidos → Validação de canal, produto e cálculo do total → Status: RECEBIDO
     ↓
POST /pagamentos/mock → Registro do pagamento → Status do pedido: EM_PREPARO
```

---

## Tecnologias Utilizadas

| Tecnologia | Finalidade |
|---|---|
| Python 3.x | Linguagem principal |
| FastAPI | Framework web / API REST |
| SQLAlchemy | ORM / mapeamento objeto-relacional |
| MySQL | Banco de dados relacional |
| PyMySQL | Driver de conexão Python → MySQL |
| Pydantic | Validação de schemas de request/response |
| Passlib + bcrypt | Hash seguro de senhas |
| PyJWT | Geração e validação de tokens JWT |
| Uvicorn | Servidor ASGI para execução da API |
