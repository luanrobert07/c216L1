import time

from fastapi import Request


async def log_requests(request: Request, call_next):
    inicio = time.time()
    print(f">> {request.method} {request.url.path}")

    response = await call_next(request)

    duracao = time.time() - inicio
    print(f"<< {response.status_code} - {duracao:.4f}s")
    return response
