import json
import urllib.request
import urllib.error
import time

# URL da API Central (A API que a Sarah está configurando)
# Se estiver rodando localmente na mesma máquina, normalmente será http://127.0.0.1:8000/sessao
URL_API = "http://127.0.0.1:8000/sessao"

def gerar_payload_telemetria():
    """
    Simula a geração de dados pelo hardware GoodWe HCA G2
    respeitando estritamente o contrato de dados da arquitetura.
    """
    payload = {
        "id_usuario": "usr_001",
        "id_unidade": "Bloco A - Ap 102",
        "id_carregador": "GoodWe-HCA-G2-L1",
        "kwh_consumido": 35.5,
        "tempo_conexao_minutos": 120,
        "ocioso_minutos": 15,
        "status_sessao": "CONCLUIDA"
    }
    return payload

def disparar_telemetria():
    dados = gerar_payload_telemetria()
    
    # Converte o dicionário Python em uma string JSON formatada em bytes UTF-8
    dados_json = json.dumps(dados).encode('utf-8')
    
    # Prepara a requisição HTTP POST
    req = urllib.request.Request(
        URL_API,
        data=dados_json,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    print(f"[SIMULADOR GOODWE HCA G2] Disparando telemetria para: {URL_API}...")
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            resposta_servidor = response.read().decode('utf-8')
            print(f"[SUCESSO] Servidor respondeu com Status: {status_code}")
            print(f"[RESPOSTA] {resposta_servidor}")
            
    except urllib.error.URLError as e:
        print(f"[ERRO DE CONEXÃO] Não foi possível conectar à API: {e.reason}")
        print("[AVISO] Certifique-se de que a API da Sarah está rodando localmente na porta 8000.")

if __name__ == "__main__":
    # Executa o disparo do simulador
    disparar_telemetria()