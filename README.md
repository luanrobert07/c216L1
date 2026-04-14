# CRUD de Alunos com API HTTP

## Descrição

Este projeto implementa um CRUD de alunos exposto por API HTTP com Flask.

Cada aluno possui:

- `nome`
- `email`
- `curso`
- `matricula`

A matrícula é gerada automaticamente por curso no formato `CURSO + sequencial`, como `GES1`, `GES2` e `GEC1`.

## Endpoints

### `GET /`

Healthcheck da aplicação.

### `GET /alunos`

Lista todos os alunos cadastrados.

### `POST /alunos`

Cria um novo aluno.

Exemplo de payload:

```json
{
  "nome": "Luan Robert",
  "email": "luan@email.com",
  "curso": "GES"
}
```

### `GET /alunos/<matricula>`

Busca um aluno por matrícula.

### `PUT /alunos/<matricula>`

Atualiza nome, email e/ou curso de um aluno existente.

### `DELETE /alunos/<matricula>`

Remove um aluno.

## Middleware

A aplicação possui um middleware em [crud_alunos.py](/home/luan/Documentos/Projetos/Inatel/c216/crud_alunos.py:1) usando `before_request` e `after_request` para registrar:

- método HTTP
- rota acessada
- status da resposta
- tempo de processamento

Exemplo de log:

```text
[middleware] GET /alunos status=200 tempo=0.0004s
```

## Execução Local

Criar e ativar o ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Subir a API:

```bash
python crud_alunos.py
```

## Execução com Docker Compose

Subir a API:

```bash
docker compose up --build api
```

Executar os testes:

```bash
docker compose up --build testes
```

## Testes de API

Os testes automatizados estão em [tests/test_api.py](/home/luan/Documentos/Projetos/Inatel/c216/tests/test_api.py:1) e cobrem:

- `GET /`
- `GET /alunos`
- `POST /alunos` com sucesso
- `POST /alunos` com erro de validação
- `GET /alunos/<matricula>` com sucesso
- `GET /alunos/<matricula>` com `404`
- `PUT /alunos/<matricula>` com sucesso
- `PUT /alunos/<matricula>` com `404`
- `DELETE /alunos/<matricula>` com sucesso
- `DELETE /alunos/<matricula>` com `404`

Para rodar localmente:

```bash
source .venv/bin/activate
pytest -v tests/test_api.py
```

## Gerando Logs de Evidência

Para gerar os logs de build, testes e execução da API:

```bash
docker rm -f api-alunos-e2e
docker build -t api-alunos-local . > evidencias/build.log 2>&1
docker run -d --name api-alunos-e2e -p 5001:5000 api-alunos-local
docker run --rm --add-host host.docker.internal:host-gateway -e APP_URL=http://host.docker.internal:5001 api-alunos-local pytest -v tests/test_api.py > evidencias/testes_api.log 2>&1
docker logs api-alunos-e2e > evidencias/api_execucao.log 2>&1
echo "\nPortas publicadas:" >> evidencias/api_execucao.log
docker inspect --format '{{json .NetworkSettings.Ports}}' api-alunos-e2e >> evidencias/api_execucao.log
```

Arquivos gerados:

- `evidencias/build.log`
- `evidencias/testes_api.log`
- `evidencias/api_execucao.log`

## Estrutura

- [crud_alunos.py](/home/luan/Documentos/Projetos/Inatel/c216/crud_alunos.py:1): API Flask com CRUD e middleware
- [Dockerfile](/home/luan/Documentos/Projetos/Inatel/c216/Dockerfile:1): imagem da aplicação
- [docker-compose.yml](/home/luan/Documentos/Projetos/Inatel/c216/docker-compose.yml:1): orquestração da API e dos testes
- [tests/test_api.py](/home/luan/Documentos/Projetos/Inatel/c216/tests/test_api.py:1): testes automatizados da API
- [requirements.txt](/home/luan/Documentos/Projetos/Inatel/c216/requirements.txt:1): dependências do projeto
- [evidencias](/home/luan/Documentos/Projetos/Inatel/c216/evidencias): logs de build, execução e testes
