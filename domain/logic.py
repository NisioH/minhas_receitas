def parse_decimal(texto):
    normalizado = texto.strip().replace(",", ".")
    try:
        return True, float(normalizado)
    except ValueError:
        return False, "Valor decimal inválido."

def validar_unidade(unidade):
    unidades_validas = ("ml", "g", "und")
    return unidade in unidades_validas

def calcular_preco_unitario(preco_pacote, quantidade_pacote):
    if quantidade_pacote <= 0:
        return False, "Quantidade do pacote deve ser maior que zero."
    preco_unitario = preco_pacote / quantidade_pacote
    return True, preco_unitario

def calcular_custo_por_porcao(receita: dict, ingredientes: list): 
    
    try: 
        custo_total = 0 
        for ing in ingredientes: 
            ok, preco_unit = calcular_preco_unitario( 
                ing["preco_pacote"], ing["quantidade_pacote"] 
                ) 
            if not ok: 
                return False, preco_unit 
            custo_total += ing["quantidade"] * preco_unit 
    
        rendimento = receita.get("rendimento", 0) 
        custo_por_porcao = custo_total / rendimento if rendimento > 0 else 0 
        return True, { 
            "custo_total": round(custo_total, 2), 
            "custo_por_porcao": round(custo_por_porcao, 3) 
            } 
    
    except Exception as e: 
        return False, f"Erro ao calcular custo: {e}"