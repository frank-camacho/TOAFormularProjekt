// Importar dependencias necesarias
import { destroyTable, initializeTable } from './tableUtils.js';
import { destroyChart, initializeChart } from './chartsUtils.js';

// Gestiona la visibilidad de pestañas y contenido
export function resetTabs() {
    console.log('Reseteando todas las pestañas y botones...');

    // Ocultar todo el contenido de las pestañas
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));

    // Quitar clase activa de todos los botones
    document.querySelectorAll('.tabs button').forEach(button => button.classList.remove('active'));
}

// Activa una pestaña específica
export function activateTab(tabId) {
    const selectedTab = document.getElementById(tabId);
    const selectedButton = document.querySelector(`.tabs button[data-tab="${tabId}"]`);

    if (selectedTab) {
        selectedTab.classList.add('active');
        console.log(`Pestaña "${tabId}" activada.`);
    } else {
        console.warn(`⚠️ La pestaña con ID "${tabId}" no existe.`);
    }

    if (selectedButton) {
        selectedButton.classList.add('active');
    } else {
        console.warn(`⚠️ El botón para la pestaña "${tabId}" no existe.`);
    }
}

// Obtiene los datos necesarios para inicializar el gráfico
export function getChartData() {
    try {
        const labels = ['Neu', 'In Arbeit', 'Abgeschlossen'];
        const values = [
            parseInt(document.getElementById('stat-new')?.textContent || 0, 10),
            parseInt(document.getElementById('stat-in-progress')?.textContent || 0, 10),
            parseInt(document.getElementById('stat-completed')?.textContent || 0, 10)
        ];

        console.log('Datos obtenidos para el gráfico:', { labels, values });
        return { labels, values };
    } catch (error) {
        console.error('❌ Error al obtener datos para el gráfico:', error);
        return { labels: [], values: [] };
    }
}

// Inicializa el contenido de una pestaña según su ID
export function initializeTabContent(tabId) {
    switch (tabId) {
        case 'tab-rma-list':
            console.log('Inicializando tabla de RMAs...');
            try {
                destroyTable('rmaTable');
                initializeTable('rmaTable');
            } catch (error) {
                console.error(`❌ Error al inicializar la tabla: ${error.message}`);
            }
            break;

        case 'tab-summary':
            console.log('Inicializando gráfico de resumen...');
            try {
                const chartData = getChartData();
                destroyChart('rmaChart');
                initializeChart('rmaChart', chartData);
            } catch (error) {
                console.error(`❌ Error al inicializar el gráfico: ${error.message}`);
            }
            break;

        default:
            console.warn(`⚠️ ID de pestaña desconocido: "${tabId}"`);
            break;
    }
}

// Configura la pestaña activa por defecto al cargar la página
export function initializeDefaultTab() {
    const defaultTab = document.querySelector('.tabs button.active');
    if (defaultTab) {
        const defaultTabId = defaultTab.getAttribute('data-tab');
        console.log(`Inicializando la pestaña activa por defecto: ${defaultTabId}`);
        activateTab(defaultTabId);
        initializeTabContent(defaultTabId);
    } else {
        console.warn('⚠️ No se encontró una pestaña activa por defecto.');
    }
}
