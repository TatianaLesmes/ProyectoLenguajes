btnBuscar.addEventListener('click', async () => {
    // Obtener valores de los inputs
    const placa = inputPlaca.value.trim();
    const colorFondo = selectColorFondo.value;
    const colorLetra = selectColorLetra.value;

    // Validar que todos los campos estén llenos
    if (!placa || colorFondo === 'Color de fondo' || colorLetra === 'Color de letra') {
        alert('Por favor completa todos los campos.');
        return;
    }

    try {
        // Limpiar solo el cuerpo de la tabla (tbody) antes de la nueva búsqueda
        const tbody = tablaResultados.querySelector('tbody');
        tbody.innerHTML = '';  // Esto limpia solo las filas de datos

        // Hacer la solicitud POST al backend
        const response = await fetch('http://127.0.0.1:5000/api/validate-plate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                placa,
                color_fondo: colorFondo,
                color_letra: colorLetra,
            }),
        });

        // Parsear la respuesta JSON
        const result = await response.json();

        // Verificar si la respuesta fue exitosa
        if (!result.success) {
            alert(`Error: ${result.message}`);
            return;
        }

        // Verificar si hay datos para mostrar
        if (result.data) {
            Swal.fire({ title: '¡Buen trabajo!', text: 'Has hecho clic en el botón', icon: 'success', confirmButtonText: 'Aceptar' });
            const vehiculo = result.data;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${vehiculo.placa}</td>
                <td>${vehiculo.servicio || 'N/A'}</td>
                <td>${vehiculo.departamento || 'N/A'}</td>
                <td>${vehiculo.ciudad || 'N/A'}</td>
                <td>${vehiculo.pais || 'N/A'}</td>
                <td>${vehiculo.color_fondo || 'N/A'}</td>
                <td>${vehiculo.color_letra || 'N/A'}</td>
            `;
            tbody.appendChild(row); // Añadir la fila al tbody
        } else {
            // Si no hay datos, mostrar mensaje en la tabla
            const row = document.createElement('tr');
            row.innerHTML = `
                <td colspan="7" class="text-center">No se encontraron resultados</td>
            `;
            tbody.appendChild(row); // Añadir la fila con mensaje al tbody
        }
    } catch (error) {
        // Manejar errores de red u otros problemas
        console.error('Error al conectar con el servidor:', error);
        alert('Error al conectar con el servidor. Por favor, inténtalo de nuevo.');
    }
});
