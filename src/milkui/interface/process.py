import json
import bottle
from threading import Thread
from geventwebsocket import WebSocketError
from .api import *
from .utils import find_free_port, call_after, serve_wsgi

class Process:
    def __init__(self, app, server, api, port=0):
        self.app = app
        self.server = server
        self.port = find_free_port() if port == 0 else port
        self.api = api

    def _load_app(self):
        self.app = self.app(port=self.port)
    
    def _extract_event(self, event, params={}, *args, **kwargs): return event, params
    
    def _load_api(self):
        # websocket
        @self.server.route('/websocket')
        def handle_websocket():
            wsock = bottle.request.environ.get('wsgi.websocket')
            if not wsock:
                bottle.abort(400, 'Expected WebSocket request.')

            while True:
                try:
                    msg = wsock.receive()
                    if msg is not None:
                        msg = json.loads(msg)
                        event, params = self._extract_event(**msg)
                        if event.startswith('app.'): params['app'] = self.app
                        if event.startswith('dialog.'): params['window'] = self.app.main_window
                        if event.startswith('api.'): params['app'], params['server'] = self.app, self.server
                        try:
                            value = call_after(eval(event), **params)
                            response = {
                                'success': True,
                                'data': value
                            }
                        except Exception as e:
                            response = {
                                'success': False,
                                'data': str(e)
                            }
                        finally:
                            response['messageId'] = msg['messageId'] # sync
                            wsock.send(json.dumps(response))
                    else: break
                except WebSocketError:
                    break
    
    def _load_server(self):
        Thread(target=serve_wsgi, kwargs={'host':'127.0.0.1', 'port':self.port, 'app':self.server, 'quiet':False}, daemon=True).start()
    
    def run(self):
        self._load_app()
        self._load_api()
        self._load_server()
        self.app.main_loop()