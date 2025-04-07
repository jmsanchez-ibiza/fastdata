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
def auto_destroy_js(seconds: int = 3):
    """Destroy all elements with the auto-destroy class after a specified time."""
    js = """
    const elements = document.querySelectorAll('.auto-destroy');
    elements.forEach(element => {
        setTimeout(() => {
            element.style.opacity = '0'; // Fade out the element
            setTimeout(() => {
                element.remove(); // Remove the element after it has faded out
            }, 1000); // Wait 1 second (transition duration) before removing
        }, 5000); // Wait 5 seconds before starting the fade-out
    });
    """.replace("5000", str(seconds*1000)) # Convert seconds to milliseconds and replace in the script
    return Script(js)