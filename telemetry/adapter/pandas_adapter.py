import pandas as pd
from .adapter import Adapter

class PandasAdapter(Adapter):
    def convert(self, data):
        # if data is a DataFrame, just return it
        if isinstance(data, pd.DataFrame):
            return data
        # Implement conversion to pandas DataFrame here
        converted_data = []
        for entry in data:
            if hasattr(entry, '__table__'):
                entry_dict = {column.name: getattr(entry, column.name) for column in entry.__table__.columns}
                converted_data.append(entry_dict)
            else:
                converted_data.append(entry)
        return pd.DataFrame(converted_data)
