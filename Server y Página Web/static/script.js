document.getElementById('garmentForm').addEventListener('submit', function(e) {
    const btn = this.querySelector('.btn-submit');
    const originalText = btn.innerHTML;

    // Cambiar el estado del botón al enviar
    btn.style.pointerEvents = 'none';
    btn.innerHTML = '<span>Extrayendo...</span> <i class="fas fa-spinner fa-spin"></i>';

    
    //Para probar la animación sin recargar la página, descomentar la línea de abajo:
    // e.preventDefault(); 
});
