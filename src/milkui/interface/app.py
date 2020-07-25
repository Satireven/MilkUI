import toga
import milkui.resources
from os import path

STATIC_FOLDER = path.dirname(milkui.resources.__file__)

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

    def invoke_js(self, sender):
        """
            invoke javascript for communication
        """
        with open(path.join(STATIC_FOLDER, 'invoke.js')) as f:
            js = f.read().replace('{MilkAppPort}', str(self.port)).replace('{MilkAppToken}', self.token)
        self.webview.invoke_javascript(js)
    
    def on_key_down(self, *args, **kwargs):
        """
            key down event for shortcut
        """
        pass

    def on_mount(self):
        """
            start call function
        """
        pass

    def on_destroy(self):
        """
            exit call function
        """
        pass

    def set_menu_bar(self, menu):
        groups = {
            'App': toga.Group.APP,
            'File': toga.Group.FILE,
            'Edit': toga.Group.EDIT,
            'View': toga.Group.VIEW,
            'Commands': toga.Group.COMMANDS,
            'Window': toga.Group.WINDOW,
            'Help': toga.Group.HELP
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

    def startup(self):
        self.webview = WebView(style=toga.style.Pack(flex=1))
        self.webview.url = f"http://localhost:{self.port}/"
        self.webview.on_key_down = self.on_key_down
        self.webview.on_webview_load = self.invoke_js

        self.main_window = toga.Window()
        self.main_window.content = self.webview
        self.on_mount()
        self.main_window.show()
    