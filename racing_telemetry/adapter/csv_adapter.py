import csv
from .adapter import Adapter

class CSVAdapter(Adapter):
    def convert(self, data):
        # Implement conversion to CSV here
        output = []
        for row in data:
            output.append(','.join(map(str, row)))
        return '\n'.join(output)
