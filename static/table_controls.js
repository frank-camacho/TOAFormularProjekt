document.addEventListener('DOMContentLoaded', function () {
    // Función para inicializar DataTables
    window.initializeTable = function (tableId) {
        const table = document.getElementById(tableId);
        if (table) {
            try {
                console.log(`Inicializando DataTables para la tabla: ${tableId}...`);
                $(table).DataTable({
                    autoWidth: true,
                    paging: true,
                    searching: true,
                    ordering: true,
                    lengthMenu: [5, 10, 25, 50],
                    language: {
                        url: "/static/german.json"
                    },
                    columnDefs: [
                        { targets: '_all', defaultContent: 'N/A' } // Manejar celdas vacías
                    ]
                });
                console.log(`✅ DataTables inicializado correctamente para: ${tableId}`);
            } catch (error) {
                console.error(`❌ Error al inicializar DataTables para ${tableId}:`, error);
            }
        } else {
            console.warn(`⚠️ Tabla con ID ${tableId} no encontrada para inicializar DataTables.`);
        }
    };

    // Filtro de búsqueda para tablas simples
    const searchInput = document.getElementById('searchInput');
    const simpleTable = document.getElementById('simpleTable'); // Tabla específica sin DataTables

    if (searchInput && simpleTable) {
        searchInput.addEventListener('keyup', function () {
            const filter = this.value.toLowerCase();
            const rows = simpleTable.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const cells = Array.from(row.getElementsByTagName('td'));
                const match = cells.some(cell => cell.textContent.toLowerCase().includes(filter));
                row.style.display = match ? '' : 'none';
            });
        });
    }

    // Ordenamiento por columna para tablas simples
    window.sortTable = function (tableId, columnIndex) {
        const table = document.getElementById(tableId);
        if (!table) return;

        const rows = Array.from(table.rows).slice(1); // Excluir la fila de encabezado
        const sortedRows = rows.sort((a, b) => {
            const aText = a.cells[columnIndex].textContent.trim();
            const bText = b.cells[columnIndex].textContent.trim();
            return isNaN(aText) || isNaN(bText)
                ? aText.localeCompare(bText)
                : parseFloat(aText) - parseFloat(bText);
        });
        table.tBodies[0].append(...sortedRows);
    };

    // Paginación para tablas simples
    const rowsPerPage = 10;
    let currentPage = 1;

    function paginate(tableId) {
        const table = document.getElementById(tableId);
        if (!table) return;

        const rows = Array.from(table.rows).slice(1); // Excluir encabezado
        const totalPages = Math.ceil(rows.length / rowsPerPage);

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
                paginate(tableId);
            });
            pagination.appendChild(button);
        }
    }

    // Inicializar DataTables y tablas simples
    const dataTables = document.querySelectorAll('.datatable'); // Clases de tablas para DataTables
    dataTables.forEach(table => initializeTable(table.id));

    paginate('simpleTable'); // Solo para tablas simples
});
