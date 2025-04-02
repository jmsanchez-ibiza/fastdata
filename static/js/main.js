document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener('htmx:afterSwap', (e) => {
        console.log("📦 Evento htmx:afterSwap recibido");

        const tables = document.querySelectorAll(".datatable");
        console.log("🔍 Buscando tablas .datatable...");

        tables.forEach(table => {
            console.log(`➡️ Inicializando DataTable para: #${table.id}`);
            
            if ($.fn.DataTable.isDataTable(table)) {
                console.warn("⚠️ Tabla ya inicializada. Destruyendo instancia existente.");

                // Destruir instancia anterior
                $(table).DataTable().destroy();

                // Clonar y reemplazar para limpiar restos de DataTable
                const clonedTable = table.cloneNode(true);
                table.parentElement.replaceChild(clonedTable, table);
                table = clonedTable;
            }

            // Inicializar DataTable con estilos Bootstrap
            const $table = $(table);
            $table.DataTable({
                renderer: 'bootstrap',
                language: {
                    decimal: ",",
                    processing: "Procesando...",
                    search: "Buscar:",
                    lengthMenu: "Mostrar _MENU_",
                    info: "Mostrando (_START_ a _END_) de _TOTAL_ registros",
                    infoEmpty: "No hay datos que mostrar.",
                    infoFiltered: "(filtrado de _MAX_ registros en total)",
                    loadingRecords: "Cargando...",
                    zeroRecords: "No se encontraron registros coincidentes",
                    emptyTable: "No hay datos disponibles en la tabla",
                    paginate: {
                        first: "<<",
                        previous: "<",
                        next: ">",
                        last: ">>"
                    },
                    aria: {
                        sortAscending: ": activar para ordenar la columna de manera ascendente",
                        sortDescending: ": activar para ordenar la columna de manera descendente"
                    }
                },
                layout: {
                    topStart: 'info',
                    topEnd: {
                        search: { placeholder: 'Buscar ...' }
                    },
                    bottomStart: 'pageLength',
                    bottomEnd: {
                        paging: { firstLast: false }
                    }
                }
            });

            // ✅ Establecer el foco en el campo de búsqueda de DataTables v2
            document.querySelector(`#${table.id}_wrapper .dt-search input`)?.focus();
        });
    });
});
