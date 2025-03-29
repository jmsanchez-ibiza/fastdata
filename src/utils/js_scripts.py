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