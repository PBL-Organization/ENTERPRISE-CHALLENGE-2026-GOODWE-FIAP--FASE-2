import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest

# --- 1. REGRESSÃO DE CONSUMO (Predição de kWh acumulado no tempo) ---
def predict_consumption_trend(time_steps_sec: list, energy_kwh_accumulated: list, future_step_sec: int) -> float:
    """
    Prevê o consumo de energia no tempo t usando Regressão Linear.
    """
    # Converte a lista temporal em um array bidimensional (matriz X), requisito do scikit-learn
    X = np.array(time_steps_sec).reshape(-1, 1)
    
    # Converte a lista de energia acumulada em um array unidimensional (vetor alvo y)
    y = np.array(energy_kwh_accumulated)

    # Instancia o modelo de Regressão Linear Ordinária
    model = LinearRegression()
    
    # Executa o ajuste (treinamento) do modelo minimizando os mínimos quadrados
    model.fit(X, y)

    # Realiza a predição para o passo de tempo futuro informado
    predicted_kwh = model.predict(np.array([[future_step_sec]]))
    
    # Exibe a projeção formatada no console
    print(f"[Regressão] Projeção de consumo para t={future_step_sec}s: {predicted_kwh[0]:.2f} kWh")
    
    # Retorna o valor predito como um tipo primitivo float
    return float(predicted_kwh[0])


# --- 2. DETECÇÃO DE ANOMALIAS (Isolation Forest) ---
def detect_charger_anomalies(telemetry_data: list[dict]) -> pd.DataFrame:
    """
    Analisa variações atípicas de Voltagem, Corrente e Temperatura.
    Exemplo de telemetria suspeita: Voltagem > 250V ou Temp > 80°C.
    """
    # Converte a lista de dicionários em um DataFrame do Pandas para manipulação estruturada
    df = pd.DataFrame(telemetry_data)
    
    # Seleciona as colunas de atributos (features) que passarão pela análise multivariada
    features = ["voltage_v", "current_a", "temperature_c"]
    X = df[features]

    # Inicializa o Isolation Forest configurando a taxa de contaminação esperada em 10%
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    
    # Executa o ajuste e predição, gerando os rótulos (-1 para anomalias, 1 para dados normais)
    df["anomaly_score"] = iso_forest.fit_predict(X)
    
    # Filtra o DataFrame isolando unicamente as linhas sinalizadas como anômalas
    anomalies = df[df["anomaly_score"] == -1]
    
    # Exibe métrica resumida da varredura de anomalias no terminal
    print(f"[Anomalias] Detectadas {len(anomalies)} medições fora do padrão num total de {len(df)} registros.")
    
    # Retorna o conjunto de dados filtrado contendo as anomalias
    return anomalies


# Bloco de execução principal protegido por verificação de escopo global
if __name__ == "__main__":
    # Conjunto de dados de teste para a regressão linear (tempo vs kWh acumulado)
    times = [0, 60, 120, 180, 240, 300]  # Segundos
    kwh = [0.0, 0.12, 0.25, 0.38, 0.51, 0.64]
    
    # Aciona a função de projeção de consumo para t = 600 segundos
    predict_consumption_trend(times, kwh, future_step_sec=600)

    # Conjunto de dados simulados de telemetria contendo um ponto discrepante crítico
    sample_data = [
        {"voltage_v": 220, "current_a": 16, "temperature_c": 40},
        {"voltage_v": 221, "current_a": 15.8, "temperature_c": 41},
        {"voltage_v": 219, "current_a": 16.1, "temperature_c": 39},
        {"voltage_v": 280, "current_a": 45, "temperature_c": 85},  # Anomalia clara inserida propositalmente
        {"voltage_v": 222, "current_a": 16, "temperature_c": 42},
    ]
    
    # Aciona a detecção de anomalias com base na amostra de telemetria
    detected = detect_charger_anomalies(sample_data)
    
    # Imprime no console apenas as colunas de interesse das anomalias isoladas
    print(detected[["voltage_v", "current_a", "temperature_c"]])
