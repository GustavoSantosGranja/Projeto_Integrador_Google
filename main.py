from datetime import datetime, timezone
from flask import Flask, Response, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json
import paho.mqtt.client as mqtt

#pip install paho-mqtt flask -> Conexão com os sensores 

#Conexão com o Banco de Dados
app = Flask("registro")
#A conexão com o banco havera modificações na base de dados
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senai%40134@127.0.0.1/bd_medidor'

#criar uma instancia do SQLAlchemy, passando a aplicação do flask como Parametro
#
mybd = SQLAlchemy(app)

# Conexão Dos Sensores
mqtt_dados = {}

def conexao_sensor(cliente, rc):
    cliente.subscribe("projeto_integrado/SENAI134/Cienciadedados/GrupoX")

def msg_sensor(msg):
    global mqtt_dados
    #Decodificar a mensagem recebida de bytes para string
    valor = msg.payload.decode('utf-8')
    #decodificar de string para JSON
    mqtt_dados = json.loads(valor)
    
    print(f"Mensagem Recebida: {mqtt_dados}")

    with app.app_context():
        try:
            temperatura = mqtt_dados.get('temperature'),
            pressao = mqtt_dados.get('pressure'),
            altitude = mqtt_dados.get('altitude'),
            umidade = mqtt_dados.get('humidity'),
            co2 = mqtt_dados.get('co2'),
            poeira = 0,
            tempo_registro = mqtt_dados.get('timestamp')

            if tempo_registro is None:
                print("Timestamp não encontrado")
                return
            
            try:
                tempo_oficial = datetime.fromtimestamp(int(tempo_registro), tz=timezone.utc)

            except (ValueError, TypeError) as e:
                print(f"Erro ao converter timestamp: {str(e)}")
                return
            
#Criar objeto que vai simular a tabela 

            novos_dados = Registro(
                temperaturaV = temperatura,
                pressaoV = pressao,
                altitudeV = altitude,
                umidadeV = umidade,
                co2V = co2,
                poeiraV = poeira,
                tempo_registro = tempo_oficial

            )

            #adicionar novo registro

            mybd.session.add(novos_dados)
            mybd.session.commit()
            print("Dados Foram inseridos com sucesso no Banco de Dados!!!")

        except Exception as e:
            print(f"Erro ao processar os dados do MQTT: {str(e)}")
            mybd.session.rollback()

mqtt_client = mqtt.Client()
mqtt_client.on_connect = conexao_sensor
mqtt_client.on_message = msg_sensor
mqtt_client.connect("test.mosquitto.org", 1833, 60)

def start_mqtt():
    mqtt_client.loop_start()