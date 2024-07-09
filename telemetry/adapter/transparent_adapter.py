from .adapter import Adapter

class TransparentAdapter(Adapter):
    def convert(self, data):
        return data
