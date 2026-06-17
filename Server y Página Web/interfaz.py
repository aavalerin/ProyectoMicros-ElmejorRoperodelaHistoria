import tkinter as  tk
from tkinter import messagebox, ttk, filedialog
import requests
import json
import os

class InterfazPercheros:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Perchero Inteligente")
        self.ventana.geometry ("600x400")
        self.url_pagina = "http://127.0.0.1:5000"
        self.crear_menu()

    def crear_menu(self):

        for vista in self.ventana.winfo_children():
            vista.destroy()
        
        tk.Label(self.ventana, text="Sistema de percheros", font=("Arial", 18, "bold")).pack(pady=20)

        boton_estilo = {"width": 20, "font": ("Arial", 12), "pady": 10}
        tk.Button(self.ventana, text="Agregar Prenda", command=self.vista_agregar, **boton_estilo).pack(pady=10)
        tk.Button(self.ventana, text="Extraer Prenda por Nombre", command= self.vista_extraer, **boton_estilo).pack(pady=10)
        tk.Button(self.ventana, text="Eliminar Prenda", command= self.vista_eliminar, **boton_estilo).pack(pady=10)
        tk.Button(self.ventana, text="Diagrama de Est. Act.", command=self.vista_diagrama, **boton_estilo).pack(pady=10)
        tk.Button(self.ventana, text="Cargar Estado ", command=self.cargar_estado_txt, **boton_estilo).pack(pady=10)
        tk.Button(self.ventana, text="Informe por Características", command=self.vista_informe, **boton_estilo).pack(pady=10)
        tk.Button(self.ventana, text="Salir", command=self.ventana.quit, bg="#ff9999", **boton_estilo).pack(pady=10)

    def vista_agregar(self):
        
        for vista in self.ventana.winfo_children():
            vista.destroy()

        tk.Label(self.ventana, text="Registrar Prenda", font=("Arial", 16, "bold")).pack(pady=15)
        

        tk.Button(self.ventana, text="Agregar Prenda Nueva", command=self.agregar_nueva, bg="#0965CE", font=("Arial", 11)).pack(pady=15)
        tk.Button(self.ventana, text="Agregar Prenda Previa", command=self.agregar_previa, bg="#C75019", font=("Arial", 11)).pack(pady=15)
        tk.Button(self.ventana, text="Volver al Menú", command=self.crear_menu, font=("Arial", 11)).pack()

    def agregar_nueva(self):
        for vista in self.ventana.winfo_children():
            vista.destroy()

        tk.Label(self.ventana, text="Registrar Nueva Prenda", font=("Arial", 16, "bold")).pack(pady=15)
        

        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=10)

        tk.Label(formulario, text="Ingrese el nombre:").grid(row=0, sticky="e", padx=5, pady=5)
        self.input_nombre = tk.Entry(formulario, width = 25)
        self.input_nombre.grid(row=0, column=1,sticky="e", padx=5, pady=5)

        tk.Label(formulario, text="Tipo:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.tipo_prenda = ttk.Combobox(formulario, values=["T-Shirt", "Pantalón", "Short", "Camisa Manga Larga", "Enagua"], width=22, state="readonly")
        self.tipo_prenda.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Color:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.input_color = ttk.Combobox(formulario, values=["Blanco", "Negro", "Café", "Azul", "Gris"], width=22,state="readonly")
        self.input_color.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Tela:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.input_tela = ttk.Combobox(formulario, values=["Denim", "Algodón", "Polyester", "Seda", "Lino",], width=22, state="readonly")
        self.input_tela.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Talla:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.input_talla = ttk.Combobox(formulario, values=[ "S", "M", "L", "XL", "XXL"], width=22, state="readonly")
        self.input_talla.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Fit:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.input_fit = ttk.Combobox(formulario, values=[ "Regular", "Skinny", "Slim", "Loose", "Oversized"], width=22, state="readonly")
        self.input_fit.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(formulario, text="Número de perchero:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.input_perchero = ttk.Combobox(formulario, values=[ "Perchero 1", "Perchero 2", "Perchero 3"], width=22, state="readonly")
        self.input_perchero.grid(row=6, column=1, padx=5, pady=5)



        # Botones de acción
        tk.Button(self.ventana, text="Validar", command=self.validacion1_flask, bg="#90EE90", font=("Arial", 11)).pack(pady=15)
        tk.Button(self.ventana, text="Volver al Menú", command=self.crear_menu, font=("Arial", 11)).pack()


    def validacion1_flask(self):
       
        datos = {
            "nombre": self.input_nombre.get(),
            "tipo": self.tipo_prenda.get(),
            "color": self.input_color.get(),
            "tela": self.input_tela.get(),
            "talla": self.input_talla.get(),
            "fit": self.input_fit.get(),
            "perchero": self.input_perchero.get() 
        }

        if not all(datos.values()):
            messagebox.showwarning("Faltan datos", "Por favor, complete todos los campos del formulario.")
            return
    
        datos["perchero"] = datos["perchero"].replace("Perchero ", "")

        
        url = f"{self.url_pagina}/agregar_nueva"

        try:
            respuesta = requests.post(url, data=datos)
            
            if respuesta.status_code == 200:
                info = respuesta.json()
                if info.get("status") == "ok":
                    messagebox.showinfo("Éxito", info.get("mensaje"))
                    # Refrescar la vista tras el éxito
                    for vista in self.ventana.winfo_children():
                        vista.destroy()
                    self.vista_agregar() 
                else:
                    messagebox.showerror("Error", info.get("mensaje"))
            else:
                messagebox.showerror("Error del Servidor", f"Código: {respuesta.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con el servidor.\nDetalle: {e}")

    
    def agregar_previa(self):
        for vista in self.ventana.winfo_children():
             vista.destroy()
    
        tk.Label(self.ventana, text="Reinsertar Prenda", font=("Arial", 16, "bold")).pack(pady=15)
         
        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=10)
         
        nombres_prendas = self.cargar_prendas_previas()
         
        if not nombres_prendas:
            tk.Label(formulario, text="No hay prendas registradas", font=("Arial", 12)).pack(pady=20)
            tk.Button(self.ventana, text="Volver", command=self.vista_agregar, font=("Arial", 11)).pack(pady=10)
            return
         
        tk.Label(formulario, text="Seleccione una prenda:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.seleccionar_prenda = ttk.Combobox(formulario, values=nombres_prendas, width=30, state="readonly")
        self.seleccionar_prenda.grid(row=0, column=1, padx=5, pady=5)
    
        tk.Label(formulario, text="Número de perchero:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.input_perchero = ttk.Combobox(formulario, values=[ "Perchero 1", "Perchero 2", "Perchero 3"], width=22, state="readonly")
        self.input_perchero.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(self.ventana, text="Reinsertar Prenda Seleccionada", command=self.validacion2_flask, bg="#90EE90", font=("Arial", 11)).pack(pady=15)
        tk.Button(self.ventana, text="Volver", command=self.vista_agregar, font=("Arial", 11)).pack()
    
    def validacion2_flask(self):
        nombre_seleccionado = self.seleccionar_prenda.get()
        perchero_seleccionado = self.input_perchero.get()
        

        if not nombre_seleccionado or not perchero_seleccionado:
            messagebox.showwarning("Faltan Datos.", "Seleccione al menos una prenda y un perchero")
            return
        
        new_perchero = perchero_seleccionado.replace("Perchero ", "")

        datos = {
            "nombre": nombre_seleccionado,
            "perchero": new_perchero
        }


        url = f"{self.url_pagina}/agregar_previa"


        try:
            respuesta = requests.post(url, data=datos)
            
            if respuesta.status_code == 200:
                info = respuesta.json()
                if info.get("status") == "ok":
                    messagebox.showinfo("Éxito", info.get("mensaje"))
                    # Regresar al submenú de agregar tras el éxito
                    for vista in self.ventana.winfo_children():
                        vista.destroy()
                    self.vista_agregar() 
                else:
                    messagebox.showerror("Error", info.get("mensaje"))
            else:
                messagebox.showerror("Error del Servidor", f"Código: {respuesta.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con el servidor.\nDetalle: {e}")

    #def agregar_prenda_flask():

    def cargar_prendas_previas(self):
        url = f"{self.url_pagina}/obtener_catalogo_previas"

        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                return datos.get("catalogo", [])
            else:
                messagebox.showerror("Error", "No hay registro de prendas extraídas") 
                return []
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar: {e}")
            return []
        
    def cargar_nombres_prendas(self):
        url = f"{self.url_pagina}/obtener_catalogo"

        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                return datos.get("catalogo", [])
            else:
                messagebox.showerror("Error", "No hay prendas para extraer") 
                return []
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar: {e}")
            return []
    
    def vista_eliminar(self):
        for vista in self.ventana.winfo_children():
            vista.destroy()

        tk.Label(self.ventana, text = "Eliminar Prenda", font = ("Arial", 16, "bold")).pack(pady=15)

        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=10)

        nombres_prendas = self.cargar_prendas_previas()
         
        if not nombres_prendas:
            tk.Label(formulario, text="No hay prendas que se puedan eliminar", font=("Arial", 12)).pack(pady=20)
            tk.Button(self.ventana, text="Volver", command=self.crear_menu, font=("Arial", 11)).pack(pady=10)
            return

        tk.Label(formulario, text="Seleccione una prenda:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.seleccionar_prenda = ttk.Combobox(formulario, values=nombres_prendas, width=30, state="readonly")
        self.seleccionar_prenda.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.ventana, text="Eliminar Prenda Seleccionada", command=self.validacion3_flask, bg="#90EE90", font=("Arial", 11)).pack(pady=15)
        tk.Button(self.ventana, text="Volver", command=self.crear_menu, font=("Arial", 11)).pack()
        
       
    def validacion3_flask(self):
        nombre_seleccionado = self.seleccionar_prenda.get()

        if not nombre_seleccionado:
            messagebox.showwarning("Faltan Datos.", "Seleccione una prenda")
            return
        datos = {
            "nombre": nombre_seleccionado,
        }
        url = f"{self.url_pagina}/eliminar"

        try:
            respuesta = requests.post(url, data = datos)

            if respuesta.status_code == 200:
                info = respuesta.json()
                if info.get("status") == "ok":
                    messagebox.showinfo("Éxito", info.get("mensaje"))
                    # Regresar al submenú de agregar tras el éxito
                    for vista in self.ventana.winfo_children():
                        vista.destroy()
                    self.crear_menu() 
                else:
                    messagebox.showerror("Error", info.get("mensaje"))
            else:
                messagebox.showerror("Error del Servidor", f"Código: {respuesta.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con el servidor.\nDetalle: {e}")


    def vista_extraer(self):
        for vista in self.ventana.winfo_children():
            vista.destroy()
        
        tk.Label(self.ventana, text="Extraer Prenda", font=("Arial", 16, "bold")).pack(pady=15)

        formulario = tk.Frame(self.ventana)
        formulario.pack(pady=10)

        nombres_prendas = self.cargar_nombres_prendas()
         
        if not nombres_prendas:
            tk.Label(formulario, text="No hay prendas para extraer", font=("Arial", 12)).pack(pady=20)
            tk.Button(self.ventana, text="Volver", command=self.crear_menu, font=("Arial", 11)).pack(pady=10)
            return
    
        tk.Label(formulario, text="Seleccione una prenda:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.seleccionar_prenda = ttk.Combobox(formulario, values=nombres_prendas, width=30, state="readonly")
        self.seleccionar_prenda.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self.ventana, text="Extraer Prenda", command=self.validacion4_flask, bg="#DB8F2A", font=("Arial", 11)).pack(pady=15)
        tk.Button(self.ventana, text="Volver", command=self.crear_menu, font=("Arial", 11)).pack()
        
        


    def validacion4_flask(self):
        prenda_seleccionada = self.seleccionar_prenda.get()

        if not prenda_seleccionada:
            messagebox.showwarning("Error", "Por favor, seleccione una prenda")
            return
        
        datos = {
            "nombre": prenda_seleccionada

        }

        url = f"{self.url_pagina}/extraer_nombre"


        try:
            respuesta = requests.post(url, data = datos)

            if respuesta.status_code == 200:
                info = respuesta.json()
                if info.get("status") == "ok":
                    messagebox.showinfo("Éxito", info.get("mensaje"))
                    # Regresar al submenú de agregar tras el éxito
                    for vista in self.ventana.winfo_children():
                        vista.destroy()
                    self.crear_menu() 
                else:
                    messagebox.showerror("Error", info.get("mensaje"))
            else:
                messagebox.showerror("Error del Servidor", f"Código: {respuesta.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con el servidor.\nDetalle: {e}")
        
    def vista_informe(self):
        for vista in self.ventana.winfo_children():
            vista.destroy()

        tk.Label(self.ventana, text="Informe por Características", font=("Arial", 16, "bold")).pack(pady=10)

        # Contenedor para los filtros
        frame_filtros = tk.Frame(self.ventana)
        frame_filtros.pack(pady=5)

        # Cajas de selección (El primer valor es "" para permitir dejar el filtro en blanco)
        tk.Label(frame_filtros, text="Tipo:").grid(row=0, column=0, padx=5, sticky="e")
        self.filtro_tipo = ttk.Combobox(frame_filtros, values=["", "T-Shirt", "Pantalón", "Short", "Camisa Manga Larga", "Enagua"], width=12, state="readonly")
        self.filtro_tipo.grid(row=0, column=1, padx=5)

        tk.Label(frame_filtros, text="Color:").grid(row=0, column=2, padx=5, sticky="e")
        self.filtro_color = ttk.Combobox(frame_filtros, values=["", "Blanco", "Negro", "Café", "Azul", "Gris"], width=10, state="readonly")
        self.filtro_color.grid(row=0, column=3, padx=5)

        tk.Label(frame_filtros, text="Tela:").grid(row=0, column=4, padx=5, sticky="e")
        self.filtro_tela = ttk.Combobox(frame_filtros, values=["", "Denim", "Algodón", "Polyester", "Seda", "Lino"], width=10, state="readonly")
        self.filtro_tela.grid(row=0, column=5, padx=5)

        tk.Label(frame_filtros, text="Talla:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.filtro_talla = ttk.Combobox(frame_filtros, values=["", "S", "M", "L", "XL", "XXL"], width=12, state="readonly")
        self.filtro_talla.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_filtros, text="Fit:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.filtro_fit = ttk.Combobox(frame_filtros, values=["", "Regular", "Skinny", "Slim", "Loose", "Oversized"], width=10, state="readonly")
        self.filtro_fit.grid(row=1, column=3, padx=5, pady=5)

        # Botón para ejecutar la búsqueda
        tk.Button(frame_filtros, text="Filtrar", command=self.ejecutar_filtro, bg="#0965CE", fg="white").grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="we")

        # Configuración de la tabla (Treeview) para mostrar los resultados
        columnas = ("Nombre", "Tipo", "Color", "Talla", "Ubicación")
        self.tabla_resultados = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=8)
        
        # Definir los encabezados y anchos de columna
        self.tabla_resultados.heading("Nombre", text="Nombre")
        self.tabla_resultados.column("Nombre", width=120)
        self.tabla_resultados.heading("Tipo", text="Tipo")
        self.tabla_resultados.column("Tipo", width=100)
        self.tabla_resultados.heading("Color", text="Color")
        self.tabla_resultados.column("Color", width=80)
        self.tabla_resultados.heading("Talla", text="Talla")
        self.tabla_resultados.column("Talla", width=50)
        self.tabla_resultados.heading("Ubicación", text="Ubicación")
        self.tabla_resultados.column("Ubicación", width=100)

        self.tabla_resultados.pack(pady=10)

        # Botón inferior
        tk.Button(self.ventana, text="Volver al Menú", command=self.crear_menu, font=("Arial", 11)).pack(pady=5)

    def ejecutar_filtro(self):
        # 1. Limpiar la tabla de resultados anteriores
        for fila in self.tabla_resultados.get_children():
            self.tabla_resultados.delete(fila)

        # 2. Recolectar lo que el usuario seleccionó (los vacíos se ignoran)
        filtros = {
            "tipo": self.filtro_tipo.get(),
            "color": self.filtro_color.get(),
            "tela": self.filtro_tela.get(),
            "talla": self.filtro_talla.get(),
            "fit": self.filtro_fit.get()
        }

        # 3. Pedir el inventario actual a Flask
        inventario = []
        try:
            respuesta = requests.get(f"{self.url_pagina}/obtener_inventario")
            if respuesta.status_code == 200:
                inventario = respuesta.json().get("inventario", [])
            else:
                messagebox.showerror("Error", "No se pudo obtener el inventario del servidor.")
                return
        except requests.exceptions.RequestException:
            messagebox.showerror("Error de Conexión", "No hay conexión con el servidor Flask.")
            return

        # 4. Aplicar la lógica de filtrado universal
        for prenda in inventario:
            # Solo buscamos entre lo que está físicamente colgado
            if prenda.get("estado") != "colgada":
                continue

            coincide = True
            for clave, valor_filtro in filtros.items():
                # Si hay un filtro seleccionado y no es igual a la característica de la prenda, se descarta
                if valor_filtro != "" and prenda.get(clave) != valor_filtro:
                    coincide = False
                    break
            
            # Si superó todos los filtros, lo agregamos a la tabla
            if coincide:
                ubicacion = f"P:{prenda['perchero']} - Pos:{prenda['posicion']}"
                self.tabla_resultados.insert("", "end", values=(
                    prenda["nombre"], 
                    prenda["tipo"], 
                    prenda["color"], 
                    prenda["talla"], 
                    ubicacion
                ))

    def cargar_estado_txt(self):
        # Abre una ventana para buscar el archivo 
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de estado",
            filetypes=[("Archivos de texto", "*.txt")]
        )

        # Si se cierra la ventana sin seleccionar
        if not ruta_archivo:
            return 

        # Validación del nombre obligatorio
        if os.path.basename(ruta_archivo) != "inventario.txt":
            messagebox.showwarning("Archivo Inválido", "Por requerimiento, el archivo debe llamarse estrictamente 'inventario.txt'")
            return

        # Intentar leer el archivo y verificar que el formato sea correcto
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as file:
                datos_nuevos = json.load(file)
        except json.JSONDecodeError:
            messagebox.showerror("Error de Formato", "El archivo está corrupto o no tiene la estructura interna correcta.")
            return
        except Exception as e:
            messagebox.showerror("Error de Lectura", f"No se pudo leer el archivo.\n{e}")
            return

        # Enviar los datos validados al servidor Flask
        url = f"{self.url_pagina}/sobrescribir_inventario"
        try:
            # Enviamos como JSON puro en lugar de form-data
            respuesta = requests.post(url, json={"nuevo_inventario": datos_nuevos})
            
            if respuesta.status_code == 200:
                info = respuesta.json()
                if info.get("status") == "ok":
                    messagebox.showinfo("Éxito", info.get("mensaje"))
                else:
                    messagebox.showerror("Error", info.get("mensaje"))
            else:
                messagebox.showerror("Error del Servidor", f"Código: {respuesta.status_code}")
                
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar con el servidor.\nDetalle: {e}")

    def vista_diagrama(self):
        for vista in self.ventana.winfo_children():
            vista.destroy()

        tk.Label(self.ventana, text="Estado Actual de los Percheros", font=("Arial", 16, "bold")).pack(pady=10)

        # Contenedor principal para la matriz física
        cuadricula = tk.Frame(self.ventana)
        cuadricula.pack(pady=10)

        # 1. Dibujar los encabezados de las columnas (Percheros)
        for p in range(1, 4):
            tk.Label(cuadricula, text=f"Perchero {p}", font=("Arial", 11, "bold"), fg="#333333").grid(row=0, column=p, padx=15, pady=5)

        # 2. Dibujar los indicadores de las filas (Posiciones)
        for pos in range(1, 6):
            tk.Label(cuadricula, text=f"Pos {pos}", font=("Arial", 9, "italic"), fg="#666666").grid(row=pos, column=0, padx=10, pady=10)

        # 3. Solicitar el inventario actualizado al servidor Flask
        inventario_completo = []
        try:
            respuesta = requests.get(f"{self.url_pagina}/obtener_inventario")
            if respuesta.status_code == 200:
                inventario_completo = respuesta.json().get("inventario", [])
        except requests.exceptions.RequestException:
            messagebox.showerror("Error", "No se pudo conectar al servidor para obtener el estado actual.")

        # 4. Mapear las prendas colgadas
        mapa_fisico = {}
        for prenda in inventario_completo:
            if prenda.get("estado") == "colgada":
                coordenada = (int(prenda["perchero"]), int(prenda["posicion"]))
                mapa_fisico[coordenada] = prenda

        # Nombres de los archivos PNG que debes tener en tu carpeta (tamaño recomendado: 50x50 px)
        archivos_ropa = {
            "T-Shirt": "tshirt.png",
            "Pantalón": "pantalon.png",
            "Short": "short.png",
            "Camisa Manga Larga": "camisa.png",
            "Enagua": "enagua.png"
        }

        # Diccionario vital para evitar que Python borre las imágenes de la memoria (Garbage Collector)
        if not hasattr(self, 'imagenes_cargadas'):
            self.imagenes_cargadas = {}

        # 5. Renderizar dinámicamente cada celda del perchero
        import os
        directorio_actual = os.path.dirname(os.path.abspath(__file__))

        for pos in range(1, 6):
            for p in range(1, 4):
                prenda_en_sitio = mapa_fisico.get((p, pos))
                
                # Crear una celda de tamaño fijo para que la cuadrícula no se deforme
                celda = tk.Frame(cuadricula, width=110, height=85, bd=2)
                celda.grid(row=pos, column=p, padx=6, pady=6)
                celda.grid_propagate(False) # Obliga al Frame a mantener su tamaño ignorando el contenido
                
                if prenda_en_sitio:
                    celda.config(bg="#D4EDDA", relief="raised")
                    tipo = prenda_en_sitio.get("tipo")
                    nombre_archivo = archivos_ropa.get(tipo, "default.png")
                    ruta_img = os.path.join(directorio_actual, nombre_archivo)
                    
                    # Intentar cargar y mostrar la imagen
                    try:
                        if tipo not in self.imagenes_cargadas:
                            self.imagenes_cargadas[tipo] = tk.PhotoImage(file=ruta_img)
                        img = self.imagenes_cargadas[tipo]
                        
                        lbl_img = tk.Label(celda, image=img, bg="#D4EDDA")
                        lbl_img.pack(pady=(2, 0))
                    except Exception as e:
                        # Si no encuentra la imagen o no es PNG, la omitimos sin que el programa se caiga
                        print(f"[ADVERTENCIA] No se pudo cargar la imagen {nombre_archivo}: {e}")

                    # Texto de la prenda debajo de la imagen
                    texto_celda = f"{prenda_en_sitio['nombre'][:12]}\n[{prenda_en_sitio['color']}]"
                    tk.Label(celda, text=texto_celda, bg="#D4EDDA", fg="#155724", font=("Arial", 8, "bold")).pack()

                else:
                    # Celda Vacía
                    celda.config(bg="#E2E3E5", relief="sunken")
                    tk.Label(celda, text="Vacío", bg="#E2E3E5", fg="#6C757D", font=("Arial", 9)).pack(expand=True)

        # Botón inferior para regresar
        tk.Button(self.ventana, text="Volver al Menú Principal", command=self.crear_menu, font=("Arial", 11)).pack(pady=15)
if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazPercheros(ventana)
    ventana.mainloop()


        