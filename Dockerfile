FROM python:3.12-slim

WORKDIR /app

COPY crud_alunos.py .

CMD ["python", "crud_alunos.py"]
