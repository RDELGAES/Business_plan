import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json, os
from modules import pricing, market_estimation

def main():
    st.title("Business Plan - Hub de Marketplace Crossborder")
    st.write("Configure os planos, estime o mercado, analise os custos, o breakeven e salve seus cenários.")

    # Criação das abas
    tabs = st.tabs(["Configuração dos Planos", "Estimativa de Mercado", "Custos & Breakeven", "Sobre", "Cenários Salvos"])

    #############################
    # Aba 1: Configuração dos Planos
    #############################
    with tabs[0]:
        st.header("Configuração dos Planos")
        st.write(
            "Defina as variáveis de cada plano. O preço será calculado como Taxa Fixa + maior entre: "
            "Preço por Pedido (Número de Pedidos × Preço por Pedido) ou Percentual da Venda (Número de Pedidos × Ticket Médio × Percentual/100)."
        )
        plan_names = ["Starter", "Growth", "Enterprise"]
        plan_data = {}

        # Valores padrão exemplares com base na sugestão:
        defaults = {
            "Starter": {"Taxa Fixa": 100.0, "Número de SKUs": 50, "Marketplaces Integrados": 1,
                        "Número de Pedidos/Mês": 100, "Ticket Médio": 100.0, "Percentual Venda": 1.5, "Preço por Pedido": 2.0},
            "Growth": {"Taxa Fixa": 400.0, "Número de SKUs": 100, "Marketplaces Integrados": 3,
                       "Número de Pedidos/Mês": 200, "Ticket Médio": 200.0, "Percentual Venda": 2.0, "Preço por Pedido": 3.0},
            "Enterprise": {"Taxa Fixa": 1200.0, "Número de SKUs": 200, "Marketplaces Integrados": 5,
                           "Número de Pedidos/Mês": 500, "Ticket Médio": 300.0, "Percentual Venda": 3.0, "Preço por Pedido": 5.0}
        }

        for plan in plan_names:
            st.subheader(f"Plano {plan}")
            fixed_fee = st.number_input(
                f"Taxa Fixa ({plan}) [em R$]", value=defaults[plan]["Taxa Fixa"], step=10.0, format="%.2f", key=f"{plan}_fixed"
            )
            num_skus = st.number_input(
                f"Número de SKUs Permitidos ({plan})", value=defaults[plan]["Número de SKUs"], step=1, key=f"{plan}_skus"
            )
            num_marketplaces = st.number_input(
                f"Número de Marketplaces Integrados ({plan})", value=defaults[plan]["Marketplaces Integrados"], step=1, key=f"{plan}_marketplaces"
            )
            num_orders = st.number_input(
                f"Número de Pedidos por Mês ({plan})", value=defaults[plan]["Número de Pedidos/Mês"], step=1, key=f"{plan}_orders"
            )
            avg_ticket = st.number_input(
                f"Ticket Médio do Carrinho ({plan}) [em R$]", value=defaults[plan]["Ticket Médio"], step=10.0, format="%.2f", key=f"{plan}_ticket"
            )
            sale_percentage = st.number_input(
                f"Percentual da Venda por Pedido ({plan}) [%]", value=defaults[plan]["Percentual Venda"], step=0.1, format="%.2f", key=f"{plan}_percentage"
            )
            order_price = st.number_input(
                f"Preço por Pedido ({plan}) [em R$]", value=defaults[plan]["Preço por Pedido"], step=0.5, format="%.2f", key=f"{plan}_order_price"
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
        
        st.session_state["plan_prices"] = plan_prices

    #############################
    # Aba 2: Estimativa de Mercado (TAM, SAM e Taxa de Adoção + Share dos Planos)
    #############################
    with tabs[1]:
        st.header("Estimativa de Mercado (TAM & SAM)")
        st.write("Preencha os campos para estimar o TAM (Total Addressable Market) e, com a taxa de adoção, obtenha o SAM.")

        st.subheader("Cenário 1: LATAM enviando para os EUA")
        # Valor conservador para LATAM: 500.000 sellers
        tam_latam_eua = st.number_input("TAM - Sellers LATAM que vendem para os EUA:", value=500000, step=10000)
        # Taxa de adoção conservadora: 1%
        adoption_rate_latam = st.slider("Taxa de adoção (sellers que utilizarão o hub) [%]:", 0, 100, 1)
        st.session_state["adoption_rate_latam"] = adoption_rate_latam
        sam_latam_eua = tam_latam_eua * (adoption_rate_latam / 100)
        st.write(f"Com essa taxa, o SAM é: {int(sam_latam_eua)}")
        st.progress(int(adoption_rate_latam))

        st.subheader("Cenário 2: EUA/CHINA enviando para LATAM")
        # Valor conservador para EUA/CHINA: 100.000 sellers
        tam_eua_china_latam = st.number_input("TAM - Sellers dos EUA/CHINA que vendem para LATAM:", value=100000, step=1000)
        # Taxa de adoção conservadora: 1%
        adoption_rate_eua_china = st.slider("Taxa de adoção para esse cenário [%]:", 0, 100, 1, key="adoption_rate_eua_china")
        sam_eua_china_latam = tam_eua_china_latam * (adoption_rate_eua_china / 100)
        st.write(f"Com essa taxa, o SAM é: {int(sam_eua_china_latam)}")
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
        st.session_state["plan_shares"] = {
            "Starter": share_starter,
            "Growth": share_growth,
            "Enterprise": share_enterprise
        }

        # Armazena os valores de mercado na sessão para uso posterior
        st.session_state["tam_latam_eua"] = tam_latam_eua
        st.session_state["sam_latam_eua"] = int(sam_latam_eua)
        st.session_state["tam_eua_china_latam"] = tam_eua_china_latam
        st.session_state["sam_eua_china_latam"] = int(sam_eua_china_latam)

    #############################
    # Aba 3: Custos & Breakeven (24 meses)
    #############################
    with tabs[2]:
        st.header("Custos & Breakeven (24 meses)")
        st.write("Insira os custos operacionais e projete o número de sellers necessário para cobrir os custos em 24 meses.")

        st.subheader("Custos Operacionais (24 meses)")
        # Custos de aquisição SW
        sw_cost = st.number_input("Custos de aquisição SW (R$):", value=5000.0, step=100.0, format="%.2f", key="sw_cost")
        sw_months = st.number_input("Meses para custo SW:", value=12, step=1, key="sw_months")
        sw_start = st.number_input("Mês de início para custo SW:", value=1, min_value=1, max_value=24, step=1, key="sw_start")

        # Custos Advisor
        advisor_cost = st.number_input("Custos Advisor (R$):", value=3000.0, step=100.0, format="%.2f", key="advisor_cost")
        advisor_months = st.number_input("Meses para Advisor:", value=12, step=1, key="advisor_months")
        advisor_start = st.number_input("Mês de início para Advisor:", value=1, min_value=1, max_value=24, step=1, key="advisor_start")

        # Custo de manutenção
        maintenance_cost = st.number_input("Custo de manutenção (R$):", value=2000.0, step=100.0, format="%.2f", key="maintenance_cost")
        maintenance_months = st.number_input("Meses para manutenção:", value=24, step=1, key="maintenance_months")
        maintenance_start = st.number_input("Mês de início para manutenção:", value=1, min_value=1, max_value=24, step=1, key="maintenance_start")

        # Calcula os meses efetivos para cada custo
        effective_sw_months = max(0, min(sw_months, 24 - sw_start + 1))
        effective_advisor_months = max(0, min(advisor_months, 24 - advisor_start + 1))
        effective_maintenance_months = max(0, min(maintenance_months, 24 - maintenance_start + 1))

        total_cost = (sw_cost * effective_sw_months) + (advisor_cost * effective_advisor_months) + (maintenance_cost * effective_maintenance_months)
        st.write(f"Custo total projetado para 24 meses: R$ {total_cost:,.2f}")
        st.session_state["total_cost"] = total_cost

        st.subheader("Projeção de Sellers e Receita")
        st.write("Preencha os parâmetros para a projeção de vendas (as vendas começam a partir de um determinado mês).")
        start_month = st.number_input("Mês de início das vendas:", value=7, step=1)
        initial_sellers = st.number_input("Número inicial de sellers no mês de início:", value=10, step=1)
        growth_rate = st.number_input("Taxa de crescimento mensal dos sellers (%):", value=10.0, step=0.1, format="%.2f")

        plan_prices = st.session_state.get("plan_prices", {"Starter":0, "Growth":0, "Enterprise":0})
        plan_shares = st.session_state.get("plan_shares", {"Starter":60.0, "Growth":30.0, "Enterprise":10.0})
        weighted_price = (plan_prices.get("Starter",0) * (plan_shares.get("Starter",0)/100) +
                          plan_prices.get("Growth",0) * (plan_shares.get("Growth",0)/100) +
                          plan_prices.get("Enterprise",0) * (plan_shares.get("Enterprise",0)/100))
        st.write(f"Preço médio ponderado dos planos: R$ {weighted_price:,.2f}")
        st.session_state["weighted_price"] = weighted_price

        st.markdown("---")
        st.write("**Simulação dos 24 meses:**")
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

        breakeven_month = None
        for idx, rev in enumerate(cumulative_revenues):
            if rev >= total_cost:
                breakeven_month = months[idx]
                break
        if breakeven_month:
            st.success(f"Breakeven alcançado no mês: {breakeven_month}")
        else:
            st.warning("Breakeven não alcançado em 24 meses.")
        st.session_state["breakeven_month"] = breakeven_month

        st.write(f"Taxa de Adoção (sellers que utilizarão o hub): {st.session_state.get('adoption_rate_latam', 1)}%")
        st.progress(int(st.session_state.get("adoption_rate_latam", 1)))

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
            "Você pode configurar planos de cobrança com variáveis ajustáveis, estimar o mercado (TAM, SAM com taxa de adoção e share dos planos) e "
            "analisar os custos operacionais e o breakeven da operação em 24 meses.\n\n"
            "Racional para estimativa de mercado:\n"
            "- **Cenário 1 (LATAM → EUA):** Consideramos um TAM de 500.000 sellers na América Latina. "
            "Utilizando uma taxa de adoção conservadora de 1%, o SAM (sellers que efetivamente utilizariam o hub) seria de aproximadamente 5.000 sellers.\n\n"
            "- **Cenário 2 (EUA/CHINA → LATAM):** Consideramos um TAM de 100.000 sellers dos EUA/CHINA para o mercado LATAM. "
            "Com uma taxa de adoção conservadora de 1%, o SAM seria de aproximadamente 1.000 sellers.\n\n"
            "Esses números foram adotados para uma visão mais pessimista, considerando barreiras operacionais, logísticas e regulatórias.\n\n"
            "Para os custos, além do valor e da quantidade de meses, foi considerada a data de início de cada custo, "
            "de forma que o custo só seja aplicado a partir do mês especificado."
        )

    #############################
    # Aba 5: Cenários Salvos
    #############################
    with tabs[4]:
        st.header("Cenários Salvos")
        st.write("Salve o cenário atual com um nome para consulta futura.")

        scenario_name = st.text_input("Nome do Cenário")
        if st.button("Salvar Cenário"):
            scenario_data = {
                "nome": scenario_name,
                "plan_prices": st.session_state.get("plan_prices", {}),
                "market": {
                    "TAM_LATAM_EUA": st.session_state.get("tam_latam_eua"),
                    "SAM_LATAM_EUA": st.session_state.get("sam_latam_eua"),
                    "TAM_EUA_CHINA_LATAM": st.session_state.get("tam_eua_china_latam"),
                    "SAM_EUA_CHINA_LATAM": st.session_state.get("sam_eua_china_latam"),
                    "Taxa Adoção LATAM": st.session_state.get("adoption_rate_latam"),
                    "Taxa Adoção EUA/CHINA": st.session_state.get("adoption_rate_eua_china"),
                    "Plan Shares": st.session_state.get("plan_shares")
                },
                "financial": {
                    "Custo Total": st.session_state.get("total_cost"),
                    "Breakeven Mês": st.session_state.get("breakeven_month"),
                    "Preço Médio Ponderado": st.session_state.get("weighted_price")
                }
            }
            scenarios_file = "saved_scenarios.json"
            if os.path.exists(scenarios_file):
                with open(scenarios_file, "r") as f:
                    saved_scenarios = json.load(f)
            else:
                saved_scenarios = {"scenarios": []}
            saved_scenarios["scenarios"].append(scenario_data)
            with open(scenarios_file, "w") as f:
                json.dump(saved_scenarios, f, indent=4)
            st.success(f"Cenário '{scenario_name}' salvo com sucesso!")

        st.markdown("---")
        st.header("Lista de Cenários Salvos")
        scenarios_file = "saved_scenarios.json"
        if os.path.exists(scenarios_file):
            with open(scenarios_file, "r") as f:
                saved_scenarios = json.load(f)
            if saved_scenarios["scenarios"]:
                for sc in saved_scenarios["scenarios"]:
                    st.subheader(sc["nome"])
                    st.write("**Planos:**", sc.get("plan_prices", {}))
                    st.write("**Market:**", sc.get("market", {}))
                    st.write("**Financial:**", sc.get("financial", {}))
                    st.markdown("---")
            else:
                st.info("Nenhum cenário salvo ainda.")
        else:
            st.info("Nenhum cenário salvo ainda.")

if __name__ == '__main__':
    main()





