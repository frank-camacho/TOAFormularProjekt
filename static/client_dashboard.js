console.log("client_dashboard.js cargado correctamente.");

document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM cargado y listo.");

    const buttons = document.querySelectorAll(".history-button");
    console.log(`Se encontraron ${buttons.length} botones.`);

    buttons.forEach(button => {
        button.addEventListener("click", function() {
            console.log("Botón clickeado, ID:", this.getAttribute("data-id"));
            const rmaId = this.getAttribute("data-id");

            // Hacer la petición AJAX al servidor
            fetch(`/client/repair_history/${rmaId}`)
                .then(response => response.json())
                .then(data => {
                    console.log("Datos recibidos del servidor:", data);
                    const tableBody = document.querySelector("#history-table tbody");
                    tableBody.innerHTML = ""; // Limpiar la tabla

                    // Insertar filas en la tabla con las nuevas columnas
                    data.forEach(row => {
                        tableBody.innerHTML += `
                            <tr>
                                <td>${row.rma_id || "N/A"}</td>
                                <td>${row.technician_name || "N/A"}</td>
                                <td>${row.repair_status || "N/A"}</td>
                                <td>${row.used_parts || "N/A"}</td>
                                <td>${row.duration || "0"} Stunden</td>
                                <td>${row.next_steps || "N/A"}</td>
                                <td>${row.ZOR || "N/A"}</td>
                                <td>${row.Lieferscheinnummer || "N/A"}</td>
                                <td>${row.comments || "N/A"}</td>
                                <td>${row.cost || "0.00"} €</td>
                                <td>${row.created_at || "N/A"}</td>
                            </tr>`;
                    });                    

                    openModal();
                })
                .catch(error => {
                    console.error("Error al cargar el historial:", error);
                    alert("Fehler beim Laden des Reparaturverlaufs.");
                });
        });
    });

    // Función para abrir el modal
    function openModal() {
        console.log("Abriendo el modal...");
        document.getElementById("history-modal").style.display = "block";
    }

    // Función para cerrar el modal
    document.getElementById("close-modal").addEventListener("click", function() {
        console.log("Cerrando el modal...");
        document.getElementById("history-modal").style.display = "none";
    });
});
