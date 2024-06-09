import csv
from telemetry.adapter.data_adapter import DataAdapter

class CSVDataAdapter(DataAdapter):
    def convert(self, data):
        # Implement conversion to CSV here
        output = []
        for row in data:
            output.append(','.join(map(str, row)))
        return '\n'.join(output)
