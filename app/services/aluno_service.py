from app.db.connection import get_connection
from app.schemas.aluno import AlunoCreate, AlunoUpdate, Curso


class AlunoService:
    async def listar(self):
        conn = await get_connection()
        try:
            rows = await conn.fetch("SELECT * FROM alunos ORDER BY curso, matricula")
            return [dict(row) for row in rows]
        finally:
            await conn.close()

    async def buscar_por_id(self, aluno_id: str):
        conn = await get_connection()
        try:
            row = await conn.fetchrow(
                "SELECT * FROM alunos WHERE id=$1",
                aluno_id.upper(),
            )
            return dict(row) if row else None
        finally:
            await conn.close()

    async def criar(self, aluno_data: AlunoCreate):
        conn = await get_connection()
        try:
            async with conn.transaction():
                matricula = await self._proxima_matricula(conn, aluno_data.curso)
                aluno_id = f"{aluno_data.curso.value}{matricula}"

                row = await conn.fetchrow(
                    """
                    INSERT INTO alunos (id, matricula, nome, email, curso)
                    VALUES ($1, $2, $3, $4, $5)
                    RETURNING *
                    """,
                    aluno_id,
                    matricula,
                    aluno_data.nome,
                    aluno_data.email,
                    aluno_data.curso.value,
                )
                return dict(row)
        finally:
            await conn.close()

    async def atualizar(self, aluno_id: str, aluno_data: AlunoUpdate):
        conn = await get_connection()
        try:
            async with conn.transaction():
                aluno = await conn.fetchrow(
                    "SELECT * FROM alunos WHERE id=$1",
                    aluno_id.upper(),
                )
                if not aluno:
                    return None

                dados = aluno_data.model_dump(exclude_unset=True, exclude_none=True)
                novo_curso = self._valor_curso(dados.get("curso")) or aluno["curso"]
                nova_matricula = aluno["matricula"]
                novo_id = aluno["id"]

                if novo_curso != aluno["curso"]:
                    nova_matricula = await self._proxima_matricula(conn, Curso(novo_curso))
                    novo_id = f"{novo_curso}{nova_matricula}"

                row = await conn.fetchrow(
                    """
                    UPDATE alunos
                    SET id=$1, matricula=$2, nome=$3, email=$4, curso=$5
                    WHERE id=$6
                    RETURNING *
                    """,
                    novo_id,
                    nova_matricula,
                    dados.get("nome", aluno["nome"]),
                    dados.get("email", aluno["email"]),
                    novo_curso,
                    aluno["id"],
                )
                return dict(row) if row else None
        finally:
            await conn.close()

    async def deletar(self, aluno_id: str):
        conn = await get_connection()
        try:
            result = await conn.execute(
                "DELETE FROM alunos WHERE id=$1",
                aluno_id.upper(),
            )
            return result == "DELETE 1"
        finally:
            await conn.close()

    async def resetar(self):
        conn = await get_connection()
        try:
            await conn.execute("DELETE FROM alunos")
        finally:
            await conn.close()

    async def _proxima_matricula(self, conn, curso: Curso) -> int:
        await conn.execute(
            """
            INSERT INTO matriculas_curso (curso, proxima_matricula)
            VALUES ($1, 1)
            ON CONFLICT (curso) DO NOTHING
            """,
            curso.value,
        )

        return await conn.fetchval(
            """
            UPDATE matriculas_curso
            SET proxima_matricula = proxima_matricula + 1
            WHERE curso=$1
            RETURNING proxima_matricula - 1
            """,
            curso.value,
        )

    def _valor_curso(self, curso):
        if curso is None:
            return None
        if isinstance(curso, Curso):
            return curso.value
        return curso
