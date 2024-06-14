from sanic import Sanic, response

app = Sanic(__name__)
cache = {}

@app.route('/')
async def index(request):
    # Limpar o cache aqui
    cache.clear()
    return response.text('Cache cleared!')

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=8000)
