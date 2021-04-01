import json
import pandas as pd

from csv_reader import csv_to_dictlist
    
count_dict = csv_to_dictlist()
df = pd.DataFrame(count_dict)

df.to_json(r'./data/deDomiciled.json')
