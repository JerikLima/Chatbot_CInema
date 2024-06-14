from sanic import Sanic
from sanic.response import json

# Configuração personalizada
app = Sanic("MyApp")
app.config.REQUEST_MAX_SIZE = 1000 * 1024 * 1024  # 500 MB
app.config.REQUEST_BUFFER_SIZE = 65536  # 64 KiB
app.config.REQUEST_MAX_HEADER_SIZE = 8192  # 8 KiB

print(f"Configuração de REQUEST_MAX_SIZE: {app.config.REQUEST_MAX_SIZE}")
print(f"Configuração de REQUEST_BUFFER_SIZE: {app.config.REQUEST_BUFFER_SIZE}")
print(f"Configuração de REQUEST_MAX_HEADER_SIZE: {app.config.REQUEST_MAX_HEADER_SIZE}")

@app.route('/upload', methods=['POST'])
async def upload(request):
    return json({'status': 'received'})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
