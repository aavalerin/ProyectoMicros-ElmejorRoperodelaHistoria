from flask import Flask, render_template, request, jsonify
import serial
import json
import os

app = Flask(__name__)
prendasXperch = 5
percheros = 3

# Configuración RS232 UART
try:
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
except:
    print("[ADVERTENCIA] No se pudo abrir el puerto serial. Ejecutando en modo de prueba.")
    ser = None

inventario = "inventario.txt"


@app.route('/')
def index():
    return render_template('index.html')



#Se carga el inventario.txt
def cargar_inventario():
    if not os.path.exists(inventario):
        with open(inventario, 'w') as file:
            json.dump([], file)
        return []

    with open(inventario, 'r') as file:
        try: 
            return json.load(file)
        except json.JSONDecodeError:
            return []
        
def guardar_inventario(lista_prendas):
    with open(inventario, 'w') as file:
        json.dump(lista_prendas, file, indent=4)

@app.route('/obtener_catalogo_previas', methods=['GET'])
def obtener_catalogo_previas():
    prendas = cargar_inventario()
    nombres_disponibles = []
    
    for prenda in prendas:
        # Solo enviamos a la interfaz las prendas que ya están fuera del perchero
        if prenda.get("estado") == "extraida":
            nombres_disponibles.append(prenda["nombre"])
            
    return jsonify({"catalogo": nombres_disponibles})

@app.route('/obtener_inventario', methods=['GET'])
def obtener_inventario():
    return jsonify({"inventario": cargar_inventario()})

@app.route('/obtener_catalogo', methods=['GET'])
def obtener_catalogo():
    prendas = cargar_inventario()
    nombres_disponibles = []
    
    for prenda in prendas:
        # Solo enviamos a la interfaz las prendas que están en el perchero
        if prenda.get("estado") == "colgada":
            nombres_disponibles.append(prenda["nombre"])
            
    return jsonify({"catalogo": nombres_disponibles})

@app.route('/sobrescribir_inventario', methods=['POST'])
def sobrescribir_inventario():
    # En lugar de request.form, usamos request.json porque mandamos una lista compleja
    datos = request.json
    
    if not datos or "nuevo_inventario" not in datos:
        return jsonify({"status": "error", "mensaje": "No se recibieron datos válidos."})
    
    nuevo_inventario = datos["nuevo_inventario"]
    
   
    guardar_inventario(nuevo_inventario)
    
    print("\n[INFO] El inventario ha sido sobrescrito mediante carga de archivo TXT.")
    return jsonify({"status": "ok", "mensaje": "Estado del perchero actualizado correctamente."})

@app.route ('/agregar_nueva', methods = ['GET', 'POST'])
def agregar_nueva():
    prendas = cargar_inventario()


    nuevo_nombre = request.form.get("nombre")
    perchero_dest = request.form.get("perchero")
     
          # VALIDACIÓN 1: Impedir nombre repetido
    for p in prendas:
        if p["nombre"].lower() == nuevo_nombre.lower():
            return jsonify({"status": "error", "mensaje": f"El nombre '{nuevo_nombre}' ya existe en el sistema."})
     
     # Cálculos de capacidad
    colgadas_perch_dest = [p for p in prendas if p.get("perchero") == perchero_dest and p.get("estado")== "colgada"]
    total_prendas_sistema = sum(1 for p in prendas if p.get("estado")== "colgada")
     
     # VALIDACIÓN 2: Llenado total del sistema
    if total_prendas_sistema >= (prendasXperch * percheros):
        return jsonify({"status": "error", "mensaje": "Sistema bloqueado: Todos los percheros están completamente llenos."})
         
     # VALIDACIÓN 3: Llenado del perchero específico
    if len(colgadas_perch_dest) >= prendasXperch:
        return jsonify({"status": "error", "mensaje": f"El Perchero {perchero_dest} no tiene más espacio."})
     
     # Asignar la siguiente posición física disponible en ese perchero
    ocupados = [int(p["posicion"]) for p in colgadas_perch_dest]
    posicion_fisica = None

    for i in  range(1, prendasXperch + 1 ):
        if i not in ocupados:
            posicion_fisica = i
            break
         
     
    nueva_prenda = {
        "nombre": nuevo_nombre,
        "tipo": request.form.get("tipo"),
        "color": request.form.get("color"),
        "tela": request.form.get("tela"),
        "talla": request.form.get("talla"),
        "fit": request.form.get("fit"),
        "perchero": perchero_dest,
        "posicion": str(posicion_fisica),
        "estado": "colgada"
     }
     
    prendas.append(nueva_prenda)
    guardar_inventario(prendas) # Sobrescribir el .txt

    comando = f"<{perchero_dest},{posicion_fisica}\n"
    if ser is not None:
        ser.write(comando.encode())
        print(f"[EXITO] Moviendo motor para guardar prenda: {comando.strip()}")
    else:
        print(f"[MODO PRUEBA] El motor se movería a: P{perchero_dest}, Pos{posicion_fisica}")
    

    

    print(f"\n[NUEVO REGISTRO] {nueva_prenda['nombre']} guardada en P:{perchero_dest} Pos:{posicion_fisica}")
    return jsonify({"status": "ok", "mensaje": f"Prenda '{nuevo_nombre}' registrada exitosamente."})
    
@app.route ('/agregar_previa', methods = ['GET', 'POST'])
def agregar_previa():
    prendas = cargar_inventario()

    nombre = request.form.get("nombre")
    perchero_dest = request.form.get("perchero")

    # Cálculos de capacidad
    colgadas_perch_dest = [p for p in prendas if p.get("perchero") == perchero_dest and p.get("estado") == "colgada"]
    total_prendas_sistema = sum(1 for p in prendas if p.get("estado") == "colgada")

    # VALIDACIÓN 2: Llenado total del sistema
    if total_prendas_sistema >= (prendasXperch * percheros):
        return jsonify({"status": "error", "mensaje": "Sistema bloqueado: Todos los percheros están completamente llenos."})

    # VALIDACIÓN 3: Llenado del perchero específico
    if len(colgadas_perch_dest) >= prendasXperch:
        return jsonify({"status": "error", "mensaje": f"El Perchero {perchero_dest} no tiene más espacio."})

    # Asignar la siguiente posición física disponible en ese perchero
    ocupados = [int(p["posicion"]) for p in colgadas_perch_dest]
    posicion_fisica = None

    for i in range(1, prendasXperch + 1):
        if i not in ocupados:
            posicion_fisica = i
            break

    for prenda in prendas:
        if prenda.get("nombre") == nombre:
            
            prenda["estado"] = "colgada"
            prenda["posicion"] = str(posicion_fisica)
            prenda["perchero"] = perchero_dest

            guardar_inventario(prendas)

            comando = f"<{perchero_dest},{posicion_fisica}\n"
            if ser is not None:
                ser.write(comando.encode())
                print(f"[EXITO] Moviendo motor para guardar prenda: {comando.strip()}")
            else:
                print(f"[MODO PRUEBA] El motor se movería a: P{perchero_dest}, Pos{posicion_fisica}")

            return jsonify({"status": "ok", "mensaje": "Prenda reingresada"})

    print(f"\n[REINGRESO] {nombre} guardada en P:{perchero_dest} Pos:{posicion_fisica}")
    return jsonify({"status": "ok", "mensaje": f"Prenda '{nombre}' reinsertada exitosamente."})

def coincide(prenda, solicitud):
    for llave in solicitud:
        if solicitud[llave] and prenda[llave] != solicitud[llave]:
            return False
    return True

#Se genera la página con el estilo y formato asignado

@app.route('/extraer', methods=['POST'])
def extraer():

    prendas = cargar_inventario()

    solicitud = {
        "tipo": request.form.get("tipo"),
        "color": request.form.get("color"),
        "tela": request.form.get("tela"),
        "talla": request.form.get("talla"),
        "fit": request.form.get("fit")
    }

    print("\n[INFO] --- NUEVA ORDEN RECIBIDA ---")
    print(f"[INFO] Datos crudos del formulario: {solicitud}")
    print("[INFO] ----------------------------\n")

    # Tipo de prenda obligatorio
    if not solicitud["tipo"]:
        return jsonify({"status":"error","mensaje":"Debe indicar tipo de prenda"})

    #Se busca una coincidencia en el inventario
    for prenda in prendas:
        if  prenda.get("estado") == "colgada" and coincide(prenda, solicitud):
            comando = f"<{prenda['perchero']},{prenda['posicion']}\n"
            
            if ser is not None:
                ser.write(comando.encode())
                print(f"[EXITO] Extrayendo prenda: Comando enviado -> {comando.strip()}")
            else:
                print(f"[MODO PRUEBA] Se extraería de: {comando.strip()}")

            #Se actualiza el inventario para eliminar la prenda extraída
            prenda["estado"] = "extraida"
            prenda["perchero"] = "None"
            prenda["posicion"] = "None"
            guardar_inventario(prendas)

            

            return jsonify({"status":"ok","mensaje":"Prenda encontrada. Extrayendo..."})


    return jsonify({"status":"error","mensaje":"No se encontró dicha prenda"})


@app.route('/extraer_nombre', methods=['POST'])
def extraer_nombre():

    nombre = request.form.get("nombre")
    prendas = cargar_inventario()
    

    #Se busca una coincidencia en el inventario
    for prenda in prendas:
        if  prenda.get("estado") == "colgada" and prenda.get("nombre").lower() == nombre.lower():
            comando = f"<{prenda['perchero']},{prenda['posicion']}\n"
            
            if ser is not None:
                ser.write(comando.encode())
                print(f"[EXITO] Extrayendo '{nombre}': Comando enviado -> {comando.strip()}")

                # Agrega esto para la prueba de loopback
                respuesta = ser.readline().decode().strip()
                print(f"[LOOPBACK] Recibido de vuelta: {respuesta}")

            #Se actualiza el inventario para eliminar la prenda extraída
            prenda["estado"] = "extraida"
            prenda["perchero"] = "None"
            prenda["posicion"] = "None"
            guardar_inventario(prendas)

            

            return jsonify({"status":"ok","mensaje":"Prenda encontrada. Extrayendo..."})


    return jsonify({"status":"error","mensaje":"No se encontró dicha prenda"})

@app.route('/eliminar', methods = ['POST', 'GET'])
def eliminar():
    
    nombre = request.form.get("nombre")
    prendas = cargar_inventario()

    for prenda in prendas:
        if  prenda.get("nombre") == nombre:
            if prenda.get("estado") == "colgada":
                return jsonify({
                    "status": "Error", 
                    "mensaje": f"No se puede eliminar '{nombre}'. Primero debe ser extraída del perchero."
                })


            prendas.remove(prenda)
            guardar_inventario(prendas)

            return jsonify({"status":"ok","mensaje":"Prenda encontrada. Eliminando..."})
    
    return jsonify({"status": "error", "mensaje": "No se pudo eliminar la prenda"})



#Creación del server para hostear la página web
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)
