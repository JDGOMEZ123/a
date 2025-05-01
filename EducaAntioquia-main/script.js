function handleNavClick(page) {
    // Actualizar el estado de la sesión
    window.parent.postMessage({
        type: 'streamlit:setSessionState',
        data: {
            current_page: page
        }
    }, '*');
    
    // Recargar la página para aplicar los cambios
    window.parent.postMessage({
        type: 'streamlit:rerun'
    }, '*');
} 