class MenuItem:
    def __init__(self, label, callback=None, children=None, enabled=True):
        self.label = label
        self.enabled = enabled
        self.callback = callback
        self.children = children

class MenuSeparator:
    pass