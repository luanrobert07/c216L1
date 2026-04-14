import os
import re
import uuid

import requests


BASE_URL = os.getenv("APP_URL", "http://localhost:5000")


def criar_aluno(nome="Luan Robert", email=None, curso="GES"):
    email = email or f"{uuid.uuid4().hex[:8]}@email.com"
    payload = {"nome": nome, "email": email, "curso": curso}
    resposta = requests.post(f"{BASE_URL}/alunos", json=payload, timeout=5)
    return resposta


def test_healthcheck_retorna_200():
    resposta = requests.get(f"{BASE_URL}/", timeout=5)

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "API de alunos em execução"}


def test_listar_alunos_retorna_uma_lista():
    resposta = requests.get(f"{BASE_URL}/alunos", timeout=5)

    assert resposta.status_code == 200
    assert isinstance(resposta.json(), list)


def test_criar_aluno_retorna_201_com_dados_normalizados():
    resposta = criar_aluno(curso="ges")

    assert resposta.status_code == 201

    aluno = resposta.json()
    assert aluno["nome"] == "Luan Robert"
    assert aluno["curso"] == "GES"
    assert re.fullmatch(r"GES\d+", aluno["matricula"])


def test_criar_aluno_valida_campos_obrigatorios():
    resposta = requests.post(
        f"{BASE_URL}/alunos",
        json={"nome": "Sem Curso"},
        timeout=5,
    )

    assert resposta.status_code == 400
    assert resposta.json()["erro"] == "Os campos nome, email e curso são obrigatórios."


def test_busca_aluno_por_matricula():
    resposta_criacao = criar_aluno()
    matricula = resposta_criacao.json()["matricula"]

    resposta = requests.get(f"{BASE_URL}/alunos/{matricula}", timeout=5)

    assert resposta.status_code == 200
    assert resposta.json()["matricula"] == matricula


def test_busca_aluno_inexistente_retorna_404():
    resposta = requests.get(f"{BASE_URL}/alunos/ALUNO99999", timeout=5)

    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "Aluno não encontrado."


def test_atualizar_aluno_altera_apenas_campos_enviados():
    resposta_criacao = criar_aluno(nome="Aluno Original", curso="GET")
    aluno = resposta_criacao.json()

    resposta = requests.put(
        f"{BASE_URL}/alunos/{aluno['matricula']}",
        json={"nome": "Aluno Atualizado"},
        timeout=5,
    )

    assert resposta.status_code == 200

    aluno_atualizado = resposta.json()
    assert aluno_atualizado["nome"] == "Aluno Atualizado"
    assert aluno_atualizado["email"] == aluno["email"]
    assert aluno_atualizado["curso"] == aluno["curso"]
    assert aluno_atualizado["matricula"] == aluno["matricula"]


def test_atualizar_aluno_inexistente_retorna_404():
    resposta = requests.put(
        f"{BASE_URL}/alunos/ALUNO99999",
        json={"nome": "Nao Existe"},
        timeout=5,
    )

    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "Aluno não encontrado."


def test_remover_aluno_retorna_200_e_remove_registro():
    resposta_criacao = criar_aluno(curso="GEC")
    matricula = resposta_criacao.json()["matricula"]

    resposta_remocao = requests.delete(f"{BASE_URL}/alunos/{matricula}", timeout=5)
    resposta_busca = requests.get(f"{BASE_URL}/alunos/{matricula}", timeout=5)

    assert resposta_remocao.status_code == 200
    assert resposta_remocao.json()["mensagem"] == "Aluno removido com sucesso."
    assert resposta_busca.status_code == 404


def test_remover_aluno_inexistente_retorna_404():
    resposta = requests.delete(f"{BASE_URL}/alunos/ALUNO99999", timeout=5)

    assert resposta.status_code == 404
    assert resposta.json()["erro"] == "Aluno não encontrado."
