from fastapi import FastAPI
from auth_routers import auth_router
from motorista_routers import motorista_router
from documento_routers import documento_router          # ← novo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Smartfrota API",
    version="1.0.0",
    description="Backend da plataforma de gestão de frotas Smartfrota.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrinja para domínios específicos em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(motorista_router)
app.include_router(documento_router)                   # ← registra as rotas de documentos