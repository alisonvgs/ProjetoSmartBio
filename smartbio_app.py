import streamlit as st
import time
import pandas as pd
import plotly.express as px
from ProjetoSmartBio.app import predizer_imagem
from ProjetoSmartBio.llm import llm_com_llama3

if "page" not in st.session_state:
    st.session_state.page = "home"

if "energia_total" not in st.session_state:
    st.session_state.energia_total = 0.0
# Inicialização dos históricos no session_state
if "materiais_usados" not in st.session_state:
    st.session_state.materiais_usados = {}

if "consumo_energia" not in st.session_state:
    st.session_state.consumo_energia = {
        "Carro elétrico": 0,
        "Geração de pães": 0,
        "Autoconsumo": 0
    }

def navegar_para(pagina):
    st.session_state.page = pagina



def mostrar_circulos(etapas):
    cores = {
        "pendente": "#d3d3d3",  # cinza
        "ativo": "#90ee90",     # verde claro
        "concluido": "#006400"  # verde escuro
    }
    estados = ["pendente"] * len(etapas)
    placeholder = st.empty()

    for i in range(len(etapas) + 1):
        for idx in range(len(etapas)):
            if idx < i-1:
                estados[idx] = "concluido"
            elif idx == i-1:
                estados[idx] = "ativo"
            else:
                estados[idx] = "pendente"

        with placeholder.container():
            cols = st.columns(len(etapas))
            for i_col, col in enumerate(cols):
                cor = cores[estados[i_col]]
                estilo = "font-weight: bold; color: black;" if estados[i_col] != "pendente" else "color: grey;"
                col.markdown(f"""
                    <div style='text-align: center;'>
                        <div style='width: 90px; height: 90px; background-color: {cor};
                            border-radius: 50%; margin: auto; border: 2px solid #555;'></div>
                        <div style='{estilo}'>{etapas[i_col]}</div>
                    </div>
                """, unsafe_allow_html=True)
        time.sleep(2)

    # Garantir que todas as etapas fiquem como concluídas no final
    estados = ["concluido"] * len(etapas)
    with placeholder.container():
        cols = st.columns(len(etapas))
        for i_col, col in enumerate(cols):
            cor = cores[estados[i_col]]
            estilo = "font-weight: bold; color: black;"
            col.markdown(f"""
                <div style='text-align: center;'>
                    <div style='width: 90px; height: 90px; background-color: {cor};
                        border-radius: 50%; margin: auto; border: 2px solid #555;'></div>
                    <div style='{estilo}'>{etapas[i_col]}</div>
                </div>
            """, unsafe_allow_html=True)

def tela_inicial():
    st.markdown("""
        <style>
            body { background-color: #e6ffe6; }
            .stButton > button {
                padding: 20px 40px; font-size: 20px;
                background-color: #2e8b57; color: white;
                border-radius: 10px; border: none; font-weight: bold;
            }
            .stButton > button:hover { background-color: #246b45; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: green;'>SMARTBIO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>O que deseja fazer hoje?</h3>", unsafe_allow_html=True)

    # Bateria visual
    nivel_bateria = min(st.session_state.energia_total / 10.0, 1.0)  # assume 10kWh como carga total
    largura_total = 300
    altura = 50
    largura_carregada = int(largura_total * nivel_bateria)
    cor = "#2e8b57" if nivel_bateria > 0.2 else "#ff4d4d"  # verde se carregada, vermelho se vazia

   

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Produzir Energia"):
            navegar_para("producao")
    with col2:
        if st.button("Utilizar Energia"):
            navegar_para("utilizar")
    with col3:
        if st.button("Painel"):
            navegar_para("painel")

    st.markdown(f"""
            <div style="text-align: center; margin-top: 30px;">
                <div style="width: {largura_total}px; height: {altura}px; border: 2px solid #555; border-radius: 5px; display: inline-block; position: relative;">
                    <div style="width: {largura_carregada}px; height: 100%; background-color: {cor}; border-radius: 5px 0 0 5px;"></div>
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: blak;">
                        {round(st.session_state.energia_total, 2)} kWh
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def producao_energia():
    st.markdown("<h2 style='text-align: center; color: green;'>🔋 SMARTBIO - Produção de Energia</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("🧪 Análise de resíduo para produção de energia")

    if "resultado" not in st.session_state:
        st.session_state.resultado = None
    if "avaliacao_llm" not in st.session_state:
        st.session_state.avaliacao_llm = None
    if "confirmado" not in st.session_state:
        st.session_state.confirmado = False
    if "processado" not in st.session_state:
        st.session_state.processado = False
    if "quantidade_kg" not in st.session_state:
        st.session_state.quantidade_kg = 5.0  # Exemplo fixo, ou peça ao usuário
    if "energia_gerada" not in st.session_state:
        st.session_state.energia_gerada = None

    # Ocultar upload e análise se já está processando
    if not st.session_state.confirmado and not st.session_state.processado:
        arq = st.file_uploader("📷 Envie a imagem do resíduo", type=["jpg", "png", "jpeg"])

        if arq and not st.session_state.resultado:
            st.image(arq, caption="Imagem enviada", use_column_width=True)

            resultado = predizer_imagem(arq)
            st.session_state.resultado = resultado

            prompt = f"""O objeto detectado é um {resultado}. Você é um especialista em energia de biogás, com conhecimento profundo sobre biodigestores, digestão anaeróbia e os tipos de substratos utilizados na produção de biogás. Avalie se este material é adequado para produção de biogás, considerando teor de matéria orgânica, biodegradabilidade, relação C/N e potencial de produção de metano. Seja curto na sua resposta. Responda em português técnico e claro."""

            with st.spinner("🔍 Analisando viabilidade do resíduo..."):
                avaliacao = llm_com_llama3(prompt)
                st.session_state.avaliacao_llm = avaliacao

    if st.session_state.resultado and not st.session_state.confirmado and not st.session_state.processado:
        st.success(f"✅ Objeto identificado: **{st.session_state.resultado}**")
        st.markdown("### 🧠 Avaliação do Especialista:")
        st.write(st.session_state.avaliacao_llm)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Confirmar material"):
                st.session_state.confirmado = True
                st.rerun()
        with col2:
            if st.button("🔄 Inserir outro produto"):
                for chave in ["resultado", "avaliacao_llm", "confirmado", "processado", "energia_gerada"]:
                    st.session_state[chave] = None
                    st.rerun()

    if st.session_state.confirmado and not st.session_state.processado:
        etapas = [f"Pesando {st.session_state.resultado}", "Triturando", f"Decompondo {st.session_state.resultado}"]
        mostrar_circulos(etapas)

        # Cálculo fictício da energia gerada
        st.session_state.energia_gerada = round(st.session_state.quantidade_kg * 0.65, 2)  # 0.65 kWh por kg (exemplo)
        st.session_state.energia_total += st.session_state.energia_gerada
        # Registro do material usado
        material = st.session_state.resultado
        if material in st.session_state.materiais_usados:
            st.session_state.materiais_usados[material] += st.session_state.quantidade_kg
        else:
            st.session_state.materiais_usados[material] = st.session_state.quantidade_kg

        st.session_state.processado = True

    if st.session_state.processado:
        st.success("✅ Processo concluído com sucesso!")
        st.markdown(f"""
            <div style='font-size: 20px; text-align: center; margin-top: 20px;'>
                A quantidade de <strong>{st.session_state.quantidade_kg} kg</strong> de 
                <strong>{st.session_state.resultado}</strong> gerou aproximadamente 
                <strong>{st.session_state.energia_gerada} kWh</strong> de energia! ⚡️
            </div>
        """, unsafe_allow_html=True)

        st.markdown("###")
        if st.button("🏠 Voltar ao menu"):
            for chave in ["resultado", "avaliacao_llm", "confirmado", "processado", "energia_gerada"]:
                st.session_state[chave] = None
            navegar_para("home")
            st.rerun()


def utilizar_energia():
    st.markdown("<h2 style='text-align: center; color: green;'>⚡ Utilizar Energia</h2>", unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.energia_total <= 0:
        st.warning("🔋 Nenhuma energia disponível no momento. Por favor, produza energia primeiro.")
        if st.button("Produzir Energia"):
            navegar_para("producao")
            st.rerun()
        elif st.button("🏠 Voltar ao menu"):
            navegar_para("home")
            st.rerun()
        return

    opcoes = ["Selecione uma opção...", "Carregar carro elétrico", "Geração de pães", "Autoconsumo de uma casa"]
    escolha = st.selectbox("Escolha uma aplicação para a energia:", opcoes)

    if escolha != "Selecione uma opção...":
        st.subheader("🔍 Pré-visualização do uso da energia:")

        energia_disponivel = st.session_state.energia_total
        mensagem = ""

        if escolha == "Carregar carro elétrico":
            km = round(energia_disponivel / 0.15, 1)
            mensagem = f"🔋 Energia disponível: **{energia_disponivel} kWh**\n\n🚗 Isso fornecerá aproximadamente **{km} km** de autonomia para um carro elétrico."
        elif escolha == "Geração de pães":
            paes = int(energia_disponivel / 0.05)
            mensagem = f"🔋 Energia disponível: **{energia_disponivel} kWh**\n\n🍞 Isso permitirá produzir cerca de **{paes} pães**."
        elif escolha == "Autoconsumo de uma casa":
            dias = round(energia_disponivel / 8.0, 1)
            mensagem = f"🔋 Energia disponível: **{energia_disponivel} kWh**\n\n🏠 Isso mantém uma casa funcionando por aproximadamente **{dias} dias**."

        st.info(mensagem)

        if st.button("⚡ Confirmar e Utilizar Energia"):
            if escolha == "Carregar carro elétrico":
                st.session_state.consumo_energia["Carro elétrico"] += energia_disponivel
            elif escolha == "Geração de pães":
                st.session_state.consumo_energia["Geração de pães"] += energia_disponivel
            elif escolha == "Autoconsumo de uma casa":
                st.session_state.consumo_energia["Autoconsumo"] += energia_disponivel

            st.success(mensagem.replace("🔋 Energia disponível:", "✅ Energia utilizada:"))

            st.session_state.energia_total = 0.0

            if st.button("🏠 Voltar ao menu"):
                navegar_para("home")
                st.rerun()
    else:
        st.info("🔽 Selecione uma opção para visualizar como sua energia será utilizada.")



def painel():
    st.markdown("<h2 style='text-align: center; color: green;'>📊 Painel de Energia</h2>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Materiais Utilizados na Produção")
        if st.session_state.materiais_usados:
            df_materiais = pd.DataFrame.from_dict(st.session_state.materiais_usados, orient='index', columns=['Quantidade (kg)'])
            fig_materiais = px.bar(df_materiais, x=df_materiais.index, y='Quantidade (kg)', color=df_materiais.index, title="Produção de Energia")
            st.plotly_chart(fig_materiais, use_container_width=True)
        else:
            st.info("Nenhum material foi utilizado ainda.")

    with col2:
        st.markdown("###  Forma do Consumo de Energia")
        if any(v > 0 for v in st.session_state.consumo_energia.values()):
            df_consumo = pd.DataFrame.from_dict(st.session_state.consumo_energia, orient='index', columns=['Energia usada (kWh)'])
            fig_consumo = px.bar(df_consumo, x=df_consumo.index, y='Energia usada (kWh)', color=df_consumo.index, title="Consumo de Energia")
            st.plotly_chart(fig_consumo, use_container_width=True)
        else:
            st.info("A energia ainda não foi consumida.")

        if st.button("🏠 Voltar ao menu"):
                navegar_para("home")
                st.rerun()


if st.session_state.page == "producao":
    producao_energia()
elif st.session_state.page == "utilizar":
    utilizar_energia()
elif st.session_state.page == "painel":
    painel()
else:
    tela_inicial()
