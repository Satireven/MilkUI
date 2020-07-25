import bottle
import logging
import json
from threading import Thread
from .utils import find_free_port, call_after
from .api import *
from bottle import request, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.logging import create_logger

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
                    # print(msg)
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
        # websocket
        # @server.post('/milk/dialog/info')
        # def info_dialog():
        #     AppHelper.callAfter(app.openFileDialog) # fix not main thread calling error
        
        # @server.post('/milk/dialog/question')
        # def question_dialog():
        #     AppHelper.callAfter(app.openFileDialog)

        # @server.post('/milk/dialog/confirm')
        # def confirm_dialog():
        #     AppHelper.callAfter(app.openFileDialog)
        
        # @server.post('/milk/dialog/error')
        # def error_dialog():
        #     AppHelper.callAfter(app.openFileDialog)
        
        # @server.post('/milk/dialog/stack_trace')
        # def stack_trace_dialog():
        #     AppHelper.callAfter(app.openFileDialog)
        
        # @server.post('/milk/dialog/open_file')
        # def open_file_dialog():
        #     AppHelper.callAfter(app.openFileDialog)
        
        # @server.post('/milk/dialog/save_file')
        # def save_file_dialog():
        #     AppHelper.callAfter(app.openFileDialog)
        
        # @server.post('/milk/dialog/select_folder')
        # def select_folder_dialog():
        #     AppHelper.callAfter(app.openFileDialog)

    def _serve_wsgi(self, host, port, app, quiet=False):
        server = WSGIServer((host, port), app, handler_class=WebSocketHandler)
        if not quiet:
            server.logger = create_logger('geventwebsocket.logging')
            server.logger.setLevel(logging.INFO)
            server.logger.addHandler(logging.StreamHandler())
        server.logger.info(f'Listening on http://{host}:{port}/\nHit Ctrl-C to quit.\n')
        server.serve_forever()
    
    def _load_server(self):
        Thread(target=self._serve_wsgi, kwargs={'host':'127.0.0.1', 'port':self.port, 'app':self.server, 'quiet':False}, daemon=True).start()
    
    def run(self):
        self._load_app()
        self._load_api()
        self._load_server()
        self.app.main_loop()