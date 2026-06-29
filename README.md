# Raízes do Nordeste - API (Back-end)

Este projeto é a API para a rede de lanchonetes Raízes do Nordeste, desenvolvida para a Trilha: Back-end Rede "Raízes do Nordeste", um Projeto Multidisciplinar.

## 🛠️ Requisitos
* Python 3.x
* Banco de Dados SQLite (ou o que você estiver usando)
* Bibliotecas listadas em `requirements.txt` (FastAPI, Uvicorn, SQLAlchemy, etc.)

## ⚙️ Como configurar variáveis de ambiente
1. Crie um arquivo `.env` na raiz do projeto baseando-se no arquivo `.env.example`.
2. Configure as variáveis necessárias (ex: `SECRET_KEY`, `DATABASE_URL`).

## 📦 Como instalar as dependências
Abra o terminal e execute o comando:
`pip install -r requirements.txt`

## 🗄️ Como criar o banco e executar migrations (e seed)
(Explique brevemente como o seu banco é criado. Ex: "Ao iniciar a API, o SQLAlchemy cria automaticamente as tabelas no arquivo banco.db").

## 🚀 Como iniciar a API
Execute o comando abaixo no terminal:
`uvicorn main:app --reload`

## 📖 Como acessar a documentação (Swagger/OpenAPI)
Com a API rodando, acesse no seu navegador:
* URL do Swagger: `http://127.0.0.1:8000/docs`

## 🧪 Como rodar os testes
Os testes foram documentados e exportados via Insomnia.
1. Baixe o arquivo `Testes_Raizes_do_Nordeste.json` que está na raiz deste repositório.
2. Abra o Insomnia, vá em "Import/Export" e importe o arquivo.
3. Garanta que a API está rodando localmente.
4. Execute as requisições (certifique-se de rodar primeiro o teste "T02 - Login Válido" para gerar o Token de acesso).