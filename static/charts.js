// Importar funciones del módulo chartUtils.js
import { initializeChart, destroyChart } from './modules/chartsUtils.js';

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    // Ejemplo: Datos iniciales para el gráfico
    const chartData = {
        labels: ['Neu', 'In Arbeit', 'Abgeschlossen'],
        values: [
            parseInt(document.getElementById('stat-new')?.textContent || 0, 10),
            parseInt(document.getElementById('stat-in-progress')?.textContent || 0, 10),
            parseInt(document.getElementById('stat-completed')?.textContent || 0, 10)
        ]
    };

    console.log('Datos enviados al gráfico:', chartData);

    // Verificar y destruir gráfico previo si existe (opcional, ya manejado en el módulo)
    destroyChart('rmaChart');

    console.log('Datos procesados para el gráfico:', JSON.stringify(chartData, null, 2));

    // Inicializar el gráfico
    initializeChart('rmaChart', chartData);
});
