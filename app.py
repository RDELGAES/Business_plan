import streamlit as st
import pandas as pd
from modules import pricing, market_estimation

def main():
    st.title("Business Plan - Hub de Marketplace Crossborder")
    st.write("Configure os planos, estime as receitas e analise o payback do investimento.")

    # Criação das abas
    tabs = st.tabs(["Configuração dos Planos", "Estimativa de Mercado", "Análise de Payback", "Sobre"])

    # Aba 1: Configuração dos Planos
    with tabs[0]:
        st.header("Planos de Cobrança")
        st.write(
            "Ajuste as variáveis de cada plano. Além dos parâmetros básicos, os campos opcionais "
            "permitirão complementar o modelo de cobrança, como número de pedidos, ticket médio, "
            "percentual da venda e preço por pedido."
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
            order_price = st.number_input(
                f"Preço por Pedido ({plan}) (opcional) [em R$]", value=0.0, step=10.0, format="%.2f", key=f"{plan}_order_price"
            )

            plan_data[plan] = {
                "Taxa Fixa": fixed_fee,
                "Número de SKUs": num_skus,
                "Marketplaces Integrados": num_marketplaces,
                "Número de Pedidos/Mês": num_orders,
                "Ticket Médio": avg_ticket,
                "Percentual Venda": sale_percentage,
                "Preço por Pedido": order_price
            }
            st.write("Configuração do plano:", plan_data[plan])
        
        st.markdown("---")
        st.write("Resumo dos Planos:")
        st.json(plan_data)

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
        - **Número total de sellers:** Quantidade de sellers LATAM que exportam para os EUA.
        - **Taxa de adoção:** Percentual desses sellers que aderirão ao hub.
        - **Ticket Médio:** Valor médio de cada pedido.
        - **Pedidos por canal:** Distribuição dos pedidos entre os canais.
        
        **Cenário EUA -> LATAM:**
        - **Número total de sellers:** Sellers dos EUA que exportam para a LATAM.
        - **Taxa de adoção:** Percentual de sellers que utilizarão o hub.
        - **Ticket Médio:** Valor médio de cada pedido.
        - **Pedidos por canal:** Distribuição dos pedidos entre os canais.
        
        **Receita de Assinatura:**
        - **Peso dos Planos:** Percentual de sellers que optarão por cada plano, usado para estimar a receita com base no preço calculado.
        """)
        
        # Armazena a receita de assinatura na sessão para uso na análise de payback
        st.session_state["subscription_revenue"] = total_subscription_revenue

    # Aba 3: Análise de Payback
    with tabs[2]:
        st.header("Análise de Payback")
        st.write("Esta análise utiliza as receitas projetadas dos planos para estimar em quantos meses o investimento será recuperado.")

        # Obter o investimento via CSV ou entrada manual
        uploaded_file = st.file_uploader("Faça o upload do CSV com os dados do investimento (coluna 'Investimento')", type="csv")
        if uploaded_file is not None:
            df_invest = pd.read_csv(uploaded_file)
            st.write("Dados do Investimento:")
            st.dataframe(df_invest)
            if "Investimento" in df_invest.columns:
                total_investment = df_invest["Investimento"].sum()
                st.write("Investimento Total: R$", total_investment)
            else:
                st.error("A coluna 'Investimento' não foi encontrada no CSV.")
                total_investment = st.number_input("Insira o investimento total manualmente (R$):", value=0.0)
        else:
            st.info("Faça o upload do arquivo CSV ou insira o investimento manualmente.")
            total_investment = st.number_input("Insira o investimento total (R$):", value=0.0)

        # Utiliza a receita projetada dos planos (caso já esteja calculada)
        if "subscription_revenue" in st.session_state:
            monthly_revenue = st.session_state["subscription_revenue"]
            st.write(f"Receita mensal projetada (dos planos): R$ {monthly_revenue:,.2f}")
        else:
            st.info("Receita de assinatura não disponível. Insira o valor manualmente.")
            monthly_revenue = st.number_input("Receita Recorrente Mensal (R$):", value=50000.0, step=1000.0, format="%.2f")
        
        # Permite definir uma taxa de crescimento (opcional)
        growth_rate = st.number_input("Taxa de Crescimento Mensal (%) (Ex: 0 para sem crescimento):", value=0.0, step=0.1, format="%.2f")

        # Botão para calcular o payback com base nas receitas projetadas
        if st.button("Calcular Payback"):
            months = []
            monthly_revenues = []
            cumulative_revenues = []

            cumulative = -total_investment  # Começamos com o valor negativo do investimento
            month = 0
            # Simula até 60 meses ou até que o acumulado seja >= 0
            while month < 60 and cumulative < 0:
                months.append(month)
                if month == 0:
                    current_revenue = monthly_revenue
                else:
                    current_revenue = monthly_revenues[-1] * (1 + growth_rate / 100)
                monthly_revenues.append(current_revenue)
                cumulative += current_revenue
                cumulative_revenues.append(cumulative)
                month += 1

            df_payback = pd.DataFrame({
                "Mês": months,
                "Receita Mensal (R$)": monthly_revenues,
                "Receita Acumulada (R$)": cumulative_revenues
            })
            st.dataframe(df_payback)

            if cumulative >= 0:
                payback_month = df_payback[df_payback["Receita Acumulada (R$)"] >= 0].iloc[0]["Mês"]
                st.success(f"Payback alcançado no mês: {int(payback_month)}")
            else:
                st.warning("Payback não alcançado em 60 meses.")

    # Aba 4: Sobre
    with tabs[3]:
        st.header("Sobre")
        st.write(
            "Este sistema foi desenvolvido para auxiliar na criação de um business plan para um hub de marketplace crossborder.\n\n"
            "Você pode configurar planos de cobrança com variáveis ajustáveis, estimar o potencial de receita em diferentes cenários e analisar o payback do investimento utilizando as receitas projetadas dos planos."
        )

if __name__ == '__main__':
    main()

