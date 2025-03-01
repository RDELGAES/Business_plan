import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from modules import pricing, market_estimation

def main():
    st.title("Business Plan - Hub de Marketplace Crossborder")
    st.write("Configure os planos, estime o mercado, analise os custos e o breakeven da operação.")

    # Criação das abas
    tabs = st.tabs(["Configuração dos Planos", "Estimativa de Mercado", "Custos & Breakeven", "Sobre"])

    #############################
    # Aba 1: Configuração dos Planos
    #############################
    with tabs[0]:
        st.header("Configuração dos Planos")
        st.write(
            "Defina as variáveis de cada plano. Os campos opcionais (Número de Pedidos, Ticket Médio, "
            "Percentual da Venda e Preço por Pedido) serão usados para compor o pricing."
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
        plan_prices = {}
        for plan in plan_names:
            price = pricing.calculate_plan_price(plan_data[plan])
            plan_prices[plan] = price
            st.write(f"Preço calculado para o plano {plan}: R$ {price:,.2f}")
        
        # Armazena os preços na sessão para uso posterior
        st.session_state["plan_prices"] = plan_prices

    #############################
    # Aba 2: Estimativa de Mercado (TAM & SAM + Taxa de Adoção)
    #############################
    with tabs[1]:
        st.header("Estimativa de Mercado (TAM & SAM)")
        st.write("Preencha os campos para estimar o TAM (Total Addressable Market) e o SAM (Serviceable Addressable Market) para cada cenário.")

        st.subheader("Cenário 1: LATAM enviando para os EUA")
        tam_latam_eua = st.number_input("TAM - Sellers LATAM que vendem para os EUA:", value=10000, step=100)
        # Aqui, em vez de inserir SAM manualmente, calculamos a partir da taxa de adoção
        adoption_rate_latam = st.slider("Taxa de adoção estimada (sellers que utilizarão o hub) [%]:", 0, 100, 10)
        # Armazena a taxa de adoção na sessão para uso posterior
        st.session_state["adoption_rate_latam"] = adoption_rate_latam
        sam_latam_eua = tam_latam_eua * (adoption_rate_latam / 100)
        st.write(f"Com essa taxa de adoção, o SAM (sellers que utilizarão o hub) é: {int(sam_latam_eua)}")
        st.progress(int(adoption_rate_latam))

        st.subheader("Cenário 2: EUA/CHINA enviando para LATAM")
        tam_eua_china_latam = st.number_input("TAM - Sellers dos EUA/CHINA que vendem para LATAM:", value=8000, step=100)
        # Neste cenário, você pode inserir a taxa de adoção manualmente se desejar
        adoption_rate_eua_china = st.slider("Taxa de adoção estimada para esse cenário [%]:", 0, 100, 10, key="adoption_rate_eua_china")
        sam_eua_china_latam = tam_eua_china_latam * (adoption_rate_eua_china / 100)
        st.write(f"Com essa taxa de adoção, o SAM é: {int(sam_eua_china_latam)}")
        st.progress(int(adoption_rate_eua_china))

        st.markdown("---")
        st.write("Resumo dos mercados:")
        st.write(f"**LATAM → EUA:** TAM = {tam_latam_eua}, SAM = {int(sam_latam_eua)}")
        st.write(f"**EUA/CHINA → LATAM:** TAM = {tam_eua_china_latam}, SAM = {int(sam_eua_china_latam)}")

        st.markdown("---")
        st.subheader("Share dos Planos")
        share_starter = st.number_input("Share do Plano Starter (%):", value=60.0, step=1.0, format="%.2f", key="share_starter")
        share_growth = st.number_input("Share do Plano Growth (%):", value=30.0, step=1.0, format="%.2f", key="share_growth")
        share_enterprise = st.number_input("Share do Plano Enterprise (%):", value=10.0, step=1.0, format="%.2f", key="share_enterprise")
        st.write("Shares: Starter =", share_starter, "%, Growth =", share_growth, "%, Enterprise =", share_enterprise, "%")
        # Armazena os shares para uso posterior
        st.session_state["plan_shares"] = {
            "Starter": share_starter,
            "Growth": share_growth,
            "Enterprise": share_enterprise
        }

    #############################
    # Aba 3: Custos & Breakeven
    #############################
    with tabs[2]:
        st.header("Custos & Breakeven (24 meses)")
        st.write("Insira os custos operacionais e projete o número de sellers necessário para cobrir os custos em 24 meses.")

        st.subheader("Custos Operacionais (24 meses)")
        sw_cost = st.number_input("Custos de aquisição SW (R$):", value=5000.0, step=100.0, format="%.2f", key="sw_cost")
        sw_months = st.number_input("Quantidade de meses para custo SW:", value=12, step=1, key="sw_months")
        
        advisor_cost = st.number_input("Custos Advisor (R$):", value=3000.0, step=100.0, format="%.2f", key="advisor_cost")
        advisor_months = st.number_input("Quantidade de meses para Advisor:", value=12, step=1, key="advisor_months")
        
        maintenance_cost = st.number_input("Custo de manutenção (R$):", value=2000.0, step=100.0, format="%.2f", key="maintenance_cost")
        maintenance_months = st.number_input("Quantidade de meses para manutenção:", value=24, step=1, key="maintenance_months")

        # Limita a quantidade de meses a 24 (horizonte)
        total_cost = (sw_cost * min(sw_months, 24)) + (advisor_cost * min(advisor_months, 24)) + (maintenance_cost * min(maintenance_months, 24))
        st.write(f"Custo total projetado para 24 meses: R$ {total_cost:,.2f}")

        st.subheader("Projeção de Sellers e Receita")
        st.write("Preencha os parâmetros para a projeção de vendas (as vendas começam a partir de um determinado mês).")
        start_month = st.number_input("Mês de início das vendas:", value=7, step=1)
        initial_sellers = st.number_input("Número inicial de sellers no mês de início:", value=10, step=1)
        growth_rate = st.number_input("Taxa de crescimento mensal dos sellers (%):", value=10.0, step=0.1, format="%.2f")

        # Recupera os preços dos planos e os shares definidos
        plan_prices = st.session_state.get("plan_prices", {"Starter":0, "Growth":0, "Enterprise":0})
        plan_shares = st.session_state.get("plan_shares", {"Starter":60.0, "Growth":30.0, "Enterprise":10.0})
        weighted_price = (plan_prices.get("Starter",0) * (plan_shares.get("Starter",0)/100) +
                          plan_prices.get("Growth",0) * (plan_shares.get("Growth",0)/100) +
                          plan_prices.get("Enterprise",0) * (plan_shares.get("Enterprise",0)/100))
        st.write(f"Preço médio ponderado dos planos: R$ {weighted_price:,.2f}")

        st.markdown("---")
        st.write("**Simulação dos 24 meses:**")
        # Simulação: vendedores acumulados e receita mensal
        months = list(range(1, 25))
        cumulative_sellers = []
        monthly_revenues = []
        cumulative_revenues = []
        total_sellers = 0

        for m in months:
            if m < start_month:
                new_sellers = 0
            elif m == start_month:
                new_sellers = initial_sellers
            else:
                new_sellers = initial_sellers * ((1 + growth_rate/100) ** (m - start_month))
            total_sellers += new_sellers
            cumulative_sellers.append(total_sellers)
            monthly_rev = total_sellers * weighted_price
            monthly_revenues.append(monthly_rev)
            if m == 1:
                cumulative_revenues.append(monthly_rev)
            else:
                cumulative_revenues.append(cumulative_revenues[-1] + monthly_rev)

        df_breakeven = pd.DataFrame({
            "Mês": months,
            "Vendedores Acumulados": cumulative_sellers,
            "Receita Mensal (R$)": monthly_revenues,
            "Receita Acumulada (R$)": cumulative_revenues
        })
        st.dataframe(df_breakeven)

        # Determina o mês de breakeven (quando a receita acumulada supera o custo total)
        breakeven_month = None
        for idx, rev in enumerate(cumulative_revenues):
            if rev >= total_cost:
                breakeven_month = months[idx]
                break
        if breakeven_month:
            st.success(f"Breakeven alcançado no mês: {breakeven_month}")
        else:
            st.warning("Breakeven não alcançado em 24 meses.")

        # Exibe a barra de progresso com a taxa de adoção (obtida na aba Estimativa de Mercado)
        adoption_rate_latam = st.session_state.get("adoption_rate_latam", 10)
        st.write(f"Taxa de Adoção (sellers que utilizarão o hub): {adoption_rate_latam}%")
        st.progress(int(adoption_rate_latam))

        # Gráfico de Receita Acumulada x Custo Total
        fig, ax = plt.subplots()
        ax.plot(months, cumulative_revenues, label="Receita Acumulada")
        ax.hlines(total_cost, xmin=1, xmax=24, colors='r', linestyles='dashed', label="Custo Total")
        ax.set_xlabel("Mês")
        ax.set_ylabel("Valor (R$)")
        ax.set_title("Receita Acumulada vs. Custo Total (24 meses)")
        ax.legend()
        st.pyplot(fig)

    #############################
    # Aba 4: Sobre
    #############################
    with tabs[3]:
        st.header("Sobre")
        st.write(
            "Este sistema foi desenvolvido para auxiliar na criação de um business plan para um hub de marketplace crossborder.\n\n"
            "Você pode configurar planos de cobrança com variáveis ajustáveis, estimar o mercado (TAM e SAM com share dos planos e taxa de adoção) e "
            "analisar os custos operacionais junto com a projeção do número de sellers necessário para atingir o breakeven em 24 meses."
        )

if __name__ == '__main__':
    main()

