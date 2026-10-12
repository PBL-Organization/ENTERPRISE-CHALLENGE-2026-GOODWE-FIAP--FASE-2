def calcular_conta_morador(kwh_usado, preco_kwh, taxa_fixa_condominio):
    """
    Fórmula de Cobrança Individualizada do EV ChargeOps:
    Calcula o custo da energia consumida + a taxa proporcional de manutenção do carregador.
    """
    custo_luz = kwh_usado * preco_kwh
    total_a_pagar = custo_luz + taxa_fixa_condominio
    return round(total_a_pagar, 2)

if __name__ == "__main__":
    # Exemplo de teste da fórmula:
    resultado = calcular_conta_morador(kwh_usado=30.0, preco_kwh=0.80, taxa_fixa_condominio=10.00)
    print(f"Valor total a pagar pelo morador: R$ {resultado}")
    