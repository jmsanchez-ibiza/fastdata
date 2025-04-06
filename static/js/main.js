document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener('htmx:afterSwap', (e) => {
        console.log("📦 Evento htmx:afterSwap recibido");

        const tables = document.querySelectorAll(".datatable");
        console.log("🔍 Buscando tablas .datatable...");

        tables.forEach(table => {
            console.log(`➡️ Inicializando DataTable para: #${table.id}`);
            
            if ($.fn.DataTable.isDataTable(table)) {
                console.warn("⚠️ Tabla ya inicializada. Destruyendo instancia existente.");

                $(table).DataTable().destroy();

                const clonedTable = table.cloneNode(true);
                table.parentElement.replaceChild(clonedTable, table);
                table = clonedTable;
            }

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
                },
                initComplete: function () {
                    htmx.process(this.api().table().node());
                },
                drawCallback: function () {
                    const rows = this.api().rows({ page: 'current' }).nodes();
                    rows.each(function (row) {
                        htmx.process(row); // 🔥 esto reactiva los botones en cada fila visible
                    });
                }
            });

            // Foco en campo de búsqueda
            document.querySelector(`#${table.id}_wrapper .dt-search input`)?.focus();
        });
    });
});
