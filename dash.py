import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *

#Consulta no banco de dados
query = "SELECT * FROM registro"

#carregar os dados MySQL
df = conexao(query)

#botão para atualização dos daddos
if st.button("Atualizar dados"):
    df = conexao(query)

# Menu Lateral
st.sidebar.header("Selecione a informação para gerar o gráfico")

#Seleção de colunas X
# Selectbox-> cria uma caixa de seleção na barra lateral
colunaX = st.sidebar.selectbox(
    "Eixo X",
    options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
    index = 0

)

colunaY = st.sidebar.selectbox(
    "Eixo Y",
    options=["umidade", "temperatura", "pressao", "altitude" "co2", "poeira"],
    index = 1

)

#Verificar se o atributo está sendo exibido no filtro

def filtros(atributo):
    return atributo in [colunaX, colunaY]

# Filtro e Range -> Slider
st.sidebar.header("Selecione o Filtro")

#temperatura
if filtros("temperatura"):
    temperatura_range = st.sidebar.slider(
        "Temperatura (ºC)",
        #Valor minimo
        min_value = float(df["temperatura"].min()),
        #valor maximo
        max_value = (df["temperatura"].max()),
        
        value = (float(df["temperatura"].min()), float(df["temperatura"].max())),
    
        step = 0.1    
    )

#altitude

if filtros("altitude"):
    altitude_range = st.sidebar.slider(
        "Altitude º",
        #Valor minimo
        min_value = float(df["altitude"].min()),
        #valor maximo
        max_value = (df["altitude"].max()),
        
        value = (float(df["altitude"].min()), float(df["altitude"].max())),
    
        step = 0.1    

    )

#umidade
if filtros("umidade"):
    umidade_range = st.sidebar.slider(
        "umidade",
        #Valor minimo
        min_value = float(df["umidade"].min()),
        #valor maximo
        max_value = (df["umidade"].max()),
        
        value = (float(df["umidade"].min()), float(df["umidade"].max())),
    
        step = 0.1    
    )


#pressao
if filtros("pressao"):
    pressao_range = st.sidebar.slider(
        "pressao",
        #Valor minimo
        min_value = float(df["pressao"].min()),
        #valor maximo
        max_value = (df["pressao"].max()),
        
        value = (float(df["pressao"].min()), float(df["pressao"].max())),
    
        step = 0.1    
    )

# poeira
if filtros("poeira"):
    poeira_range = st.sidebar.slider(
        "poeira",
        #Valor minimo
        min_value = float(df["poeira"].min()),
        #valor maximo
        max_value = (df["poeira"].max()),
        
        value = (float(df["poeira"].min()), float(df["poeira"].max())),
    
        step = 0.1    
    )

#CO2
if filtros("co2"):
    co2_range = st.sidebar.slider(
        "co2",
        #Valor minimo
        min_value = float(df["co2"].min()),
        #valor maximo
        max_value = (df["co2"].max()),
        
        value = (float(df["co2"].min()), float(df["co2"].max())),
    
        step = 0.1    
    )

df_selecionado = df.copy()
#cria uma cópia do df original

if filtros("temperatura"):
    df_selecionado = df_selecionado[
        (df_selecionado["temperatura"] >= temperatura_range[0]) &
        (df_selecionado["temperatura"] <= temperatura_range[1])
    ]
    
#umidade
if filtros("umidade"):
    df_selecionado = df_selecionado[
        (df_selecionado["umidade"] >= umidade_range[0]) &
        (df_selecionado["umidade"] <= umidade_range[1])
    ]

#poeira
if filtros("poeira"):
    df_selecionado = df_selecionado[
        (df_selecionado["poeira"] >= poeira_range[0]) &
        (df_selecionado["poeira"] <= poeira_range[1])
    ]

#co2
if filtros("co2"):
    df_selecionado = df_selecionado[
        (df_selecionado["co2"] >= co2_range[0]) &
        (df_selecionado["co2"] <= co2_range[1])
    ]

#altitude
if filtros("altitude"):
    df_selecionado = df_selecionado[
        (df_selecionado["altitude"] >= altitude_range[0]) &
        (df_selecionado["altitude"] <= altitude_range[1])
    ]

#pressao
if filtros("pressao"):
    df_selecionado = df_selecionado[
        (df_selecionado["pressao"] >= pressao_range[0]) &
        (df_selecionado["pressao"] <= pressao_range[1])
    ]

#graficos 
def Home():
    with st.expander("Tabela"):
        mostrarDados = st.multiselect(
            "Filtro: ",
            df_selecionado.columns,
            default = [],
            key = "showData_home"
        )

        if mostrarDados:
            st.write(df_selecionado[mostrarDados])
    
    if not df_selecionado.empty:
        media_umidade = df_selecionado["umidade"].mean()
        media_temperatura = df_selecionado["temperatura"].mean()
        media_co2 = df_selecionado["co2"].mean()

        media1, media2, media3 = st.columns(3 , gap="large")

        with media1:
            st.info("Média de registros de umidade", icon="☔")
            st.metric(label="Média", value=f"{media_umidade:.2f}")

        with media2:
            st.info("Média de registros de Temperatura", icon="☔")
            st.metric(label="Média", value=f"{media_temperatura:.2f}")

        with media3:
            st.info("Média de registros de co2", icon="☔")
            st.metric(label="Média", value=f"{media_co2:.2f}")

        st.markdown("""----------""")

# graficos
def graficos():
    st.title("Dashboard Monitoramento")

    aba1, = st.tabs(["Gráfico de Linha"])

    with aba1:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponivel para gerar o gráfico")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente, para os eixos X e Y.")
            return
        
        try:
            grupo_dados1 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name="contagem")
            
            fig_valores = px.bar(
                grupo_dados1,
                x = colunaX,
                y = "contagem",
                orientation = "h",
                title =(f"Contagem de Registros por {colunaX.capitalize()}"),
                color_discrete_sequence=["#0083b8"],
                template= "plotly_white"
            )

        except Exception as e:
            st.error(f"Erro ao criar gráfico de linha: {e} ")
            
            st.plotly_chart(fig_valores, use_container_width=True)

Home()
graficos()