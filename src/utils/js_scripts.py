from fasthtml.common import *

# Enable Bootstrap ToolTips
bootstrap_tooltips_js = Script(
    code="""
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
    """
)

# Allows scrolling and centering the desired object on the screen
scroll_to_id_js = Script(
    code='''
    function scrollToId(objId) {
        if (!objId || objId === 'id-0') {
            // If there's no ID, scroll to the bottom of the page
            window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
        } else {
            const row = document.getElementById(objId);
            if (row) {
                row.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        }
    }
    '''
)

# To manage the self-destruction of objects with the auto-destroy class
def auto_destroy_js(segundos: int = 3):
    """Destruye todos los elementos coon la clase auto-destroy """
    js = """
    const elements = document.querySelectorAll('.auto-destroy');
    elements.forEach(element => {
        setTimeout(() => {
            element.style.opacity = '0'; // Desvanece el elemento
            setTimeout(() => {
                element.remove(); // Elimina el elemento después de que se haya desvanecido
            }, 1000); // Espera 1 segundo (duración de la transición) antes de eliminar
        }, 5000); // Espera 5 segundos antes de iniciar el desvanecimiento
    });
    """.replace("5000", str(segundos*1000))
    return Script(js)