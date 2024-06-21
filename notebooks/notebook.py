#!/usr/bin/env python
from init import *

t = Telemetry()
t.set_pandas_adapter()
t.set_filter({'session_id': 1718114100})
t.get_telemetry_df().head()

df = t.sessions(group_by = 'driver', limit = None)

# Remove the row with name 'Jim'
df = df[df['name'] != 'Jim']

print(df.head())

#    count    name
# 0    106   Aaron
# 1      9  Abgelo
# 2    288    Adam
# 3      9   Adnan
# 4     11    Alan

# Create a bar chart using Plotly
fig = px.bar(df, x='name', y='count', title='Session Count by Driver')
fig.update_xaxes(title='Driver Name')
fig.update_yaxes(title='Session Count')
fig.show()
