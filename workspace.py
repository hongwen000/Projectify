import os

class Workspace:
    def __init__(self, root):
        self.root = root

    def get_project_paths(self):
        return [os.path.join(self.root, name) for name in os.listdir(self.root) if os.path.isdir(os.path.join(self.root, name))]
