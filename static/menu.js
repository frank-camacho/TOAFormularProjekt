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
        return;
    }
    console.log('[DEBUG] Contenedor "session-status" encontrado en el DOM.');

    /**
     * Validar la sesión en el backend
     */
    console.log("[DEBUG] Comenzando la validación de la sesión...");
    fetch('/check_session', { cache: 'no-store' }) // Forzar que no utilice contenido en caché
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
                console.log('[DEBUG] Contenedor actualizado para sesión activa.');
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
                console.log('[DEBUG] Formulario de inicio de sesión mostrado.');
            }
        })
        .catch(error => {
            console.error('[ERROR] Validando sesión:', error);
            sessionStatusDiv.innerHTML = `
                <p style="color: red;">Fehler beim Laden des Sitzungsstatus.</p>
            `;
        });

    console.log('[DEBUG] Validación de sesión iniciada.');

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
            console.warn('⚠️ No se encontró una pestaña activa por defecto. (Esto es esperado si no se utilizan pestañas en esta página)');
        }
    }

    // Inicializar la pestaña activa por defecto
    initializeDefaultTab();

    // Exportar funciones globalmente si es necesario
    window.showTab = showTab;
});
