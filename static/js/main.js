// Código JS
// Esperar a que el DOM esté completamente cargado
document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ main.js cargado y DOM listo");

    // Función para inicializar todas las tablas con clase 'datatable'
    function initializeAllDataTables() {
        console.log("🔍 Buscando tablas .datatable...");

        document.querySelectorAll('.datatable').forEach(table => {
            console.log(`➡️ Inicializando DataTable para: #${table.id || '(sin id)'}`);

            const $table = $(table);

            // Destruir instancia previa si ya está inicializada
            if ($.fn.DataTable.isDataTable(table)) {
                console.log(`⚠️ Tabla ya inicializada. Destruyendo instancia existente.`);
                $table.DataTable().destroy();
            }

            // Inicializar nueva instancia
            $table.DataTable({
                renderer: 'bootstrap',  // 🔥 Este es el cambio clave
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
                        search: {
                            placeholder: 'Buscar ...'
                        }
                    },
                    bottomStart: 'pageLength',
                    bottomEnd: {
                        paging: { firstLast: false }
                    },
                }
            });
        });
    }

    // Inicializar DataTables al cargar contenido nuevo con HTMX
    document.body.addEventListener('htmx:afterSwap', (e) => {
        console.log("📦 Evento htmx:afterSwap recibido");
        initializeAllDataTables();
    });

    // Inicializar DataTables en la primera carga de página
    initializeAllDataTables();
});
