// Importar funciones desde utils
import { resetTabs, activateTab } from './modules/menuUtils.js';
import { destroyTable, initializeTable, cacheTableData, restoreTableData } from './modules/tableUtils.js';
import { destroyChart, initializeChart } from './modules/chartsUtils.js';

document.addEventListener('DOMContentLoaded', () => {
    const tableCache = {}; // Cache para guardar datos de tablas
    const sessionStatusDiv = document.getElementById('session-status');

    // Validar si el contenedor existe en el DOM
    if (!sessionStatusDiv) {
        console.error('[ERROR] El contenedor "session-status" no se encontró en el DOM.');
    } else {
        console.log('[DEBUG] Contenedor "session-status" encontrado en el DOM.');

        // Validar la sesión en el backend
        console.log("[DEBUG] Comenzando la validación de la sesión...");
        fetch('/check_session', { cache: 'no-store' })
            .then(response => response.json())
            .then(data => {
                console.log(`[DEBUG] Respuesta de /check_session: ${JSON.stringify(data)}`);
                sessionStatusDiv.innerHTML = ''; // Limpiar el contenido previo
                if (data.session_active) {
                    console.log('[DEBUG] Actualizando el contenedor para sesión activa.');
                    sessionStatusDiv.innerHTML = `
                        <h2>Hallo, Benutzer!</h2>
                        <p>Ihre Sitzung ist aktiv. Möchten Sie fortfahren oder sich abmelden?</p>
                        <a href="/employee/dashboard">
                            <button type="button" class="form-button">Zum Dashboard</button>
                        </a>
                        <a href="/logout">
                            <button type="button" class="form-button">Abmelden</button>
                        </a>
                    `;
                } else {
                    console.log('[DEBUG] Mostrando formulario de inicio de sesión.');
                    sessionStatusDiv.innerHTML = `
                        <div id="login-form" style="margin-top: 40px; width: 20%;" class="center">
                            <h2>Login</h2>
                            <form action="/login" method="POST" class="rma-form">
                                <div class="form-group">
                                    <input type="text" name="username" placeholder="Benutzername" required class="form-input" autocomplete="username">
                                </div>
                                <div class="form-group">
                                    <input type="password" name="password" placeholder="Passwort" required class="form-input" autocomplete="current-password">
                                </div>
                                <button type="submit" class="form-button" style="text-align: center; width: 50%;">Anmelden</button>
                            </form>
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('[ERROR] Validando sesión:', error);
                sessionStatusDiv.innerHTML = `
                    <p style="color: red;">Fehler beim Laden des Sitzungsstatus.</p>
                `;
            });
    }

    // Nueva lógica para manejar el menú desplegable
    const menuToggle = document.getElementById('menu-toggle');
    const dropdownMenu = document.getElementById('dropdown-menu');

    if (menuToggle && dropdownMenu) {
        console.log('[DEBUG] Elementos del menú encontrados:', { menuToggle, dropdownMenu });

        menuToggle.addEventListener('click', () => {
            console.log('[DEBUG] Botón de menú clickeado.');
            dropdownMenu.classList.toggle('hidden');
        });

        // Cerrar el menú si se hace clic fuera de él
        document.addEventListener('click', (event) => {
            if (!menuToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
                console.log('[DEBUG] Haciendo clic fuera del menú. Cerrando.');
                dropdownMenu.classList.add('hidden');
            }
        });
    } else {
        console.warn('[WARN] Elementos del menú desplegable no encontrados en el DOM.');
    }

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

    // Inicializar la pestaña activa por defecto
    initializeDefaultTab();

    // Exportar funciones globalmente si es necesario
    window.showTab = showTab;
});
