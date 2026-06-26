document.getElementById('garmentForm').addEventListener('submit', function(e) {
    ///EXTRACCION ASINCRONA: EVITA QUE EL NAVEGADOR RECARGUE LA PAGINA O SALTE A OTRA PESTAÑA DEL NAVEGADOR
    e.preventDefault(); 

    const btn = this.querySelector('.btn-submit');
    const originalText = btn.innerHTML;

    ///ESTADO DEL BOTON: MODIFICA EL BOTON VISUALMENTE PARA MOSTRAR LA ANIMACION DE CARGA MIENTRAS SE PROCESA
    btn.style.pointerEvents = 'none';
    btn.innerHTML = '<span>Extrayendo...</span> <i class="fas fa-spinner fa-spin"></i>';

    ///CAPTURA DE DATOS: RECOLECTA TODOS LOS VALORES SELECCIONADOS EN EL FORMULARIO HTML AUTOMATICAMENTE
    const formData = new FormData(this);

    ///ENVIO DE PETICION: ENVIA LOS DATOS CAPTURADOS POR DEBAJO DE LA MESA AL ENDPOINT DE FLASK
    fetch('/extraer', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        ///RESTAURAR INTERFAZ: DEVUELVE EL BOTON A SU ESTADO Y TEXTO ORIGINAL TRAS RECIBIR RESPUESTA
        btn.style.pointerEvents = 'auto';
        btn.innerHTML = originalText;

        ///PROCESAMIENTO DE RESPUESTA: EVALUA EL RESULTADO DEL SERVIDOR Y MUESTRA LA ALERTA CORRESPONDIENTE
        if (data.status === 'ok') {
            alert("Éxito: " + data.mensaje);
            this.reset(); 
        } else {
            alert("Error: " + data.mensaje);
        }
    })
    .catch(error => {
        ///MANEJO DE ERRORES: RESTAURAR EL BOTON Y ALERTAR AL USUARIO SI FALLA LA CONEXION DE RED
        btn.style.pointerEvents = 'auto';
        btn.innerHTML = originalText;
        alert("⚠️ Error de conexión con el servidor.");
        console.error('Error:', error);
    });
});
