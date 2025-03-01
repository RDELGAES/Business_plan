def estimate_revenue(total_sellers, adoption_rate, avg_order_value):
    """
    Estima a receita potencial com base em:
      - total_sellers: número total de sellers disponíveis
      - adoption_rate: percentual (em %) dos sellers que utilizarão o hub
      - avg_order_value: ticket médio dos pedidos
    """
    return (total_sellers * (adoption_rate / 100)) * avg_order_value




