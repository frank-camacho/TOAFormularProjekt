document.addEventListener('DOMContentLoaded', () => {
    /**
     * Muestra una pestaña específica y oculta las demás.
     * @param {string} tabId - ID de la pestaña a mostrar.
     */
    window.showTab = function (tabId) {
        console.log(`Mostrando pestaña: ${tabId}`);
        
        // Ocultar todo el contenido de las pestañas
        document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));

        // Eliminar la clase activa de todos los botones
        document.querySelectorAll('.tabs button').forEach(button => button.classList.remove('active'));

        // Mostrar la pestaña seleccionada
        const selectedTab = document.getElementById(tabId);
        if (selectedTab) {
            selectedTab.classList.add('active');
        } else {
            console.warn(`⚠️ La pestaña con ID "${tabId}" no existe.`);
            return; // Salir si la pestaña no existe
        }

        // Añadir la clase activa al botón correspondiente
        const selectedButton = document.querySelector(`.tabs button[data-tab="${tabId}"]`);
        if (selectedButton) {
            selectedButton.classList.add('active');
        } else {
            console.warn(`⚠️ El botón para la pestaña "${tabId}" no existe.`);
        }

        // Inicializar contenido de la pestaña si es necesario
        initializeTabContent(tabId);
    };

    /**
     * Inicializa el contenido específico de una pestaña si es necesario.
     * @param {string} tabId - ID de la pestaña a inicializar.
     */
    function initializeTabContent(tabId) {
        if (tabId === 'tab-rma-list') {
            console.log('Inicializando tabla de RMAs en la pestaña seleccionada...');
            try {
                initializeTable('rmaTable'); // Inicializa DataTables
            } catch (error) {
                console.error(`❌ Error al inicializar la tabla de RMAs: ${error.message}`);
            }
        } else if (tabId === 'tab-summary') {
            console.log('Pestaña de resumen seleccionada, verificando datos...');
            try {
                const chartData = {
                    labels: ['Neu', 'In Arbeit', 'Abgeschlossen'],
                    values: [
                        parseInt(document.getElementById('stat-new')?.textContent || 0),
                        parseInt(document.getElementById('stat-in-progress')?.textContent || 0),
                        parseInt(document.getElementById('stat-completed')?.textContent || 0)
                    ]
                };
                initializeChart('rmaChart', chartData); // Llamar a la función para actualizar el gráfico
            } catch (error) {
                console.error(`❌ Error al actualizar el gráfico de resumen: ${error.message}`);
            }
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
});
