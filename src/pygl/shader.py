class Shader:
    def __init__(self, shader_file: str) -> None:
        self.file = shader_file
        self.data = None

    def load(self):
        if self.data is None:
            with open(self.file, 'r') as f:
                self.data = f.read().strip()

        return self.data
        