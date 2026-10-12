from fastapi import FastAPI
from pydantic import BaseModel

# Inicializa a aplicação FastAPI
app = FastAPI(title="EV ChargeOps - API Central", version="1.0")

# Define o contrato de dados esperado (Validação automática via Pydantic)
class SessaoRecarga(BaseModel):
    id_usuario: str
    id_unidade: str
    id_carregador: str
    kwh_consumido: float
    tempo_conexao_minutos: int
    ocioso_minutos: int
    status_sessao: str

@app.post("/sessao")
def receber_telemetria_borda(sessao: SessaoRecarga):
    """
    Endpoint que recebe os dados de telemetria enviados pelo simulador 
    do carregador GoodWe HCA G2.
    """
    print("\n[SERVIDOR CENTRAL] Pacote de telemetria capturado com sucesso!")
    print(f"-> Usuário: {sessao.id_usuario} ({sessao.id_unidade})")
    print(f"-> Carregador: {sessao.id_carregador}")
    print(f"-> Volume Consumido: {sessao.kwh_consumido} kWh")
    print(f"-> Status: {sessao.status_sessao}\n")
    
    # Retorna uma resposta de confirmação para a borda
    return {
        "status_code": 201,
        "mensagem": "Telemetria processada e gravada com sucesso na API Central.",
        "dados_processados": sessao.model_dump()
    }