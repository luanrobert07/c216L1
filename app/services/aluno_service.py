from app.schemas.aluno import Aluno, AlunoCreate, AlunoUpdate, Curso


class AlunoService:
    def __init__(self):
        self._alunos: dict[str, Aluno] = {}
        self._matriculas_por_curso: dict[Curso, int] = {curso: 0 for curso in Curso}

    def listar(self) -> list[Aluno]:
        return list(self._alunos.values())

    def buscar_por_id(self, aluno_id: str) -> Aluno | None:
        return self._alunos.get(aluno_id.upper())

    def criar(self, aluno_data: AlunoCreate) -> Aluno:
        matricula = self._proxima_matricula(aluno_data.curso)
        aluno = Aluno(
            id=f"{aluno_data.curso.value}{matricula}",
            matricula=matricula,
            nome=aluno_data.nome,
            email=aluno_data.email,
            curso=aluno_data.curso,
        )
        self._alunos[aluno.id] = aluno
        return aluno

    def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate) -> Aluno | None:
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return None

        dados = aluno_data.model_dump(exclude_unset=True)
        curso_atualizado = dados.get("curso")

        if curso_atualizado and curso_atualizado != aluno.curso:
            matricula = self._proxima_matricula(curso_atualizado)
            dados["id"] = f"{curso_atualizado.value}{matricula}"
            dados["matricula"] = matricula
            del self._alunos[aluno.id]

        dados_atualizados = aluno.model_copy(update=dados)
        self._alunos[dados_atualizados.id] = dados_atualizados
        return dados_atualizados

    def deletar(self, aluno_id: str) -> bool:
        aluno = self.buscar_por_id(aluno_id)
        if not aluno:
            return False

        del self._alunos[aluno.id]
        return True

    def resetar(self) -> None:
        self._alunos.clear()

    def _proxima_matricula(self, curso: Curso) -> int:
        self._matriculas_por_curso[curso] += 1
        return self._matriculas_por_curso[curso]
