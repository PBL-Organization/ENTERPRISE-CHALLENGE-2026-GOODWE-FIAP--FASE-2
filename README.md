# Ev-ChargeOps: Sistema Inteligente de Gestão, Telemetria e Faturamento para Veículos Elétricos

## 1. Descrição da Solução Implementada
O **Ev-ChargeOps** é uma solução de software desenvolvida para o ecossistema de carregamento de veículos elétricos e inversores (com foco conceitual na linha GoodWe HCA G2). A arquitetura foi projetada para integrar o fluxo completo de dados em um ambiente residencial multifamiliar ou corporativo:
- **Camada de Borda (Edge):** Simulação de dispositivos de recarga gerando pacotes de telemetria operacional.
- **Camada de Gateway e API Core:** Recepção de dados de sessão via FastAPI, com validação estrita de contratos de dados através do Pydantic.
- **Camada de Persistência:** Banco de dados relacional (SQLite/MySQL) com controle de integridade referencial e idempotência baseada em hash criptográfico SHA-256 para evitar duplicidade de pacotes enviados pela rede.
- **Camada Financeira (Rateio):** Motor de cálculo contábil utilizando aritmética de precisão exata (`Decimal`) para rateio de energia e taxas condominiais.
- **Camada de Inteligência Analítica (Machine Learning):** Módulos de projeção de consumo energético via Regressão Linear e detecção multivariada de anomalias operacionais via *Isolation Forest*.

## 2. Estrutura do Repositório
O projeto está organizado modularmente para garantir o desacoplamento de responsabilidades:
- `analise_consumo.py`: Modelos preditivos (Regressão Linear) e detecção de anomalias em telemetria via *scikit-learn*.
- `api_gateway.py`: Servidor HTTP assíncrono (FastAPI) responsável pelo roteamento de sessões e contratos Pydantic.
- `database.py`: Gerenciamento da persistência local em SQLite e controle de idempotência por hash de payload.
- `main.py`: Entrada alternativa da API Central com foco em processamento de borda e serialização decimal.
- `rateio.py`: Módulo financeiro contábil para cálculo individualizado de contas de luz com arredondamento estrito (`ROUND_HALF_UP`).
- `simulador_borda.py`: Script cliente que simula o hardware disparando requisições HTTP POST para a API.
- `schema.sql`: DDL relacional estruturado para ambientes de banco de dados corporativos (MySQL/MariaDB).
- `requirements.txt`: Relatório de dependências fixadas para reprodutibilidade de ambiente.

## 3. Instruções de Execução

### Pré-requisitos
Certifique-se de possuir o **Python 3.10+** instalado em sua máquina.

1. **Clone o repositório e acesse o diretório do projeto:**
   ```bash
   git clone [https://github.com/PBL-Organization/ENTERPRISE-CHALLENGE-2026-GOODWE-FIAP--FASE-2.git](https://github.com/PBL-Organization/ENTERPRISE-CHALLENGE-2026-GOODWE-FIAP--FASE-2.git)
   cd ENTERPRISE-CHALLENGE-2026-GOODWE-FIAP--FASE-2
Crie e ative um ambiente virtual (Virtual Environment):

Bash
python -m venv venv
# No Windows (PowerShell):
.\venv\Scripts\Activate
# No Linux/macOS:
source venv/bin/activate
Instale as dependências oficiais:

Bash
pip install -r requirements.txt
Executando os Módulos Independentes
Executar a Análise Preditiva e Detecção de Anomalias (Machine Learning):

Bash
python analise_consumo.py
Executar o Teste do Motor Financeiro (Rateio):

Bash
python rateio.py
Executando o Fluxo de Integração API + Simulador de Borda
Inicie o servidor da API Gateway (em um terminal):

Bash
uvicorn api_gateway:app --reload
Dispare o simulador de telemetria do hardware (em outro terminal):

Bash
python simulador_borda.py
4. Decisões Técnicas Tomadas
Adoção do FastAPI e Pydantic: Escolhido por sua altíssima performance assíncrona (baseada em Starlette), geração automática de documentação interativa e robustez na validação de tipos em tempo de execução. O uso de @model_validator garante que regras de negócio complexas (como ocioso_minutos <= tempo_conexao_minutos) sejam bloqueadas na borda do servidor antes de tocarem no banco de dados.

Tratamento Contábil com Decimal (rateio.py): Diferente de linguagens ou scripts que utilizam tipos de ponto flutuante nativos (float), o que gera distorções matemáticas por arredondamento binário (padrão IEEE 754), o Ev-ChargeOps emprega a classe Decimal combinada com a diretiva de arredondamento ROUND_HALF_UP. Isso assegura exatidão jurídica e contábil nos valores cobrados dos moradores.

Idempotência Criptográfica na Persistência (database.py): Dispositivos de IoT em campo frequentemente sofrem instabilidades de rede e realizam reenvios (retries) de pacotes idênticos. Para evitar duplicação de registros de sessões de recarga, o payload JSON é normalizado, ordenado por chaves e convertido em um hash SHA-256 (payload_hash), armazenado com restrição de unicidade no banco de dados.

Modelagem de Machine Learning Desacoplada: A escolha do Isolation Forest para anomalias em vez de limiares estáticos (if/else) permite que o sistema identifique desvios multivariados complexos (relacionando voltagem, corrente e temperatura simultaneamente), enquanto a Regressão Linear modela a tendência linear de consumo acumulado no tempo.

5. Justificativa de Desvios (Sprint 01 vs. Sprint Atual)
Comparado ao escopo inicial planejado na Sprint 01 (focado primariamente em um protótipo conceitual estático baseado em arquivos CSV e scripts monolíticos), a arquitetura atual sofreu uma evolução estrutural necessária para atender aos requisitos de nível corporativo (Enterprise):

Evolução de Script para Arquitetura Distribuída: A lógica inicial concentrada em funções isoladas foi dividida em um modelo cliente-servidor real (Simulador de Borda vs. API Gateway).

Inclusão de Camada de Persistência Transacional: Substituiu-se o armazenamento volátil por um banco de dados relacional estruturado, incorporando o esquema DDL em schema.sql e gerenciamento via SQLite para assegurar auditoria das sessões.

Rigor Contábil: Adição do módulo de rateio estrito com Decimal, superando a limitação anterior de cálculos aproximados por float.
