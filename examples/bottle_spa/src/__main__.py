from milkui.interface.process import Process
from .app import HelloWorld
from .server import app
# import api


if __name__ == '__main__':
    Process(app=HelloWorld, server=app, api=None).run()
