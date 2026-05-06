# Gerenciador de Alunos com FastAPI e PostgreSQL

Projeto da Pratica 5: API CRUD estruturada em camadas, com middlewares, persistencia em PostgreSQL usando `asyncpg`, testes automatizados com `TestClient` e execucao via Docker Compose.

## Estrutura

```text
app/
├── db/
│   ├── connection.py
│   └── init.sql
├── main.py
├── middlewares/
│   ├── logging.py
│   └── custom_header.py
├── routes/
│   └── aluno_routes.py
├── services/
│   └── aluno_service.py
└── schemas/
    └── aluno.py
tests/
└── test_alunos.py
Dockerfile
docker-compose.yml
requirements.txt
pytest.ini
img/
```

## Regras Implementadas

- `POST /api/v1/alunos/`: cadastra aluno.
- `GET /api/v1/alunos/`: lista alunos.
- `GET /api/v1/alunos/{aluno_id}`: busca por ID.
- `PATCH /api/v1/alunos/{aluno_id}`: atualiza dados.
- `DELETE /api/v1/alunos/{aluno_id}`: remove aluno.
- `DELETE /api/v1/alunos/`: reseta a lista de alunos.
- Cursos suportados: `GES` e `GEC`.
- Matricula gerada automaticamente por curso.
- ID gerado como `curso + matricula`, por exemplo `GES1`, `GES2`, `GEC1`.
- IDs nao sao reutilizados apos remocao. O reset limpa a lista, mas os contadores continuam incrementando para manter essa garantia.
- Dados persistidos em PostgreSQL.

## Exemplo de Aluno

```json
{
  "id": "GES1",
  "nome": "Ana Silva",
  "email": "ana@email.com",
  "curso": "GES",
  "matricula": 1
}
```

## Execucao Local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/alunos_db
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

A API fica disponivel em `http://localhost:8000`. Para execucao local fora do Docker, mantenha um PostgreSQL rodando e crie as tabelas com `app/db/init.sql`.

## Execucao com Docker Compose

Com Compose v2:

```bash
docker compose up --build api
docker compose run tests
```

Com Compose legado:

```bash
docker-compose up --build api
docker-compose run tests
```

O Compose sobe dois servicos principais:

- `db`: banco PostgreSQL com database `alunos_db`.
- `api`: aplicacao FastAPI conectada ao banco pelo `DATABASE_URL`.

O servico `tests` executa a suite automatizada usando o mesmo banco.

## Testes

```bash
pytest -v
```

Os testes usam `fastapi.testclient.TestClient` e cobrem:

- adicao de 3 alunos por curso;
- listagem de alunos;
- busca por ID;
- atualizacao de dados;
- remocao de aluno;
- persistencia no PostgreSQL;
- reset da lista;
- validacao de curso;
- middleware de header customizado.

## Evidencias

Os prints solicitados no enunciado estão salvos na pasta `img/`:

- resultado dos testes;
- logs do container contendo as chamadas na API.
- localhost rodando

## Middlewares

- `log_requests`: registra metodo, rota, status e tempo da requisicao.
- `add_custom_header`: adiciona `X-App-Version: 1.0` em todas as respostas.
