from flask import Flask, render_template, request, jsonify
import serial

app = Flask(__name__) #Cambio por variable automática "name" para que busque el archivo en la ubicación actual

# Configuración RS232 UART
ser = serial.Serial('/dev/serial0', 9600, timeout=1) # Serial0 funciona de manera universa. Se puede cambiar por ttyS0 en caso de escoger UART

prendas = [
    {"nombre":"Camisa1","tipo":"T-Shirt","color":"Negro","tela":"Algodon","talla":"M","fit":"Regular","perchero":1,"posicion":1},
    {"nombre":"Pantalon1","tipo":"Pantalon","color":"Azul","tela":"Denim","talla":"L","fit":"Slim","perchero":2,"posicion":3},
]

def coincide(prenda, solicitud):
    for key in solicitud:
        if solicitud[key] and prenda[key] != solicitud[key]:
            return False
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extraer', methods=['POST'])
def extraer():

    solicitud = {
        "tipo": request.form.get("tipo"),
        "color": request.form.get("color"),
        "tela": request.form.get("tela"),
        "talla": request.form.get("talla"),
        "fit": request.form.get("fit")
    }

    # Tipo de prenda obligatorio
    if not solicitud["tipo"]:
        return jsonify({"status":"error","mensaje":"Debe indicar tipo de prenda"})

    for prenda in prendas:
        if coincide(prenda, solicitud):
            comando = f"{prenda['perchero']},{prenda['posicion']}\n"
            ser.write(comando.encode())
            return jsonify({"status":"ok","mensaje":"Prenda encontrada"})

    return jsonify({"status":"error","mensaje":"No se encontró prenda"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
