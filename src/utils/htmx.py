# Functions and utilities related to HTMX

def is_hx_request(req):
    """ Check if the request is from HTMX """
    return True if req.headers.get("HX-Request") else False