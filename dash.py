import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *
import smtplib
import email.message
# python -m streamlit run dash.py
#Consulta no banco de dados
query = "SELECT * FROM registro"

#carregar os dados MySQL
df = conexao(query)

#botão para atualização dos daddos
if st.button("Atualizar dados"):
    df = conexao(query)


df['tempo_registro'] = pd.to_datetime(df['tempo_registro'])

# Menu Lateral
st.sidebar.header("Selecione a informação para gerar o gráfico")

#Seleção de colunas X
# Selectbox-> cria uma caixa de seleção na barra lateral
colunaX = st.sidebar.selectbox(
    "Eixo X",
    options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira", "tempo_registro"],
    index = 0

)

colunaY = st.sidebar.selectbox(
    "Eixo Y",
    options=["umidade", "temperatura", "pressao", "altitude" ,"co2", "poeira", "tempo_registro"],
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


if filtros("tempo_registro"):
    # Converter os valores mínimo e máximo para timestamp
    min_timestamp = df["tempo_registro"].min().timestamp()
    max_timestamp = df["tempo_registro"].max().timestamp()
    
    tempo_registro_range = st.sidebar.slider(
        "Tempo Registro",
        min_value=min_timestamp,  # Valor Mínimo como timestamp.
        max_value=max_timestamp,  # Valor Máximo como timestamp.
        value=(min_timestamp, max_timestamp),  # Faixa de Valores selecionado.
        format= "Data"  # Formato de exibição
    )
    # Converter o range de volta para datetime
    tempo_registro_range = (pd.to_datetime(tempo_registro_range[0], unit='s'),
                            pd.to_datetime(tempo_registro_range[1], unit='s'))
    


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

if filtros("tempo_registro"):
    df_selecionado = df_selecionado[
        (df_selecionado["tempo_registro"] >= tempo_registro_range[0]) &
        (df_selecionado["tempo_registro"] <= tempo_registro_range[1])
    ] 

# Gráficos
def Home():
    with st.expander("Tabela"):
        mostrarDados = st.multiselect(
            "Filtro: ",
            df_selecionado.columns,
            default= [],
            key="showData_home"
        )

        if mostrarDados:
            st.write(df_selecionado[mostrarDados])


    # Calculos estatisticos
    if not df_selecionado.empty:
        media_umidade = df_selecionado["umidade"].mean()
        media_temperatura = df_selecionado["temperatura"].mean()
        media_co2 = df_selecionado["co2"].mean()
        

        media1, media2, media3 = st.columns(3, gap="large")

        with media1:
            st.info("Média de Registros de Umidade", icon='🌧️')
            st.metric(label="Média", value=f"{media_umidade:.2f}")

        with media2:
            st.info("Média de Registros de Temperatura", icon='🌡️')
            st.metric(label="Média", value=f"{media_temperatura:.2f}")

        with media3:
            st.info("Média de Registros do C02", icon='🌿')
            st.metric(label="Média", value=f"{media_co2:.2f}")

        st.markdown("""------------""")

def enviar_email():
    temperaturas_fora_do_range = df["temperatura"][(df["temperatura"].lt(21)) | (df["temperatura"].gt(24))]

    # Verifica se há temperaturas fora do intervalo e adiciona ao corpo do e-mail
    if not temperaturas_fora_do_range.empty:
        temperaturas_texto = ", ".join(str(temp) for temp in temperaturas_fora_do_range)
        corpo_email = f"""
        <p>Alerta de Temperatura</p>   
        <p>A temperatura está fora dos parâmetros devidos dentro do DataCenter.</p>
        <p>Com base nos valores fora do intervalo permitido (21-24°C). A temperatura atual é de: {temperaturas_texto}</p>
        """

        msg = email.message.Message()
        msg["Subject"] = "Alerta de Temperatura"
        msg["From"] = 'integradorp664@gmail.com'
        msg["To"] = 'gustavosgranja30@gmail.com'
        password = 'wgzqiurceaqrtlis'
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        try:
            s = smtplib.SMTP('smtp.gmail.com: 587')
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            s.quit()
            st.success('Email Enviado com sucesso!')
        except Exception as e:
            st.error(f'Erro ao enviar email: {e}')


#graficos 
def graficos():
    st.title("Dashboard Monitoramento")
       
    aba1, aba2, aba3, aba4  = st.tabs(
        ["Gráfico de Barras",
        "Gráfico de Linhas",
        "Gráfico de Dispersão",
        "Gráfico Mapa de Calor"]
        )
    
    with aba1:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return
        
        try:           
            grupo_dados1 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name="contagem")
            fig_valores = px.bar(
                grupo_dados1,       # De onde vem os dados.
                x = colunaX,        # Eixo X
                y = "contagem",     # Eixo Y com o nome que nós renomeamos no GrupBy
                orientation = "v",  # Orientação do Gráfico
                title = f"Contagem de Registros por {colunaX.capitalize()}", # Titulo do gráfico => A função capitalize() deixa tudo em maiúsculo. 
                color_discrete_sequence = ["#0083b9"],       # Altera a cor 
                template = "plotly_white"
            )
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico de barras:  {e}")
        st.plotly_chart(fig_valores, use_container_width=True)

    with aba2:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return

        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return

        try:
            grupo_dados2 = df_selecionado.groupby(by=[colunaX])[colunaY].mean().reset_index(name=colunaY)
            fig_valores2 = px.line(
                grupo_dados2,
                x=colunaX,
                y=colunaY,
                title=f"Gráfico de Linhas: {colunaX.capitalize()} vs {colunaY.capitalize()}",
                line_shape='linear',  # Tipo de linha
                markers=True  # Para mostrar marcadores nos pontos
            )
        except Exception as e:
            st.error(f"Erro ao criar gráfico de linhas: {e}")
        st.plotly_chart(fig_valores2, use_container_width=True)
 
    with aba3:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return

        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return

        try:
            grupo_dados3 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name=colunaY)
            fig_valores3 = px.scatter(grupo_dados3, x = colunaX, y = colunaY)    
            
            st.plotly_chart(fig_valores3, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao criar gráfico de disperção: {e}")
    
    with aba4:
        if df_selecionado.empty:
            st.write("Nenhum dado está disponível para gerar gráficos")
            return
        
        if colunaX == colunaY:
            st.warning("Selecione uma opção diferente para os eixos X e Y")
            return
        
        try:
            # Agrupando os dados para criar o mapa de calor
            grupo_dados4 = df_selecionado.groupby([colunaX, colunaY]).size().reset_index(name='contagem')
            # Criando o mapa de calor
            fig_valores4 = px.density_heatmap(
                grupo_dados4,
                x=colunaX,
                y=colunaY,
                z='contagem',
                title=f"Mapa de Calor: {colunaX.capitalize()} vs {colunaY.capitalize()}",
                color_continuous_scale='Viridis'  # Alterar a escala de cores se desejado
            )
            st.plotly_chart(fig_valores4, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao criar o mapa de calor: {e}")


enviar_email()
Home()
graficos()

