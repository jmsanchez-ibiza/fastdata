# Functions and utilities related to HTMX

def es_hx_request(req):
    """ Verifica si el request es de HTMX """
    return True if req.headers.get("HX-Request") else False