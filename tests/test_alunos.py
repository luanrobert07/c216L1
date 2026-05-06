import anyio
from fastapi.testclient import TestClient

from app.db.connection import get_connection
from app.main import app

client = TestClient(app)


def resetar():
    client.delete("/api/v1/alunos/")


def criar_aluno(nome="Aluno Teste", email="aluno@email.com", curso="GES"):
    return client.post(
        "/api/v1/alunos/",
        json={"nome": nome, "email": email, "curso": curso},
    )


async def buscar_aluno_no_banco(aluno_id: str):
    conn = await get_connection()
    try:
        row = await conn.fetchrow("SELECT * FROM alunos WHERE id=$1", aluno_id)
        return dict(row) if row else None
    finally:
        await conn.close()


def test_root_retorna_api_funcionando():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"mensagem": "API funcionando"}
    assert response.headers["X-App-Version"] == "1.0"


def test_adiciona_tres_alunos_por_curso():
    resetar()

    alunos_ges = [
        criar_aluno(f"Aluno GES {i}", f"ges{i}@email.com", "GES").json()
        for i in range(1, 4)
    ]
    alunos_gec = [
        criar_aluno(f"Aluno GEC {i}", f"gec{i}@email.com", "GEC").json()
        for i in range(1, 4)
    ]

    matriculas_ges = [aluno["matricula"] for aluno in alunos_ges]
    matriculas_gec = [aluno["matricula"] for aluno in alunos_gec]

    assert [aluno["id"] for aluno in alunos_ges] == [
        f"GES{matricula}" for matricula in matriculas_ges
    ]
    assert [aluno["id"] for aluno in alunos_gec] == [
        f"GEC{matricula}" for matricula in matriculas_gec
    ]
    assert matriculas_ges == list(range(matriculas_ges[0], matriculas_ges[0] + 3))
    assert matriculas_gec == list(range(matriculas_gec[0], matriculas_gec[0] + 3))


def test_listar_alunos():
    resetar()
    criar_aluno("Ana", "ana@email.com", "GES")
    criar_aluno("Bia", "bia@email.com", "GEC")

    response = client.get("/api/v1/alunos/")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_buscar_aluno_por_id():
    resetar()
    aluno = criar_aluno("Carlos", "carlos@email.com", "GES").json()

    response = client.get(f"/api/v1/alunos/{aluno['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == aluno["id"]


def test_atualizar_dados_de_aluno():
    resetar()
    aluno = criar_aluno("Dani", "dani@email.com", "GEC").json()

    response = client.patch(
        f"/api/v1/alunos/{aluno['id']}",
        json={"nome": "Daniele", "email": "daniele@email.com"},
    )

    assert response.status_code == 200
    assert response.json()["nome"] == "Daniele"
    assert response.json()["email"] == "daniele@email.com"
    assert response.json()["id"] == aluno["id"]
    assert response.json()["curso"] == "GEC"


def test_atualizar_curso_gera_novo_id_coerente():
    resetar()
    aluno = criar_aluno("Curso", "curso@email.com", "GES").json()

    response = client.patch(f"/api/v1/alunos/{aluno['id']}", json={"curso": "GEC"})

    assert response.status_code == 200
    assert response.json()["curso"] == "GEC"
    assert response.json()["id"].startswith("GEC")
    assert response.json()["id"] != aluno["id"]
    assert client.get(f"/api/v1/alunos/{aluno['id']}").status_code == 404


def test_remover_aluno():
    resetar()
    aluno = criar_aluno("Edu", "edu@email.com", "GES").json()

    response = client.delete(f"/api/v1/alunos/{aluno['id']}")
    busca = client.get(f"/api/v1/alunos/{aluno['id']}")

    assert response.status_code == 200
    assert response.json() == {"mensagem": "Aluno removido com sucesso"}
    assert busca.status_code == 404


def test_persistencia_no_postgresql():
    resetar()
    aluno = criar_aluno("Persistente", "persistente@email.com", "GES").json()

    aluno_no_banco = anyio.run(buscar_aluno_no_banco, aluno["id"])

    assert aluno_no_banco is not None
    assert aluno_no_banco["id"] == aluno["id"]
    assert aluno_no_banco["nome"] == "Persistente"
    assert aluno_no_banco["email"] == "persistente@email.com"
    assert aluno_no_banco["curso"] == "GES"


def test_resetar_lista_de_alunos():
    resetar()
    criar_aluno("Fabio", "fabio@email.com", "GES")
    criar_aluno("Gabi", "gabi@email.com", "GEC")

    response = client.delete("/api/v1/alunos/")
    lista = client.get("/api/v1/alunos/")

    assert response.status_code == 200
    assert lista.json() == []


def test_id_nao_e_reutilizado_apos_delete():
    resetar()
    aluno_removido = criar_aluno("Helena", "helena@email.com", "GES").json()

    client.delete(f"/api/v1/alunos/{aluno_removido['id']}")
    novo_aluno = criar_aluno("Igor", "igor@email.com", "GES").json()

    assert novo_aluno["id"] != aluno_removido["id"]
    assert int(novo_aluno["id"].replace("GES", "")) > int(
        aluno_removido["id"].replace("GES", "")
    )


def test_validar_curso_obrigatorio_e_existente():
    response = client.post(
        "/api/v1/alunos/",
        json={"nome": "Curso Errado", "email": "curso@email.com", "curso": "ADM"},
    )

    assert response.status_code == 422
