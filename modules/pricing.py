def calculate_plan_price(plan):
    """
    Calcula o preço do plano considerando:
      - Taxa Fixa;
      - Receita derivada do preço por pedido: (Número de Pedidos/Mês * Preço por Pedido);
      - Receita derivada do percentual de venda: (Número de Pedidos/Mês * Ticket Médio * (Percentual Venda / 100)).
    """
    base = plan.get("Taxa Fixa", 0)
    num_orders = plan.get("Número de Pedidos/Mês", 0)
    order_price = plan.get("Preço por Pedido", 0)
    avg_ticket = plan.get("Ticket Médio", 0)
    sale_percentage = plan.get("Percentual Venda", 0)
    
    extra_order = num_orders * order_price if num_orders > 0 and order_price > 0 else 0
    extra_sale = num_orders * avg_ticket * (sale_percentage / 100) if num_orders > 0 and avg_ticket > 0 and sale_percentage > 0 else 0
    
    return base + extra_order + extra_sale





