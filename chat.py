#Utilitario de conexión a Azure OpenAI
from langchain_openai import AzureChatOpenAI

#Utilitario para crear una conversación de chat con el modelo
from langchain.chains import ConversationChain

#Utilitario para crear la memoria a corto plazo del modelo
from langchain.memory import ConversationBufferMemory

from dotenv import load_dotenv
import os

load_dotenv()

# Leer variables del entorno
CONF_API_VERSION = os.getenv("CONF_API_VERSION")
CONF_AZURE_ENDPOINT = os.getenv("CONF_AZURE_ENDPOINT")
CONF_AZURE_API_KEY = os.getenv("CONF_AZURE_API_KEY")
CONF_AZURE_DEPLOYMENT = os.getenv("CONF_AZURE_DEPLOYMENT")


def obtenerModelo():
    #Conectamos modelito
    llm=AzureChatOpenAI(
        api_version=CONF_API_VERSION,
        azure_endpoint=CONF_AZURE_ENDPOINT,
        api_key=CONF_AZURE_API_KEY,
        azure_deployment=CONF_AZURE_DEPLOYMENT,
    )
    return llm

def abrirSesionChat(
    llm = None,
    contexto = None
):

    #Creando la memoria a corto plazo
    memoria = ConversationBufferMemory()
    
    #Agregando la personalidad (contexto)
    memoria.chat_memory.add_ai_message(contexto)
    
    #Creando la conversasion de chat
    chat = ConversationChain(
        llm=llm,
        memory=memoria,
        verbose=False #Desactivamos el log
    )
    return chat

def enviarMensaje(
    chat = None,
    mensaje = None
):
    #Enviando el mensaje
    respuesta = chat.predict(input=mensaje)
    
    return respuesta
    