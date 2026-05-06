DROP TABLE IF EXISTS alunos;
DROP TABLE IF EXISTS matriculas_curso;

CREATE TABLE matriculas_curso (
    curso TEXT PRIMARY KEY,
    proxima_matricula INTEGER NOT NULL
);

CREATE TABLE alunos (
    id TEXT PRIMARY KEY,
    matricula INTEGER NOT NULL,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    curso TEXT NOT NULL
);
