from milkui.interface.process import Process
from .app import BottleSinglePageApplication
from .server import app

if __name__ == '__main__':
    Process(app=BottleSinglePageApplication, server=app, api=None).run()