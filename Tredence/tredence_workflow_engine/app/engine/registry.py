class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, fn):
        self.tools[name] = fn

    def get(self, name: str):
        return self.tools.get(name)

registry = ToolRegistry()
