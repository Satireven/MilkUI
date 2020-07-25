import os
import toga
from toga import Group
from toga.style import Pack
import bottle
import json


STATIC_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')

class WebView(toga.WebView):
    def __init__(self, *args, **kwargs):
        super(WebView, self).__init__(self, *args, **kwargs)
    
    def dispatch(self, event_id):
        self.invoke_javascript("document.dispatchEvent(new CustomEvent('milkJavaScriptEvent', {detail: {id: '%s'} }));" % (event_id))


class Milk(toga.App):
    def __init__(self, port, title=None):
        toga.App.__init__(self)
        self.port = port
        self.token = '32323'
        self.title = title if title else self.formal_name
        self.on_exit = lambda _: self.on_destroy()
        
        # toga.MainWindow()
        # self.window2 = toga.Window()
        # self.window2.show()
        # self.window2.hidden = True
        # self.main_window2.content = self.webview
        # self.main_window2.show()
    


    def invoke_js(self, sender):
        """
            invoke javascript for communication
        """
        with open(os.path.join(STATIC_FOLDER, 'axios.min.js')) as f1, open(os.path.join(STATIC_FOLDER, 'invoke.js')) as f2:
            js = '\n'.join([f1.read(), f2.read().replace('{MilkAppPort}', str(self.port)).replace('{MilkAppToken}', self.token)])
            print(self.port)
        self.webview.invoke_javascript(js)

    def openFileDialog(self):
        try:
            fname = self.main_window.open_file_dialog(
                title="Open file with Toga",
                multiselect=False
            )
            if fname is not None:
                print( "File to open:" + fname)
            else:
                print("No file selected!")
        except ValueError:
            print("Open file dialog was canceled")
    
    
    def watchEvent(self, *args, **kwargs):
        print(args, kwargs)
        self.openFileDialog()

    def set_menu_bar(self, menu):
        groups = {
            'App': Group.APP,
            'File': Group.FILE,
            'Edit': Group.EDIT,
            'View': Group.VIEW,
            'Commands': Group.COMMANDS,
            'Window': Group.WINDOW,
            'Help': Group.HELP
        }
        for item in menu:
            section = 0
            try:
                group = groups[item['label']]
            except KeyError:
                group = toga.Group(item['label'])
            for child in item['children']:
                if child['type'] == 'menu_separator':
                    section += 1
                    continue
                command = toga.Command(
                    child['callback'],
                    label = child['label'],
                    shortcut = child['shortcut'],
                    section = section,
                    group = group,
                )
                if 'enabled' in child: command.enabled = child['enabled']
                self.commands.add(command)

    def set_tray_icon(self, icon, menu):
        pass

    def on_mount(self):
        pass

    def on_destroy(self):
        pass

    def startup(self):
        self.webview = WebView(style=Pack(flex=1))
        self.webview.url = f"http://localhost:{self.port}/"
        self.webview.on_key_down = self.watchEvent
        self.webview.on_webview_load = self.invoke_js

        self.main_window = toga.Window()
        self.main_window.content = self.webview
        # self.button = toga.Button('Save File', on_press=self.openFileDialog)
        self.on_mount()
        # self.add_background_task
        self.main_window.show()
        # self.openFileDialog()
        # self.webview.url = f"http://localhost:{self.port}/"
        # self.add_background_task(self.waitEvent)
    