def calculate_plan_price(plan):
    """
    Calcula um preço base para o plano a partir dos parâmetros informados.
    Lógica:
      - Preço base = Taxa Fixa
      - Se os valores opcionais forem informados (número de pedidos, ticket médio e percentual da venda),
        adiciona um valor extra baseado na receita estimada desses pedidos.
    """
    base = plan.get("Taxa Fixa", 0)
    num_orders = plan.get("Número de Pedidos/Mês", 0)
    avg_ticket = plan.get("Ticket Médio", 0)
    sale_percentage = plan.get("Percentual Venda", 0)
    
    extra = 0
    if num_orders > 0 and avg_ticket > 0 and sale_percentage > 0:
        extra = num_orders * avg_ticket * (sale_percentage / 100)
    
    return base + extra


