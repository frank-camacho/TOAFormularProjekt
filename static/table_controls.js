import {
    initializeTable,
    destroyTable,
    filterSimpleTable,
    sortSimpleTable,
    paginateSimpleTable
} from './modules/tableUtils.js';

document.addEventListener('DOMContentLoaded', () => {
    /**
     * Inicializar DataTables en todas las tablas con la clase 'datatable'.
     */
    const dataTables = document.querySelectorAll('.datatable');
    dataTables.forEach(table => {
        console.log(`Inicializando DataTables para la tabla: ${table.id}`);
        initializeTable(table.id);
    });

    /**
     * Filtro y ordenamiento para tablas simples.
     */
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', () => {
            const query = searchInput.value;
            filterSimpleTable('simpleTable', query);
        });
    }

    const sortButtons = document.querySelectorAll('.sort-button');
    sortButtons.forEach(button => {
        button.addEventListener('click', () => {
            const columnIndex = parseInt(button.getAttribute('data-column-index'), 10);
            sortSimpleTable('simpleTable', columnIndex);
        });
    });

    /**
     * Configurar paginación manual para tablas simples.
     */
    const table = document.getElementById('simpleTable');
    if (table) {
        paginateSimpleTable('simpleTable', 10);
    } else {
        console.warn('⚠️ Tabla con ID "simpleTable" no encontrada para la paginación.');
    }

    /**
     * Debugging logs para verificar el estado inicial.
     */
    const rows = document.querySelectorAll('#rmaTable tbody tr');
    console.log('Filas en la tabla antes de DataTables:', rows.length, rows);
    console.log('Contenido del tbody antes de inicializar DataTables:', document.querySelector('#rmaTable tbody').innerHTML);
    console.log(`¿Existe instancia previa de DataTables?`, $.fn.DataTable.isDataTable('#rmaTable'));
});
