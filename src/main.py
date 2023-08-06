from microdot_asyncio import Microdot, Response, send_file
from microdot_asyncio_websocket import with_websocket
from microdot_utemplate import render_template
from socket_manager import SocketManager
import ujson


app = Microdot()
Response.default_content_type = 'text/html'

sm = SocketManager()


@app.route('/')
async def index(request):
    return render_template("index.html")


@app.route('/chat', methods=['POST'])
async def chat(request):
    name = request.form['name']
    return render_template('chat.html', name=name)


@app.route('/ws')
@with_websocket
async def echo(request, ws):
    try:
        await sm.connect(ws)
        while True:
            data = await ws.receive()
            data_json = ujson.loads(data)
            #await sm.send_personal_message(data, ws)
            await sm.broadcast(data_json)
        
    except OSError as er:
        print("ws-error: ", er)
        await sm.disconnect(ws)


if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        pass