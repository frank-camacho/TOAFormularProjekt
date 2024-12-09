document.addEventListener('DOMContentLoaded', () => {
    // Inicializar DataTables para resultados generales
    const resultsTable = document.getElementById('resultsTable');
    if (resultsTable) {
        try {
            console.log("Inicializando DataTables para la tabla de resultados...");
            const headers = Array.from(resultsTable.querySelectorAll('thead th')).map(th => th.textContent);
            const rows = Array.from(resultsTable.querySelectorAll('tbody tr')).map(tr =>
                Array.from(tr.querySelectorAll('td')).map(td => td.textContent)
            );

            console.log("Encabezados detectados:", headers);

            let discrepanciesFound = false; // Para rastrear discrepancias

            rows.forEach((row, index) => {
                console.log(`Fila ${index + 1}:`, row);
                if (row.length !== headers.length) {
                    discrepanciesFound = true;
                    console.error(
                        `⚠️ Desajuste en la fila ${index + 1}: ${row.length} columnas en lugar de ${headers.length}`,
                        row
                    );
                }
            });

            if (!discrepanciesFound) {
                console.log("✅ Todas las filas tienen un número de columnas consistente con los encabezados.");
            } else {
                console.warn("⚠️ Existen discrepancias entre los encabezados y las filas. Revisa los datos.");
            }

            $(resultsTable).DataTable({
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
        } catch (error) {
            console.error('❌ Error al inicializar DataTables:', error);
        }
    } else {
        console.warn("⚠️ Tabla de resultados no encontrada. DataTables no se inicializó.");
    }

    // Inicializar DataTables para empleados
    const employeesTable = document.getElementById('employeesTable');
    if (employeesTable) {
        try {
            console.log("Inicializando DataTables para la tabla de empleados...");
            $(employeesTable).DataTable({
                paging: true,
                searching: true,
                ordering: true,
                lengthMenu: [5, 10, 25],
                language: {
                    url: "/static/german.json"
                },
                columnDefs: [
                    { targets: '_all', defaultContent: 'N/A' } // Manejar celdas vacías
                ]
            });
            console.log("✅ DataTables para empleados inicializado correctamente.");
        } catch (error) {
            console.error("❌ Error al inicializar DataTables para empleados:", error);
        }
    }

    // Gráfico de pastel
    const chartElement = document.getElementById('rmaChart');
    if (chartElement) {
        console.log("Cargando gráfico de pastel...");
        try {
            const newCount = parseInt(document.getElementById('stat-new')?.value || 0);
            const inProgressCount = parseInt(document.getElementById('stat-in-progress')?.value || 0);
            const completedCount = parseInt(document.getElementById('stat-completed')?.value || 0);

            if (isNaN(newCount) || isNaN(inProgressCount) || isNaN(completedCount)) {
                throw new Error("Los valores para el gráfico son inválidos.");
            }

            const ctx = chartElement.getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Neu', 'In Arbeit', 'Abgeschlossen'],
                    datasets: [{
                        label: 'RMA Status',
                        data: [newCount, inProgressCount, completedCount],
                        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        }
                    }
                }
            });

            console.log("✅ Gráfico de pastel cargado correctamente.");
        } catch (error) {
            console.error('❌ Error al cargar el gráfico:', error);
        }
    } else {
        console.warn("⚠️ Elemento de gráfico no encontrado. El gráfico de pastel no se cargó.");
    }

    console.log("Si los errores persisten, verifica la consola del navegador para más detalles.");
});
