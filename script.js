document.getElementById('garmentForm').addEventListener('submit', function(e) {
    const btn = this.querySelector('.btn-submit');
    const originalText = btn.innerHTML;

    // Cambiar el estado del botón al enviar
    btn.style.pointerEvents = 'none';
    btn.innerHTML = '<span>Extrayendo...</span> <i class="fas fa-spinner fa-spin"></i>';

    // Nota: El formulario se enviará normalmente al servidor.
    // Si quieres probar la animación sin recargar la página, 
    // descomenta la línea de abajo:
    // e.preventDefault(); 
});