// Registro global para instancias de DataTables
const tableRegistry = {};

/**
 * Inicializa DataTables para una tabla específica.
 * @param {string} tableId - ID de la tabla a inicializar.
 * @param {Object} [options] - Opciones adicionales para DataTables.
 */
export function initializeTable(tableId, options = {}) {
    const table = document.getElementById(tableId);
    if (!table) {
        console.warn(`⚠️ Tabla con ID "${tableId}" no encontrada para inicializar DataTables.`);
        return;
    }

    try {
        // Verificar si DataTables ya está inicializado
        if ($.fn.DataTable.isDataTable(`#${tableId}`)) {
            console.warn(`⚠️ DataTables ya estaba inicializado en la tabla: ${tableId}. Reiniciando...`);
            destroyTable(tableId);
        }

        // Opciones predeterminadas combinadas con las opciones proporcionadas
        const defaultOptions = {
            autoWidth: true,
            paging: true,
            searching: true,
            ordering: true,
            lengthMenu: [5, 10, 25, 50],
            language: { url: "/static/german.json" },
            columnDefs: [{ targets: '_all', defaultContent: 'N/A' }]
        };

        const finalOptions = { ...defaultOptions, ...options };

        // Inicializar DataTables
        tableRegistry[tableId] = $(table).DataTable(finalOptions);
        console.log(`✅ DataTables inicializado correctamente para: ${tableId}`);
    } catch (error) {
        console.error(`❌ Error al inicializar DataTables para ${tableId}:`, error);
    }
}

/**
 * Destruye una instancia de DataTables para liberar recursos.
 * @param {string} tableId - ID de la tabla a destruir.
 */
export function destroyTable(tableId) {
    if (tableRegistry[tableId]) {
        console.log(`🛠️ Destruyendo DataTables en la tabla: ${tableId}...`);
        tableRegistry[tableId].clear().destroy();
        delete tableRegistry[tableId];
    } else if ($.fn.DataTable.isDataTable(`#${tableId}`)) {
        console.warn(`⚠️ Destruyendo instancia huérfana de DataTables en la tabla: ${tableId}...`);
        $(`#${tableId}`).DataTable().clear().destroy();
    }
}

/**
 * Guarda los datos de una tabla en el caché.
 * @param {string} tableId - ID de la tabla.
 * @returns {Array} Datos de la tabla.
 */
export function cacheTableData(tableId) {
    if (!tableRegistry[tableId]) {
        console.warn(`⚠️ No se encontró una instancia de DataTables para la tabla: ${tableId}`);
        return [];
    }

    const table = tableRegistry[tableId];
    return table ? table.data().toArray() : [];
}

/**
 * Restaura los datos en una tabla desde el caché.
 * @param {string} tableId - ID de la tabla.
 * @param {Array} data - Datos a restaurar.
 */
export function restoreTableData(tableId, data) {
    if (!tableRegistry[tableId]) {
        console.warn(`⚠️ No se encontró una instancia de DataTables para la tabla: ${tableId}`);
        return;
    }

    const table = tableRegistry[tableId];
    table.clear();
    table.rows.add(data);
    table.draw();
}

/**
 * Filtra filas de una tabla simple (sin DataTables).
 * @param {string} tableId - ID de la tabla.
 * @param {string} query - Texto a buscar en la tabla.
 */
export function filterSimpleTable(tableId, query) {
    const table = document.getElementById(tableId);
    if (!table) {
        console.warn(`⚠️ Tabla con ID "${tableId}" no encontrada para el filtro.`);
        return;
    }

    const rows = Array.from(table.querySelectorAll('tbody tr'));
    const filter = query.toLowerCase();

    rows.forEach(row => {
        const cells = Array.from(row.getElementsByTagName('td'));
        const match = cells.some(cell => cell.textContent.toLowerCase().includes(filter));
        row.style.display = match ? '' : 'none';
    });
}

/**
 * Ordena filas de una tabla simple (sin DataTables) por una columna específica.
 * @param {string} tableId - ID de la tabla.
 * @param {number} columnIndex - Índice de la columna por la que ordenar.
 */
export function sortSimpleTable(tableId, columnIndex) {
    const table = document.getElementById(tableId);
    if (!table) {
        console.warn(`⚠️ Tabla con ID "${tableId}" no encontrada para ordenar.`);
        return;
    }

    const rows = Array.from(table.rows).slice(1); // Excluir encabezado
    const sortedRows = rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        return isNaN(aText) || isNaN(bText)
            ? aText.localeCompare(bText)
            : parseFloat(aText) - parseFloat(bText);
    });

    table.tBodies[0].append(...sortedRows);
}

/**
 * Configura paginación manual para tablas simples (sin DataTables).
 * @param {string} tableId - ID de la tabla.
 * @param {number} rowsPerPage - Número de filas por página.
 */
export function paginateSimpleTable(tableId, rowsPerPage) {
    const table = document.getElementById(tableId);
    if (!table) {
        console.warn(`⚠️ Tabla con ID "${tableId}" no encontrada para la paginación.`);
        return;
    }

    const rows = Array.from(table.rows).slice(1); // Excluir encabezado
    const totalPages = Math.ceil(rows.length / rowsPerPage);
    let currentPage = 1;

    function updatePagination() {
        rows.forEach((row, index) => {
            row.style.display = index >= (currentPage - 1) * rowsPerPage && index < currentPage * rowsPerPage ? '' : 'none';
        });

        const pagination = document.getElementById(`${tableId}-pagination`);
        if (!pagination) return;

        pagination.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.classList.toggle('active', i === currentPage);
            button.addEventListener('click', () => {
                currentPage = i;
                updatePagination();
            });
            pagination.appendChild(button);
        }
    }

    updatePagination();
}
