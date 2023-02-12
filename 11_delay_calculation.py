import pandas as pd
import numpy as np

data = {'Planned': ['22:50', '23:50', '23:50', '00:30', '20:50'],
        'Estimated': ['23:50', '00:30', '21:00', '22:50', '23:50']}

df = pd.DataFrame(data)

df['Planned'] = pd.to_datetime(df['Planned'], format='%H:%M')
df['Estimated'] = pd.to_datetime(df['Estimated'], format='%H:%M')
df['Estimated'] = np.where(df['Estimated'] < df['Planned'], df['Estimated'] + pd.Timedelta(days=1), df['Estimated'])
df['Delay'] = ((df['Estimated'] - df['Planned']).dt.total_seconds().astype(int)) / 60

print(df)
