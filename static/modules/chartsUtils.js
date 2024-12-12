// Registro global para múltiples gráficos
const chartsRegistry = {};

/**
 * Inicializa un gráfico en un canvas específico.
 * @param {string} chartElementId - ID del elemento canvas.
 * @param {Object} data - Datos para el gráfico.
 * @param {Array} data.labels - Etiquetas del gráfico.
 * @param {Array} data.values - Valores del gráfico.
 * @param {Array} [data.colors] - Colores opcionales para las secciones.
 */
export function initializeChart(chartElementId, data) {
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
        // Destruir gráfico anterior si existe
        if (chartsRegistry[chartElementId]) {
            console.warn(`⚠️ El gráfico ya existe en "${chartElementId}". Destruyendo el gráfico existente...`);
            destroyChart(chartElementId);
        }

        const ctx = chartElement.getContext('2d');
        chartsRegistry[chartElementId] = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'RMA Status',
                    data: data.values,
                    backgroundColor: data.colors || ['#FF6384', '#36A2EB', '#FFCE56']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        console.log(`✅ Gráfico de pastel cargado correctamente en el elemento: ${chartElementId}`);
    } catch (error) {
        console.error(`❌ Error al cargar el gráfico en ${chartElementId}:`, error);
    }
}

export function getChartData() {
    const newCount = parseInt(document.getElementById('stat-new')?.textContent || 0, 10);
    const inProgressCount = parseInt(document.getElementById('stat-in-progress')?.textContent || 0, 10);
    const completedCount = parseInt(document.getElementById('stat-completed')?.textContent || 0, 10);

    console.log('Valores extraídos del DOM:', { newCount, inProgressCount, completedCount });

    return {
        labels: ['Neu', 'In Arbeit', 'Abgeschlossen'],
        values: [newCount, inProgressCount, completedCount]
    };
}

/**
 * Destruye un gráfico existente por su ID.
 * @param {string} chartElementId - ID del gráfico a destruir.
 */
export function destroyChart(chartElementId) {
    if (chartsRegistry[chartElementId]) {
        console.warn(`🛠️ Destruyendo gráfico existente en "${chartElementId}"...`);
        chartsRegistry[chartElementId].destroy();
        delete chartsRegistry[chartElementId];
    }
}
