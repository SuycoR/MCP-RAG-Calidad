from flask import Flask, request, jsonify
import json
from chat import obtenerModelo, abrirSesionChat, enviarMensaje
from datetime import datetime

app = Flask(__name__)

llm = obtenerModelo()
contexto = "Eres un auditor que clasifica commits en tres categorías: vago, ambiguo o documentado. Analiza los archivos modificados y la descripción."
chat = abrirSesionChat(llm, contexto)

@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.get_json()

    # Muestra un pequeño mensaje en la terminal
    print("📦 Webhook recibido y guardado en archivo.")

    # Guarda el JSON recibido en un archivo de texto
    with open("webhook_log.txt", "a", encoding="utf-8") as f:
        f.write("\n\n--- Webhook recibido ---\n")
        f.write(f"Fecha: {datetime.now()}\n")
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
        f.write("\n--------------------------\n")

    # Ejemplo opcional: detectar un push
    if "pusher" in data:
        print(f"🚀 Push realizado por: {data['pusher']['name']}")
       
    commits = data.get("commits", [])
    resultados = []
    if not commits:
        return jsonify({"status": "no commits found"}), 400
        
    for commit in commits:
        mensaje = str(commit)
        respuesta = enviarMensaje(chat, mensaje)
        resultados.append({"commit": commit, "evaluacion": respuesta})

    return jsonify({"status": "ok","resultados":resultados}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
