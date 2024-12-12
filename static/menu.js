// Importar funciones desde utils
import { resetTabs, activateTab } from './modules/menuUtils.js';
import { destroyTable, initializeTable, cacheTableData, restoreTableData } from './modules/tableUtils.js';
import { destroyChart, initializeChart } from './modules/chartsUtils.js';

document.addEventListener('DOMContentLoaded', () => {
    const tableCache = {}; // Cache para guardar datos de tablas

    /**
     * Muestra una pestaña específica y maneja su contenido.
     * @param {string} tabId - ID de la pestaña a mostrar.
     */
    function showTab(tabId) {
        console.log(`Mostrando pestaña: ${tabId}`);

        // Validar si el ID de la pestaña existe
        const tabElement = document.getElementById(tabId);
        if (!tabElement) {
            console.warn(`⚠️ Pestaña con ID "${tabId}" no existe.`);
            return;
        }

        // Resetear y activar la pestaña
        resetTabs();
        activateTab(tabId);

        // Inicializar contenido de la pestaña
        try {
            initializeTabContent(tabId);
        } catch (error) {
            console.error(`❌ Error al inicializar el contenido de la pestaña "${tabId}": ${error.message}`);
        }
    }

    /**
     * Inicializa el contenido específico de una pestaña.
     * @param {string} tabId - ID de la pestaña a inicializar.
     */
    function initializeTabContent(tabId) {
        switch (tabId) {
            case 'tab-rma-list':
                console.log('Inicializando tabla de RMAs...');
                try {
                    if (tableCache['rmaTable']) {
                        restoreTableData('rmaTable', tableCache['rmaTable']);
                    } else {
                        initializeTable('rmaTable');
                        tableCache['rmaTable'] = cacheTableData('rmaTable');
                    }
                } catch (error) {
                    console.error(`❌ Error al inicializar la tabla de RMAs: ${error.message}`);
                }
                break;

            case 'tab-summary':
                console.log('Inicializando gráfico de resumen...');
                try {
                    const chartData = getChartData();
                    destroyChart('rmaChart');
                    initializeChart('rmaChart', chartData);
                } catch (error) {
                    console.error(`❌ Error al inicializar el gráfico de resumen: ${error.message}`);
                }
                break;

            default:
                console.warn(`⚠️ No se reconoce la pestaña con ID: "${tabId}"`);
                break;
        }
    }

    /**
     * Inicializa la pestaña activa por defecto al cargar la página.
     */
    function initializeDefaultTab() {
        const defaultTab = document.querySelector('.tabs button.active');
        if (defaultTab) {
            const defaultTabId = defaultTab.getAttribute('data-tab');
            console.log(`Inicializando la pestaña activa por defecto: ${defaultTabId}`);
            showTab(defaultTabId);
        } else {
            console.warn('⚠️ No se encontró una pestaña activa por defecto.');
        }
    }

    // Inicializar la pestaña activa por defecto
    initializeDefaultTab();

    // Exportar funciones globalmente si es necesario
    window.showTab = showTab;
});
