// JavaScript para el modal - Eliminación directa con fetch
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('deleteModal');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.btn-cancel');
    const confirmDelete = document.getElementById('confirmDelete');
    const materiaName = document.getElementById('materiaName');
    let currentMateriaId = null;
    let currentDeleteButton = null;

    // Abrir modal cuando se hace clic en "Eliminar"
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const materiaId = this.getAttribute('data-materia-id');
            const name = this.getAttribute('data-materia-name');
            
            materiaName.textContent = `"${name}"`;
            currentMateriaId = materiaId;
            currentDeleteButton = this;
            
            modal.style.display = 'flex';
        });
    });

    // Manejar la eliminación
    confirmDelete.addEventListener('click', function(e) {
        e.preventDefault();
        
        if (!currentMateriaId) return;
        
        // Mostrar loading
        confirmDelete.textContent = 'Eliminando...';
        confirmDelete.disabled = true;
        
        // Hacer la petición DELETE con fetch
        fetch(`/materia/materias/${currentMateriaId}/eliminar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `csrfmiddlewaretoken=${getCookie('csrftoken')}`
        })
        .then(response => {
            if (response.ok) {
                // Eliminar la fila de la tabla
                if (currentDeleteButton) {
                    const row = currentDeleteButton.closest('tr');
                    row.style.opacity = '0.5';
                    setTimeout(() => {
                        row.remove();
                        
                        // Recargar la página para actualizar la lista
                        window.location.reload();
                    }, 300);
                }
                
                // Cerrar modal
                closeModalFunc();
                
                // Mostrar mensaje de éxito (opcional)
                showMessage('Materia eliminada correctamente', 'success');
            } else {
                throw new Error('Error al eliminar');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('Error al eliminar la materia', 'error');
            confirmDelete.textContent = 'Sí, Eliminar';
            confirmDelete.disabled = false;
        });
    });

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Función para mostrar mensajes
    function showMessage(message, type) {
        // Crear elemento de mensaje
        const messageDiv = document.createElement('div');
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: var(--radius);
            color: white;
            font-weight: 500;
            z-index: 1001;
            animation: slideInRight 0.3s ease;
        `;
        
        if (type === 'success') {
            messageDiv.style.background = '#28a745';
        } else {
            messageDiv.style.background = '#dc3545';
        }
        
        document.body.appendChild(messageDiv);
        
        // Remover después de 3 segundos
        setTimeout(() => {
            messageDiv.remove();
        }, 3000);
    }

    // Cerrar modal
    function closeModalFunc() {
        modal.style.display = 'none';
        confirmDelete.textContent = 'Sí, Eliminar';
        confirmDelete.disabled = false;
        currentMateriaId = null;
        currentDeleteButton = null;
    }

    closeModal.addEventListener('click', closeModalFunc);
    cancelBtn.addEventListener('click', closeModalFunc);

    // Cerrar modal al hacer clic fuera
    modal.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModalFunc();
        }
    });

    // También cerrar con la tecla ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            closeModalFunc();
        }
    });
});