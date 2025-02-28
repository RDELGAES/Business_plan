import streamlit as st
from modules import pricing, market_estimation

def main():
    st.title("Business Plan - Hub de Marketplace Crossborder")
    st.write("Configure os planos e estime o potencial de receita para vendedores LATAM.")

    tabs = st.tabs(["Configuração dos Planos", "Estimativa de Mercado", "Sobre"])

    # Aba 1: Configuração dos Planos
    with tabs[0]:
        st.header("Planos de Cobrança")
        st.write(
            "Ajuste as variáveis de cada plano. Além dos parâmetros básicos, os campos abaixo são opcionais "
            "para complementar o modelo de cobrança (ex.: número de pedidos por mês, ticket médio e percentual da venda)."
        )

        plan_names = ["Starter", "Growth", "Enterprise"]
        plan_data = {}

        for plan in plan_names:
            st.subheader(f"Plano {plan}")
            fixed_fee = st.number_input(
                f"Taxa Fixa ({plan}) [em R$]", value=100.0, step=10.0, format="%.2f", key=f"{plan}_fixed"
            )
            num_skus = st.number_input(
                f"Número de SKUs Permitidos ({plan})", value=50, step=1, key=f"{plan}_skus"
            )
            num_marketplaces = st.number_input(
                f"Número de Marketplaces Integrados ({plan})", value=2, step=1, key=f"{plan}_marketplaces"
            )
            num_orders = st.number_input(
                f"Número de Pedidos por Mês ({plan}) (opcional)", value=0, step=1, key=f"{plan}_orders"
            )
            avg_ticket = st.number_input(
                f"Ticket Médio do Carrinho ({plan}) (opcional) [em R$]", value=0.0, step=10.0, format="%.2f", key=f"{plan}_ticket"
            )
            sale_percentage = st.number_input(
                f"Percentual da Venda por Pedido ({plan}) (opcional) [%]", value=0.0, step=1.0, format="%.2f", key=f"{plan}_percentage"
            )

            plan_data[plan] = {
                "Taxa Fixa": fixed_fee,
                "Número de SKUs": num_skus,
                "Marketplaces Integrados": num_marketplaces,
                "Número de Pedidos/Mês": num_orders,
                "Ticket Médio": avg_ticket,
                "Percentual Venda": sale_percentage
            }
            st.write("Configuração do plano:", plan_data[plan])
        
        st.markdown("---")
        st.write("Resumo dos Planos:")
        st.json(plan_data)

        # Exemplo de uso do módulo pricing para calcular o preço do plano
        st.subheader("Cálculo do Preço dos Planos")
        for plan in plan_names:
            calculated_price = pricing.calculate_plan_price(plan_data[plan])
            st.write(f"Preço calculado para o plano {plan}: R$ {calculated_price:,.2f}")

    # Aba 2: Estimativa de Mercado e Receita
    with tabs[1]:
        st.header("Estimativa de Market Share e Receita")
        st.write(
            "Utilize os campos abaixo para estimar o potencial de receita em dois cenários:\n\n"
            "**1. LATAM para EUA:** Sellers LATAM vendendo para os EUA (ex.: via Amazon, eBay, etc.)\n"
            "**2. EUA para LATAM:** Sellers dos EUA vendendo para a LATAM (ex.: via Mercado Livre, Magalu, B2W, Amazon)"
        )
        
        # Cenário 1: LATAM para EUA
        st.subheader("Cenário 1: LATAM para EUA")
        total_sellers_latam = st.number_input(
            "Número total de sellers LATAM que vendem para os EUA:", value=5000, step=100
        )
        adoption_rate_latam = st.slider(
            "Taxa de adoção estimada (sellers que utilizarão o hub) [%]:", 0, 100, 10
        )
        st.write("**Estimativa de pedidos por canal:**")
        orders_amazon = st.number_input("Pedidos mensais via Amazon:", value=0, step=10)
        orders_ebay = st.number_input("Pedidos mensais via eBay:", value=0, step=10)
        orders_outros = st.number_input("Pedidos mensais via outros canais:", value=0, step=10)
        
        avg_order_value_latam = st.number_input(
            "Ticket Médio dos pedidos (LATAM -> EUA) [em R$]:", value=150.0, step=10.0, format="%.2f"
        )
        
        potencial_receita_latam = market_estimation.estimate_revenue(total_sellers_latam, adoption_rate_latam, avg_order_value_latam)
        st.write(f"Receita potencial (LATAM para EUA): R$ {potencial_receita_latam:,.2f} por período")
        
        st.markdown("---")
        
        # Cenário 2: EUA para LATAM
        st.subheader("Cenário 2: EUA para LATAM")
        total_sellers_eua = st.number_input(
            "Número total de sellers dos EUA que vendem para LATAM:", value=3000, step=100
        )
        adoption_rate_eua = st.slider(
            "Taxa de adoção estimada (sellers que utilizarão o hub) [%]:", 0, 100, 10, key="adoption_eua"
        )
        st.write("**Estimativa de pedidos por canal:**")
        orders_mercado_livre = st.number_input("Pedidos mensais via Mercado Livre:", value=0, step=10)
        orders_magalu = st.number_input("Pedidos mensais via Magalu:", value=0, step=10)
        orders_b2w = st.number_input("Pedidos mensais via B2W:", value=0, step=10)
        orders_amazon_latam = st.number_input("Pedidos mensais via Amazon (LATAM):", value=0, step=10)
        
        avg_order_value_eua = st.number_input(
            "Ticket Médio dos pedidos (EUA -> LATAM) [em R$]:", value=120.0, step=10.0, format="%.2f"
        )
        
        potencial_receita_eua = market_estimation.estimate_revenue(total_sellers_eua, adoption_rate_eua, avg_order_value_eua)
        st.write(f"Receita potencial (EUA para LATAM): R$ {potencial_receita_eua:,.2f} por período")
        
        st.markdown("---")
        
        # Nova seção: Receita de Assinatura com Peso para cada plano
        st.subheader("Receita de Assinatura dos Planos")
        st.write("Defina o percentual de adesão para cada plano (a soma deve ser igual a 100%).")
        weight_starter = st.number_input("Peso do Plano Starter [%]:", value=40.0, step=1.0, format="%.2f")
        weight_growth = st.number_input("Peso do Plano Growth [%]:", value=40.0, step=1.0, format="%.2f")
        weight_enterprise = st.number_input("Peso do Plano Enterprise [%]:", value=20.0, step=1.0, format="%.2f")
        
        total_subscription_revenue = 0
        total_adopters = total_sellers_latam * (adoption_rate_latam / 100)
        for plan in ["Starter", "Growth", "Enterprise"]:
            weight = {"Starter": weight_starter, "Growth": weight_growth, "Enterprise": weight_enterprise}[plan]
            price = pricing.calculate_plan_price(plan_data[plan])
            plan_revenue = total_adopters * (weight / 100) * price
            total_subscription_revenue += plan_revenue
            st.write(f"Receita do plano {plan}: R$ {plan_revenue:,.2f}")
        
        st.write(f"Receita total de assinatura dos planos: R$ {total_subscription_revenue:,.2f} por período")
        
        st.markdown("### Racional das Estimativas")
        st.write("""
        **Cenário LATAM -> EUA:**
        - **Número total de sellers:** Quantidade de sellers LATAM que exportam para os EUA. (Valor arbitrário para demonstração; realize pesquisas de mercado para dados reais)
        - **Taxa de adoção:** Percentual desses sellers que aderirão ao hub.
        - **Ticket Médio:** Valor médio de cada pedido.
        - **Pedidos por canal:** Permite entender a distribuição dos pedidos entre Amazon, eBay e outros.
        
        **Cenário EUA -> LATAM:**
        - **Número total de sellers:** Sellers dos EUA que exportam para a LATAM. (Valor arbitrário; ajuste conforme dados reais)
        - **Taxa de adoção:** Percentual de sellers que utilizarão o hub.
        - **Ticket Médio:** Valor médio de cada pedido.
        - **Pedidos por canal:** Separação por canais (Mercado Livre, Magalu, B2W, Amazon).
        
        **Receita de Assinatura dos Planos:**
        - **Peso dos Planos:** Percentual de sellers que optarão por cada plano, utilizado para estimar a receita com base no preço calculado para cada plano.
        """)

    # Aba 3: Sobre
    with tabs[2]:
        st.header("Sobre")
        st.write(
            "Este sistema foi desenvolvido para auxiliar na criação de um business plan para um hub de marketplace crossborder. \n\n"
            "Os números de sellers utilizados nas estimativas são arbitrários e servem apenas como exemplo. Recomendamos realizar "
            "pesquisas de mercado para obter dados reais e ajustar os parâmetros conforme a realidade do setor.\n\n"
            "O sistema permite configurar planos de cobrança com variáveis ajustáveis, estimar o potencial de receita com base em dois cenários de mercado e calcular a receita de assinatura levando em conta o share de adesão para cada plano."
        )

if __name__ == '__main__':
    main()


