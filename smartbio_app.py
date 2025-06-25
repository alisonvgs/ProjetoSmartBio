import streamlit as st
import time
import pandas as pd
import plotly.express as px
from app import predizer_imagem
from llm import llm_com_llama3

st.set_page_config(
    page_title="SMARTBIO",
    page_icon="mascote.jpg",  # Caminho para a imagem
    menu_items={
        'Get Help': 'https://www.smartbio.com.br/',
        'Report a bug': 'https://www.smartbio.com.br/',
        'About': "Developed by SmartBio LTDA."
    }
)
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
if "feedback" not in st.session_state:
    st.session_state.feedback = []


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

import streamlit as st
import base64

def carregar_mascote_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        b64_bytes = base64.b64encode(img_file.read())
        return b64_bytes.decode()

def tela_inicial():
    mascote_b64 = carregar_mascote_base64("mascote.jpg")

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

    st.markdown(f"""
        <h1 style='text-align: center; color: green;'>
            <img src="data:image/jpg;base64,{mascote_b64}" 
                 style='height: 80px; vertical-align: middle; margin-right: 10px;'/>
            SMARTBIO
        </h1>
    """, unsafe_allow_html=True)

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
                <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: black;">
                    {round(st.session_state.energia_total, 2)} kWh
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def producao_energia():
    st.markdown(
        "<h2 style='text-align: center; color: green;'>🔋 SMARTBIO - Produção de Energia</h2>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.subheader("🧪 Análise de resíduo para produção de energia")

    # --- Inicialização de estados ---
    if "quantidade_kg" not in st.session_state:
        st.session_state.quantidade_kg = 5.0
    if "energia_total" not in st.session_state:
        st.session_state.energia_total = 0.0
    if "materiais_usados" not in st.session_state:
        st.session_state.materiais_usados = {}
    if "feedback" not in st.session_state:
        st.session_state.feedback = []
    if "residuos" not in st.session_state:
        st.session_state.residuos = []
    if "arquivos_processados" not in st.session_state:
        st.session_state.arquivos_processados = set()
    if "indice_atual" not in st.session_state:
        st.session_state.indice_atual = 0
    if "mostrar_upload" not in st.session_state:
        st.session_state.mostrar_upload = True

    # **Resetar mostrar_upload para True se não houver resíduos (início novo)**
    if not st.session_state.residuos:
        st.session_state.mostrar_upload = True


    # --- Upload e pré-processamento múltiplo ---
    uploaded_files = None
    if st.session_state.mostrar_upload:
        uploaded_files = st.file_uploader(
            "📷 Envie uma ou mais imagens do resíduo",
            accept_multiple_files=True,
            type=["png", "jpg", "jpeg", "gif", "bmp", "webp"]
        )

    if uploaded_files:
        novos = [f for f in uploaded_files
                 if f.name not in st.session_state.arquivos_processados]
        for f in novos:
            mat = predizer_imagem(f)
            prompt = f"O objeto detectado é um {mat}. Você é um especialista em energia de biogás… seja sucinto sobre o material dando destaque sobre se é bom ou ruim para um biogas"
            with st.spinner(f"🔍 Analisando viabilidade: {mat}"):
                ava = llm_com_llama3(prompt)

            st.session_state.residuos.append({
                "nome": f.name,
                "imagem": f,
                "material": mat,
                "avaliacao": ava,
                "processado": False,
                "energia": 0.0
            })
            st.session_state.arquivos_processados.add(f.name)

        if novos:
            st.session_state.indice_atual = 0
            st.session_state.mostrar_upload = False
            st.rerun()

    # --- Fluxo para cada resíduo ---
    if st.session_state.indice_atual < len(st.session_state.residuos):
        item = st.session_state.residuos[st.session_state.indice_atual]

        st.image(item["imagem"], use_container_width=True, caption=item["nome"])
        st.success(f"🔍 Identificado como: **{item['material']}**")
        st.markdown("### 🧠 Avaliação do Especialista:")
        st.write(item["avaliacao"])

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Confirmar e avançar"):
                energia = round(st.session_state.quantidade_kg * 0.65, 2)
                item["energia"] = energia
                item["processado"] = True
                st.session_state.energia_total += energia
                st.session_state.materiais_usados.setdefault(
                    item["material"], 0.0
                )
                st.session_state.materiais_usados[item["material"]] += st.session_state.quantidade_kg

                st.session_state.indice_atual += 1
                st.rerun()

        with c2:
            if st.button("❌ Rejeitar e avançar"):
                st.session_state.indice_atual += 1
                st.rerun()

    # --- Quando terminar a lista ---
    elif st.session_state.residuos:
        st.success("🎉 Todos os materiais passaram pelo fluxo!")

        if "mostrar_animacao" not in st.session_state:
            st.session_state.mostrar_animacao = True

        if st.session_state.mostrar_animacao:
            placeholder_animacao = st.empty()
            with placeholder_animacao:
                mostrar_circulos(["Análise", "Processamento", "Geração", "Resumo", "Feedback"])
            placeholder_animacao.empty()  # Oculta os círculos
            st.session_state.mostrar_animacao = False  # Desativa para não repetir após feedback
            st.rerun()

        st.markdown("## ⚡ Resumo de Energia Produzida:")
        for item in st.session_state.residuos:
            if item["processado"]:
                st.markdown(f"**🧾 {item['material']}** — {item['energia']} kWh")

        st.markdown("## 🧠 Feedback por Material:")
        feedbacks_temp = []

        for idx, item in enumerate(st.session_state.residuos):
            if item["processado"]:
                with st.expander(f"💬 Feedback para: {item['material']} ({item['nome']})", expanded=True):
                    st.image(item["imagem"], width=200)
                    likert = [
                        "1 - Muito imprecisa", "2 - Imprecisa",
                        "3 - Neutra", "4 - Precisa", "5 - Muito precisa"
                    ]
                    pes_fb = st.radio(
                        f"📏 A pesagem de **{item['material']}** pareceu correta?",
                        likert, index=2, key=f"pes_{idx}"
                    )
                    eng_fb = st.radio(
                        f"⚡ A energia estimada ({item['energia']} kWh) pareceu correta?",
                        likert, index=2, key=f"eng_{idx}"
                    )
                    com = st.text_area(f"💡 Comentários para {item['material']}:", key=f"com_{idx}")

                    feedbacks_temp.append({
                        "material": item["material"],
                        "quantidade_kg": st.session_state.quantidade_kg,
                        "energia_gerada_kWh": item["energia"],
                        "pesagem_feedback": pes_fb,
                        "energia_feedback": eng_fb,
                        "comentario": com
                    })

        if st.button("💾 Enviar Feedbacks e Voltar"):
            st.session_state.feedback.extend(feedbacks_temp)
            # Resetar tudo e voltar ao menu
            st.session_state.residuos = []
            st.session_state.arquivos_processados = set()
            st.session_state.indice_atual = 0
            st.session_state.mostrar_upload = False
            st.session_state.mostrar_animacao = True  # Reativa apenas quando voltar ao fluxo
            navegar_para("home")
            st.rerun()


        if st.button("➕ Adicionar novo material"):
            st.session_state.mostrar_upload = True
            st.session_state.indice_atual = len(st.session_state.residuos)
            st.rerun()

    # --- Botão de saída a qualquer momento ---
    if st.button("🏠 Voltar ao menu"):
        st.session_state.residuos = []
        st.session_state.arquivos_processados = set()
        st.session_state.indice_atual = 0
        st.session_state.mostrar_upload = False
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
    st.markdown("<h2 style='text-align: center; color: green;'>📊 Painel de Energia e Feedback</h2>", unsafe_allow_html=True)
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
        st.markdown("### Consumo de Energia")
        if any(v > 0 for v in st.session_state.consumo_energia.values()):
            df_consumo = pd.DataFrame.from_dict(st.session_state.consumo_energia, orient='index', columns=['Energia usada (kWh)'])
            fig_consumo = px.bar(df_consumo, x=df_consumo.index, y='Energia usada (kWh)', color=df_consumo.index, title="Consumo de Energia")
            st.plotly_chart(fig_consumo, use_container_width=True)
        else:
            st.info("A energia ainda não foi consumida.")

    st.markdown("---")
    st.subheader("📝 Feedback dos Usuários")
    if st.session_state.feedback:
        df_feedback = pd.DataFrame(st.session_state.feedback)
        st.dataframe(df_feedback)

        likert_order = [
            "1 - Muito imprecisa",
            "2 - Imprecisa",
            "3 - Neutra",
            "4 - Precisa",
            "5 - Muito precisa"
        ]

        pesagem_counts = df_feedback["pesagem_feedback"].value_counts().reindex(likert_order, fill_value=0)
        energia_counts = df_feedback["energia_feedback"].value_counts().reindex(likert_order, fill_value=0)

        fig_pesagem = px.bar(
            pesagem_counts,
            x=pesagem_counts.values,
            y=pesagem_counts.index,
            orientation="h",
            labels={"y": "Avaliação", "x": "Quantidade"},
            title="📏 Avaliação da Precisão da Pesagem"
        )
        st.plotly_chart(fig_pesagem, use_container_width=True)

        fig_energia = px.bar(
            energia_counts,
            x=energia_counts.values,
            y=energia_counts.index,
            orientation="h",
            labels={"y": "Avaliação", "x": "Quantidade"},
            title="⚡ Avaliação da Precisão da Energia Gerada"
        )
        st.plotly_chart(fig_energia, use_container_width=True)

    else:
        st.info("Ainda não há feedback coletado.")

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