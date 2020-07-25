"""
bottle single page application example app
"""
from milk.interface.app import Milk

class HelloWorld(Milk):
    def __init__(self, *args, **kwargs):
        Milk.__init__(self, *args, **kwargs)

    def on_mount(self):
        self.menu = [
            {
                'label': 'App',
                'children': [
                    {
                        'type': 'menu_item',
                        'label': 'Test',
                        'shortcut': 't',
                        'callback': lambda sender: self.webview.dispatch('menuClicked')
                    }
                ]
            },
            {
                'label': 'File',
                'children': [
                    {
                        'type': 'menu_item',
                        'label': 'New File',
                        'shortcut': 'n',
                        # 'enabled': False,
                        'callback': lambda sender: self.openFileDialog()
                    },
                    {
                        'type': 'menu_separator'
                    },
                    {
                        'type': 'menu_item',
                        'label': 'New Window',
                        'shortcut': 'N',
                        'callback': lambda sender: print(123)
                    },
                    {
                        'type': 'menu_item',
                        'label': 'Test2',
                        'shortcut': 'c',
                        'callback': lambda sender: print(123)
                    },
                    {
                        'type': 'menu_separator'
                    },
                    {
                        'type': 'menu_item',
                        'label': 'Test3',
                        'shortcut': 'd',
                        'callback': lambda sender: print(123)
                    },
                ]
            }
        ]
        self.set_menu_bar(self.menu)
        self.main_window.size = (1200, 800)
        self.main_window.title = 'Hello World'

    def on_destroy(self):
        print('exit')



