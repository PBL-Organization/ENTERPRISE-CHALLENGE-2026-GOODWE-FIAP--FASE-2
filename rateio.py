from decimal import Decimal, ROUND_HALF_UP

def calcular_conta_morador(kwh_usado: Decimal, preco_kwh: Decimal, taxa_fixa_condominio: Decimal) -> Decimal:
    """
    Fórmula de Cobrança Individualizada do EV ChargeOps (Padrão Enterprise):
    Calcula o custo da energia consumida + a taxa fixa de manutenção,
    garantindo exatidão matemática sem perdas de centavos por arredondamento de float.
    """
    
    # 1. Multiplicação de alta precisão entre o consumo e a tarifa unitária
    custo_luz = kwh_usado * preco_kwh
    
    # 2. Adição da taxa fixa de infraestrutura do condomínio
    total_a_pagar = custo_luz + taxa_fixa_condominio
    
    # 3. Arredondamento contábil rigoroso (ROUND_HALF_UP) para exatamente 2 casas decimais.
    # O método quantize() modela o número para o formato de precisão desejado ('0.01').
    return total_a_pagar.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    # ATENÇÃO DE ENGENHEIRO: Sempre instancie Decimals a partir de STRINGS ('35.5') 
    # e não de floats (35.5), caso contrário a imprecisão entra na raiz do objeto.
    resultado = calcular_conta_morador(
        kwh_usado=Decimal('35.5'), 
        preco_kwh=Decimal('0.90'), 
        taxa_fixa_condominio=Decimal('15.00')
    )
    
    print(f"Valor total contábil a pagar pelo morador: R$ {resultado}")
