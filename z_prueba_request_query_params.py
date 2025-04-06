from urllib.parse import unquote_plus
from fasthtml.common import * 

app, rt = fast_app(
    hdrs=(
        picolink,
        Style(':root { --pico-font-size: 100%; }'),
    )
)


search_input=Input(
    id="q",
    placehorder="Buscar...",
    type="search",
    hx_get="/buscar",
    hx_trigger="input changed delay:500ms, keyup[key=='Enter'], load",
    hx_target="#resultados",
)





@rt('/')
async def index(request):
    return \
    Div(
        H1("Hello World!"),
        Hr(),
        search_input(),
        Div(id="resultados")("Resultados de la búsqueda..."),
    )

@rt('/buscar')
async def buscar(request):
    q = request.query_params.get("q", "")
    q_decodificado = unquote_plus(q)
    if not q:
        return "No hay resultados"
    else:
        return f"Resultados para: {q} y request.query_params: {q_decodificado}"


serve()