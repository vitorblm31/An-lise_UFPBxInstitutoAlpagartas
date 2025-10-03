import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# ====================
# Configuração inicial
# ====================
st.set_page_config(page_title="Evolução do IDEB", page_icon="📊", layout="wide")
st.title("📊 Evolução do IDEB e Indicadores nos municípios da Paraíba")

# ====================
# Carregando os dados
# ====================
@st.cache_data
def load_data():
    # Usando caminho relativo para portabilidade
    df = pd.read_csv("IA (1).csv")
    for col in ["Instituições_20", "Projetos_20", "Beneficiados_20",
                "Instituições_23", "Projetos_23", "Beneficiados_23"]:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(" ", "")
            .str.replace(".", "", regex=False)
            .replace("nan", "0")
            .astype(float)
        )

    anos_ideb = [
        "IDEB_05", "IDEB_07", "IDEB_09", "IDEB_11", "IDEB_13",
        "IDEB_15", "IDEB_17", "IDEB_19", "IDEB_23"
    ]
    
    for col in anos_ideb:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    return df

df = load_data()
anos_ideb = [
    "IDEB_05", "IDEB_07", "IDEB_09", "IDEB_11", "IDEB_13",
    "IDEB_15", "IDEB_17", "IDEB_19", "IDEB_23"
]
anos = [col.replace("IDEB_", "") for col in anos_ideb]


# ====================
# Sidebar para filtros
# ====================
st.sidebar.header("⚙️ Filtros")
municipios = df["Município"].unique()
municipio = st.sidebar.selectbox("Selecione o município:", sorted(municipios))

# ====================
# Dados filtrados
# ====================
df_mun = df[df["Município"] == municipio]
df_ideb = df_mun[anos_ideb].iloc[0]


# ====================
# Tabs
# ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Evolução do IDEB", 
    "📌 Indicadores", 
    "📊 Comparações", 
    "🌍 Panorama Geral", 
    "🏆 Ranking de Evolução"
])

# ====================
# Tab 1 - Evolução do IDEB
# ====================
with tab1:
    st.subheader(f"Evolução do IDEB - {municipio}")

    df_plot = pd.DataFrame({
        "Ano": anos,
        "IDEB": df_ideb.values
    })

    chart = (
        alt.Chart(df_plot)
        .mark_line(point=True)
        .encode(
            x="Ano",
            y=alt.Y("IDEB", scale=alt.Scale(zero=False)),
            tooltip=["Ano", "IDEB"]
        )
        .properties(width=800, height=400)
    )

    st.altair_chart(chart, use_container_width=True)

# ====================
# Tab 2 - Indicadores
# ====================
with tab2:
    st.subheader("📌 Indicadores por ano")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 2020")
        st.metric("Instituições", int(df_mun["Instituições_20"].iloc[0]))
        st.metric("Projetos", int(df_mun["Projetos_20"].iloc[0]))
        st.metric("Beneficiados", int(df_mun["Beneficiados_20"].iloc[0]))

    with col2:
        st.markdown("### 📊 2023")
        st.metric("Instituições", int(df_mun["Instituições_23"].iloc[0]))
        st.metric("Projetos", int(df_mun["Projetos_23"].iloc[0]))
        st.metric("Beneficiados", int(df_mun["Beneficiados_23"].iloc[0]))

    # Resumo textual
    dif_projetos = int(df_mun["Projetos_23"].iloc[0] - df_mun["Projetos_20"].iloc[0])
    dif_benef = int(df_mun["Beneficiados_23"].iloc[0] - df_mun["Beneficiados_20"].iloc[0])

    st.markdown("---")
    if dif_projetos > 0:
        st.success(f"✅ O município **{municipio}** aumentou em **{dif_projetos} projetos** de 2020 para 2023.")
    elif dif_projetos < 0:
        st.error(f"❌ O município **{municipio}** teve **{abs(dif_projetos)} projetos a menos** em 2023 comparado a 2020.")
    else:
        st.info(f"ℹ️ O município **{municipio}** manteve o mesmo número de projetos entre 2020 e 2023.")

    if dif_benef > 0:
        st.success(f"✅ Houve crescimento de **{dif_benef} beneficiados** no mesmo período.")
    elif dif_benef < 0:
        st.error(f"❌ O número de beneficiados caiu em **{abs(dif_benef)}** no período.")
    else:
        st.info("ℹ️ O número de beneficiados se manteve estável.")

# ====================
# Tab 3 - Comparações
# ====================
with tab3:
    st.subheader("📊 Comparação entre municípios")

    mun_compare = st.multiselect("Selecione municípios para comparar:", sorted(municipios), default=[municipio])

    if len(mun_compare) > 0:
        df_compare = df[df["Município"].isin(mun_compare)]
        
        df_compare_plot = df_compare.melt(
            id_vars=['Município'],
            value_vars=anos_ideb,
            var_name='Ano_IDEB',
            value_name='IDEB'
        )
        df_compare_plot['Ano'] = df_compare_plot['Ano_IDEB'].str.replace('IDEB_', '')


        chart_compare = (
            alt.Chart(df_compare_plot)
            .mark_line(point=True)
            .encode(
                x="Ano",
                y=alt.Y("IDEB", scale=alt.Scale(zero=False)),
                color="Município",
                tooltip=["Município", "Ano", "IDEB"]
            )
            .properties(width=900, height=450)
        )

        st.altair_chart(chart_compare, use_container_width=True)

# ====================
# Tab 4 - Panorama Geral
# ====================
with tab4:
    st.subheader("📈 Evolução do IDEB em todos os municípios da Paraíba")

    df_long = df.melt(
        id_vars=['Município'],
        value_vars=anos_ideb,
        var_name='Ano_IDEB',
        value_name='IDEB'
    )
    df_long['Ano'] = df_long['Ano_IDEB'].str.replace('IDEB_', '')

    chart_geral = (
        alt.Chart(df_long)
        .mark_line()
        .encode(
            x='Ano:O',
            y=alt.Y('IDEB:Q', scale=alt.Scale(zero=False)),
            color='Município:N',
            tooltip=['Município', 'Ano', 'IDEB']
        )
        .properties(
            title="Evolução do IDEB por Município",
            width=900,
            height=500
        )
        .interactive()
    )

    st.altair_chart(chart_geral, use_container_width=True)

# ====================
# Tab 5 - Ranking de Evolução
# ====================
with tab5:
    st.subheader("🏆 Ranking de Evolução do IDEB (2005-2023)")
    st.markdown("Classificação baseada na variação percentual entre a primeira e a última nota do IDEB disponíveis para cada município.")

    # 1. Função para calcular a evolução
    def calcular_evolucao(row):
        ideb_vals = row[anos_ideb].dropna()
        if len(ideb_vals) < 2:
            return None, None, None
        
        ideb_inicial = ideb_vals.iloc[0]
        ideb_final = ideb_vals.iloc[-1]
        
        if ideb_inicial == 0:
            return ideb_inicial, ideb_final, np.inf
            
        evolucao = ((ideb_final - ideb_inicial) / ideb_inicial) * 100
        return ideb_inicial, ideb_final, evolucao

    # 2. Aplicar a função para criar o dataframe do ranking
    resultados = df.apply(calcular_evolucao, axis=1, result_type='expand')
    resultados.columns = ['IDEB Inicial', 'IDEB Final', 'Evolução (%)']
    
    df_ranking = pd.DataFrame({'Município': df['Município']})
    df_ranking = pd.concat([df_ranking, resultados], axis=1)
    df_ranking = df_ranking.dropna().sort_values(by='Evolução (%)', ascending=False)
    
    # 3. Função para classificar com os NOVOS PARÂMETROS
    def classificar_evolucao(percentual):
        if percentual > 50:
            return 'Excelente'
        elif 30 <= percentual <= 50:
            return 'Bom'
        elif 15 <= percentual < 30:
            return 'Razoável'
        else: # Abaixo de 15%
            return 'Ruim'
            
    df_ranking['Classificação'] = df_ranking['Evolução (%)'].apply(classificar_evolucao)

    # 4. Função para colorir a tabela
    def colorir_classificacao(val):
        color_map = {
            'Excelente': 'background-color: #28a745; color: white',
            'Bom': 'background-color: #17a2b8; color: white',
            'Razoável': 'background-color: #ffc107; color: black',
            'Ruim': 'background-color: #dc3545; color: white'
        }
        return color_map.get(val, '')

    # 5. Exibir a tabela estilizada
    st.dataframe(
        df_ranking.style.applymap(colorir_classificacao, subset=['Classificação'])
                         .format({'IDEB Inicial': '{:.2f}', 'IDEB Final': '{:.2f}', 'Evolução (%)': '{:.2f}%'}),
        use_container_width=True,
        height=600

    )
