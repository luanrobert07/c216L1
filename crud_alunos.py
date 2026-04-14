import time

from flask import Flask, g, jsonify, request

app = Flask(__name__)

alunos = {}
contadores_curso = {}

def gerar_matricula(curso):
    curso = curso.upper()
    contadores_curso[curso] = contadores_curso.get(curso, 0) + 1
    return f"{curso}{contadores_curso[curso]}"

def normalizar_dados_aluno(dados, obrigatorio=False):
    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    curso = dados.get("curso", "").strip().upper()

    if obrigatorio and (not nome or not email or not curso):
        return None, "Os campos nome, email e curso são obrigatórios."

    return {"nome": nome, "email": email, "curso": curso}, None

def resetar_dados():
    alunos.clear()
    contadores_curso.clear()


@app.before_request
def iniciar_requisicao():
    g.inicio_requisicao = time.perf_counter()


@app.after_request
def registrar_resposta(response):
    inicio = getattr(g, "inicio_requisicao", time.perf_counter())
    duracao = time.perf_counter() - inicio
    print(
        f"[middleware] {request.method} {request.path} "
        f"status={response.status_code} tempo={duracao:.4f}s"
    )
    return response


@app.get("/")
def healthcheck():
    return jsonify({"mensagem": "API de alunos em execução"}), 200

@app.get("/alunos")
def listar_alunos():
    return jsonify(list(alunos.values())), 200

@app.post("/alunos")
def cadastrar_aluno():
    dados = request.get_json(silent=True) or {}
    aluno, erro = normalizar_dados_aluno(dados, obrigatorio=True)

    if erro:
        return jsonify({"erro": erro}), 400

    matricula = gerar_matricula(aluno["curso"])
    novo_aluno = {**aluno, "matricula": matricula}
    alunos[matricula] = novo_aluno

    return jsonify(novo_aluno), 201

@app.get("/alunos/<matricula>")
def buscar_aluno(matricula):
    matricula = matricula.upper()
    aluno = alunos.get(matricula)

    if not aluno:
        return jsonify({"erro": "Aluno não encontrado."}), 404

    return jsonify(aluno), 200

@app.put("/alunos/<matricula>")
def atualizar_aluno(matricula):
    matricula = matricula.upper()
    aluno = alunos.get(matricula)

    if not aluno:
        return jsonify({"erro": "Aluno não encontrado."}), 404

    dados = request.get_json(silent=True) or {}
    atualizacoes, _ = normalizar_dados_aluno(dados, obrigatorio=False)

    if atualizacoes["nome"]:
        aluno["nome"] = atualizacoes["nome"]
    if atualizacoes["email"]:
        aluno["email"] = atualizacoes["email"]
    if atualizacoes["curso"]:
        aluno["curso"] = atualizacoes["curso"]

    return jsonify(aluno), 200

@app.delete("/alunos/<matricula>")
def remover_aluno(matricula):
    matricula = matricula.upper()
    aluno_removido = alunos.pop(matricula, None)

    if not aluno_removido:
        return jsonify({"erro": "Aluno não encontrado."}), 404

    return jsonify({"mensagem": "Aluno removido com sucesso."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
