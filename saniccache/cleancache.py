from sanic import Sanic, response

app = Sanic(__name__)

@app.route('/')
async def index(request):
    # Limpar o cache aqui
    cache.clear()
    return response.text('Cache cleared!')
