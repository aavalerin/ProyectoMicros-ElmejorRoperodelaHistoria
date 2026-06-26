from flask import Flask, render_template, request, jsonify
import serial
import json
import os

app = Flask(__name__)
prendasXperch = 5
percheros = 3

###CONFIGURACION_RS232: INTENTA ABRIR PUERTO SERIAL PARA CONTROLAR EL MOTOR, SINO ACTIVA MODO PRUEBA
try:
    ser = serial.Serial('/dev/serial0', 9600, timeout=1)
except:
    print("[ADVERTENCIA] No se pudo abrir el puerto serial. Ejecutando en modo de prueba.")
    ser = None

inventario = "inventario.txt"


@app.route('/')
def index():
    return render_template('index.html')



###CARGAR_INVENTARIO: LEE inventario.txt Y RETORNA LA LISTA DE PRENDAS O UNA LISTA VACÍA SI NO EXISTE
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
        
###GUARDAR_INVENTARIO: ESCRIBE LA LISTA DE PRENDAS EN inventario.txt Y FORMATEA EL JSON
def guardar_inventario(lista_prendas):
    with open(inventario, 'w') as file:
        json.dump(lista_prendas, file, indent=4)

@app.route('/obtener_catalogo_previas', methods=['GET'])
###OBTENER_CATALOGO_PREVIAS: DEVUELVE LOS NOMBRES DE LAS PRENDAS EXTRAIDAS AL CLIENTE
def obtener_catalogo_previas():
    prendas = cargar_inventario()
    nombres_disponibles = []
    
    for prenda in prendas:
        ###OBTENER_CATALOGO_PREVIAS: INCLUYE SOLO PRENDAS CON ESTADO extraida
        if prenda.get("estado") == "extraida":
            nombres_disponibles.append(prenda["nombre"])
            
    return jsonify({"catalogo": nombres_disponibles})

@app.route('/obtener_inventario', methods=['GET'])
###OBTENER_INVENTARIO: DEVUELVE TODO EL INVENTARIO ACTUAL AL CLIENTE
def obtener_inventario():
    return jsonify({"inventario": cargar_inventario()})

@app.route('/obtener_catalogo', methods=['GET'])
###OBTENER_CATALOGO: DEVUELVE NOMBRES DE PRENDAS COLGADAS AL CLIENTE
def obtener_catalogo():
    prendas = cargar_inventario()
    nombres_disponibles = []
    
    for prenda in prendas:
        ###OBTENER_CATALOGO: SOLO INCLUYE PRENDAS CON ESTADO colgada
        if prenda.get("estado") == "colgada":
            nombres_disponibles.append(prenda["nombre"])
            
    return jsonify({"catalogo": nombres_disponibles})

@app.route('/sobrescribir_inventario', methods=['POST'])
###SOBRESCRIBIR_INVENTARIO: RECIBE JSON CON NUEVO_INVENTARIO Y SOBRESCRIBE EL ARCHIVO DE INVENTARIO
def sobrescribir_inventario():
    ###SOBRESCRIBIR_INVENTARIO: usa request.json porque el inventario se envía como estructura JSON
    datos = request.json
    
    if not datos or "nuevo_inventario" not in datos:
        return jsonify({"status": "error", "mensaje": "No se recibieron datos válidos."})
    
    nuevo_inventario = datos["nuevo_inventario"]
    
   
    guardar_inventario(nuevo_inventario)
    
    print("\n[INFO] El inventario ha sido sobrescrito mediante carga de archivo TXT.")
    return jsonify({"status": "ok", "mensaje": "Estado del perchero actualizado correctamente."})

@app.route ('/agregar_nueva', methods = ['GET', 'POST'])
###AGREGAR_NUEVA: RECIBE DATOS DE UNA NUEVA PRENDA Y LA REGISTRA EN EL INVENTARIO
def agregar_nueva():
    prendas = cargar_inventario()

    nuevo_nombre = request.form.get("nombre")
    perchero_dest = request.form.get("perchero")
     
    ###AGREGAR_NUEVA: IMPIDE NOMBRES REPETIDOS
    for p in prendas:
        if p["nombre"].lower() == nuevo_nombre.lower():
            return jsonify({"status": "error", "mensaje": f"El nombre '{nuevo_nombre}' ya existe en el sistema."})
     
    ###AGREGAR_NUEVA: CALCULA ESPACIO DISPONIBLE EN EL PERCHERO Y EL SISTEMA
    colgadas_perch_dest = [p for p in prendas if p.get("perchero") == perchero_dest and p.get("estado")== "colgada"]
    total_prendas_sistema = sum(1 for p in prendas if p.get("estado")== "colgada")
     
    ###AGREGAR_NUEVA: BLOQUEO POR FALTA DE ESPACIO TOTAL
    if total_prendas_sistema >= (prendasXperch * percheros):
        return jsonify({"status": "error", "mensaje": "Sistema bloqueado: Todos los percheros están completamente llenos."})
         
    ###AGREGAR_NUEVA: BLOQUEO POR FALTA DE ESPACIO EN PERCHERO
    if len(colgadas_perch_dest) >= prendasXperch:
        return jsonify({"status": "error", "mensaje": f"El Perchero {perchero_dest} no tiene más espacio."})
     
    ###AGREGAR_NUEVA: ASIGNA LA PRIMERA POSICION FISICA LIBRE EN EL PERCHERO
    ocupados = [int(p["posicion"]) for p in colgadas_perch_dest]
    posicion_fisica = None

    for i in range(1, prendasXperch + 1):
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
    ###AGREGAR_NUEVA: GUARDAR LA NUEVA PRENDA EN EL ARCHIVO DE INVENTARIO
    guardar_inventario(prendas)

    comando = f"<{perchero_dest},{posicion_fisica}\n"
    if ser is not None:
        ser.write(comando.encode())
        print(f"[EXITO] Moviendo motor para guardar prenda: {comando.strip()}")
    else:
        return
    

    

    print(f"\n[NUEVO REGISTRO] {nueva_prenda['nombre']} guardada en P:{perchero_dest} Pos:{posicion_fisica}")
    return jsonify({"status": "ok", "mensaje": f"Prenda '{nuevo_nombre}' registrada exitosamente."})
    
@app.route ('/agregar_previa', methods = ['GET', 'POST'])
###AGREGAR_PREVIA: REINGRESA UNA PRENDA EXTRAIDA AL PERCHERO Y ACTUALIZA SU ESTADO
def agregar_previa():
    prendas = cargar_inventario()

    nombre = request.form.get("nombre")
    perchero_dest = request.form.get("perchero")

    ###AGREGAR_PREVIA: CALCULA ESPACIO EN EL PERCHERO DESTINO
    colgadas_perch_dest = [p for p in prendas if p.get("perchero") == perchero_dest and p.get("estado") == "colgada"]
    total_prendas_sistema = sum(1 for p in prendas if p.get("estado") == "colgada")

    if total_prendas_sistema >= (prendasXperch * percheros):
        return jsonify({"status": "error", "mensaje": "Sistema bloqueado: Todos los percheros están completamente llenos."})

    ###AGREGAR_PREVIA: VALIDACION 3 - bloquea si el perchero específico está lleno
    if len(colgadas_perch_dest) >= prendasXperch:
        return jsonify({"status": "error", "mensaje": f"El Perchero {perchero_dest} no tiene más espacio."})

    ###AGREGAR_PREVIA: ASIGNA LA PRIMERA POSICION LIBRE EN EL PERCHERO DESTINO
    ocupados = [int(p["posicion"]) for p in colgadas_perch_dest]
    posicion_fisica = None

    for i in range(1, prendasXperch + 1):
        if i not in ocupados:
            posicion_fisica = i
            break

    for prenda in prendas:
        ###AGREGAR_PREVIA: BUSCA LA PRENDA EN INVENTARIO PARA REINGRESARLA
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
                return

            return jsonify({"status": "ok", "mensaje": "Prenda reingresada"})

    print(f"\n[REINGRESO] {nombre} guardada en P:{perchero_dest} Pos:{posicion_fisica}")
    return jsonify({"status": "ok", "mensaje": f"Prenda '{nombre}' reinsertada exitosamente."})

###COINCIDE: COMPARA CADA CAMPO NO VACÍO DE LA SOLICITUD CON LA PRENDA
def coincide(prenda, solicitud):
    ###COINCIDE: COMPARA CADA CAMPO NO VACÍO DE LA SOLICITUD CON LA PRENDA
    for llave in solicitud:
        if solicitud[llave] and prenda[llave] != solicitud[llave]:
            return False
    return True

###EXTRAER: RUTA QUE BUSCA UNA PRENDA COLGADA SEGÚN FILTROS Y ACTUALIZA EL INVENTARIO

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

    ###EXTRAER: tipo de prenda es obligatorio para realizar la búsqueda
    if not solicitud["tipo"]:
        return jsonify({"status":"error","mensaje":"Debe indicar tipo de prenda"})

    ###EXTRAER: busca la primera prenda colgada que coincida con todos los filtros
    for prenda in prendas:
        if  prenda.get("estado") == "colgada" and coincide(prenda, solicitud):
            comando = f"<{prenda['perchero']},{prenda['posicion']}\n"
            
            if ser is not None:
                ser.write(comando.encode())
                print(f"[EXITO] Extrayendo prenda: Comando enviado -> {comando.strip()}")
            else:
                return

            ###EXTRAER: ACTUALIZA EL ESTADO DE LA PRENDA A extraida Y LA SACA DEL PERCHERO
            prenda["estado"] = "extraida"
            prenda["perchero"] = "None"
            prenda["posicion"] = "None"
            guardar_inventario(prendas)

            

            return jsonify({"status":"ok","mensaje":"Prenda encontrada. Extrayendo..."})


    return jsonify({"status":"error","mensaje":"No se encontró dicha prenda"})

###EXTRAER_NOMBRE: EXTRAE UNA PRENDA POR NOMBRE EXPLÍCITO SI ESTÁ COLGADA
@app.route('/extraer_nombre', methods=['POST'])

def extraer_nombre():

    nombre = request.form.get("nombre")
    prendas = cargar_inventario()
    

    ###EXTRAER_NOMBRE: BUSCA LA PRENDA COLGADA QUE COINCIDA POR NOMBRE
    for prenda in prendas:
        if  prenda.get("estado") == "colgada" and prenda.get("nombre").lower() == nombre.lower():
            comando = f"<{prenda['perchero']},{prenda['posicion']}\n"
            
            if ser is not None:
                ser.write(comando.encode())
                print(f"[EXITO] Extrayendo '{nombre}': Comando enviado -> {comando.strip()}")

                ###EXTRAER_NOMBRE: LEE RESPUESTA DEL LOOPBACK SERIAL SI ESTÁ DISPONIBLE
                respuesta = ser.readline().decode().strip()
                print(f"[LOOPBACK] Recibido de vuelta: {respuesta}")

            ###EXTRAER_NOMBRE: ACTUALIZA EL ESTADO DE LA PRENDA A extraida
            prenda["estado"] = "extraida"
            prenda["perchero"] = "None"
            prenda["posicion"] = "None"
            guardar_inventario(prendas)

            

            return jsonify({"status":"ok","mensaje":"Prenda encontrada. Extrayendo..."})


    return jsonify({"status":"error","mensaje":"No se encontró dicha prenda"})

@app.route('/eliminar', methods = ['POST', 'GET'])
###ELIMINAR: BORRA UNA PRENDA DEL HISTORIAL SI NO ESTÁ COLGADA EN EL PERCHERO
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



#CREACIÓN DEL SERVER DE PÁGINA WEB
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = True)
