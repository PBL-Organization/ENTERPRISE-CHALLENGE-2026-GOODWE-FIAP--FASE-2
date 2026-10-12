"""API Gateway isolada para a frente de API/Core Backend.

Executar com:
    uvicorn api_gateway:app --reload

O endpoint /sessao mantém exatamente o contrato já usado pelo simulador.
"""

from contextlib import asynccontextmanager
from typing import Literal

from fastapi import FastAPI, Response, status
from pydantic import BaseModel, Field, model_validator

from database import init_db, salvar_sessao


class SessaoRecarga(BaseModel):
    id_usuario: str = Field(min_length=1)
    id_unidade: str = Field(min_length=1)
    id_carregador: str = Field(min_length=1)
    kwh_consumido: float = Field(ge=0)
    tempo_conexao_minutos: int = Field(ge=0)
    ocioso_minutos: int = Field(ge=0)
    status_sessao: Literal["CONCLUIDA", "EM_ANDAMENTO", "CANCELADA"]

    @model_validator(mode="after")
    def validar_tempo_ocioso(self):
        if self.ocioso_minutos > self.tempo_conexao_minutos:
            raise ValueError("ocioso_minutos não pode exceder o tempo de conexão")
        return self


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="EV ChargeOps - API Gateway isolada", lifespan=lifespan)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/sessao", status_code=status.HTTP_201_CREATED)
def receber_sessao(sessao: SessaoRecarga, response: Response) -> dict:
    registro, ja_existia = salvar_sessao(sessao.model_dump())
    if ja_existia:
        response.status_code = status.HTTP_200_OK
    return {
        "id": registro["id"],
        "status": "ja_existia" if ja_existia else "persistida",
        "dados_processados": sessao.model_dump(),
        "recebido_em": registro["recebido_em"],
    }
