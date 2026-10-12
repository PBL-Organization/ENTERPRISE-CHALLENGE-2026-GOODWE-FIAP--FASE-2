from fastapi import FastAPI
from pydantic import BaseModel
from decimal import Decimal

# Inicializa a aplicação FastAPI
app = FastAPI(title="EV ChargeOps - API Central", version="1.0")

# Define o contrato de dados esperado com precisão contábil (Decimal)
class SessaoRecarga(BaseModel):
    id_usuario: str
    id_unidade: str
    id_carregador: str
    kwh_consumido: Decimal  # Blindado contra as imprecisões do ponto flutuante (float)
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
    
    # Retorna uma resposta de confirmação para a borda.
    # O uso de mode='json' no model_dump garante a serialização correta do tipo Decimal.
    return {
        "status_code": 201,
        "mensagem": "Telemetria processada e gravada com sucesso na API Central.",
        "dados_processados": sessao.model_dump(mode='json')
    }
