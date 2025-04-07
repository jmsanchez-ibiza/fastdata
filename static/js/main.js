document.addEventListener("DOMContentLoaded", () => {
    document.body.addEventListener('htmx:afterSwap', (e) => {
        console.log("📦 htmx:afterSwap event received");

        const tables = document.querySelectorAll(".datatable");
        console.log("🔍 Looking for .datatable...");

        tables.forEach(table => {
            console.log(`➡️ Init DataTable for: #${table.id}`);
            
            if ($.fn.DataTable.isDataTable(table)) {
                console.warn("⚠️ Table already initialized. Destroying existing instance.");

                $(table).DataTable().destroy();

                const clonedTable = table.cloneNode(true);
                table.parentElement.replaceChild(clonedTable, table);
                table = clonedTable;
            }

            const $table = $(table);
            // DataTable configuration in Spanish
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
                        search: { placeholder: 'Buscar ...' },
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
                        htmx.process(row); // 🔥 this reactivates the buttons in each visible row
                    });
                },
                // dom: 'Bfrtip',
                // buttons: [
                //     {
                //         extend: 'excelHtml5',
                //         text: '<i class="bi bi-file-earmark-excel"></i> Export records',
                //         className: 'btn btn-success btn-sm',
                //         exportOptions: {
                //             modifier: {
                //                 page: 'current'  // Solo exporta los visibles
                //             }
                //         }
                //     }
                // ],
            });

            // Focus on search field
            document.querySelector(`#${table.id}_wrapper .dt-search input`)?.focus();
        });
    });
});
