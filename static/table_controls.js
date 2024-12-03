// Filtro de búsqueda
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const table = document.getElementById('tabla_resultados');

    if (searchInput && table) {
        searchInput.addEventListener('keyup', function () {
            const filter = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                const cells = Array.from(row.getElementsByTagName('td'));
                const match = cells.some(cell => cell.textContent.toLowerCase().includes(filter));
                row.style.display = match ? '' : 'none';
            });
        });
    }

    // Ordenamiento por columna
    window.sortTable = function (columnIndex) {
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

    // Paginación
    const rowsPerPage = 10;
    let currentPage = 1;

    function paginate() {
        const rows = Array.from(table.rows).slice(1); // Excluir encabezado
        const totalPages = Math.ceil(rows.length / rowsPerPage);

        rows.forEach((row, index) => {
            row.style.display = index >= (currentPage - 1) * rowsPerPage && index < currentPage * rowsPerPage ? '' : 'none';
        });

        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = i;
            button.classList.toggle('active', i === currentPage);
            button.addEventListener('click', () => {
                currentPage = i;
                paginate();
            });
            pagination.appendChild(button);
        }
    }

    paginate();
});
