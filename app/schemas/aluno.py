from enum import Enum

from pydantic import BaseModel, field_validator


class Curso(str, Enum):
    GES = "GES"
    GEC = "GEC"


class AlunoBase(BaseModel):
    nome: str
    email: str
    curso: Curso

    @field_validator("nome", "email")
    @classmethod
    def validar_texto_obrigatorio(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("Campo obrigatorio")
        return valor

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor: str) -> str:
        if "@" not in valor:
            raise ValueError("E-mail invalido")
        return valor


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(BaseModel):
    nome: str | None = None
    email: str | None = None
    curso: Curso | None = None

    @field_validator("nome", "email")
    @classmethod
    def validar_texto_opcional(cls, valor: str | None) -> str | None:
        if valor is None:
            return valor

        valor = valor.strip()
        if not valor:
            raise ValueError("Campo obrigatorio")
        return valor

    @field_validator("email")
    @classmethod
    def validar_email(cls, valor: str | None) -> str | None:
        if valor is not None and "@" not in valor:
            raise ValueError("E-mail invalido")
        return valor


class Aluno(AlunoBase):
    id: str
    matricula: int
