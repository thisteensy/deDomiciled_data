import json
import pandas as pd

from csv_reader import csv_to_dictlist
    
count_dict = csv_to_dictlist()
df = pd.DataFrame(count_dict)

# result = df.to_json()
# parsed = json.loads(result)
# json.dumps(parsed, indent=4)

df.to_json(r'./data/deDomiciled.json')
