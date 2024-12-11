/**
 * Función para inicializar un gráfico.
 * @param {string} chartElementId - ID del elemento canvas donde se renderizará el gráfico.
 * @param {Object} data - Datos para el gráfico.
 * @param {Array} data.labels - Etiquetas del gráfico.
 * @param {Array} data.values - Valores del gráfico.
 * @param {Array} [data.colors] - Colores opcionales para las secciones del gráfico.
 */
function initializeChart(chartElementId, data) {
    const chartElement = document.getElementById(chartElementId);
    if (!chartElement) {
        console.error(`❌ Elemento de gráfico con ID "${chartElementId}" no encontrado.`);
        return;
    }

    if (!data || !Array.isArray(data.labels) || !Array.isArray(data.values)) {
        console.error("❌ Datos para el gráfico no son válidos. Se esperan 'labels' y 'values' como arreglos.");
        return;
    }

    try {
        const ctx = chartElement.getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'RMA Status',
                    data: data.values,
                    backgroundColor: data.colors || ['#FF6384', '#36A2EB', '#FFCE56'], // Colores predeterminados
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });

        console.log(`✅ Gráfico de pastel cargado correctamente en el elemento: ${chartElementId}`);
    } catch (error) {
        console.error(`❌ Error al cargar el gráfico en ${chartElementId}:`, error);
    }
}

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    // Ejemplo: Inicializar el gráfico 'rmaChart' con datos estáticos o desde el servidor
    const chartData = {
        labels: ['Neu', 'In Arbeit', 'Abgeschlossen'],
        values: [10, 20, 30], // Reemplazar con datos reales del servidor
    };
    initializeChart('rmaChart', chartData);
});
