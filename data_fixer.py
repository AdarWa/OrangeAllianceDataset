import pandas as pd
import numpy as np
import logging
import api
from results import Results

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

api.init('limiter')

df = pd.read_csv('dataset.csv')
null_rows = df[df['rank'].isnull()]
for index, row in null_rows.iterrows():
    team_num = row['number']
    logging.info(f"Processing team #{team_num} at index {index}")
    try:
        results = Results(api.get_team_results(team_num))
        results_dict = results.to_dict()
    except Exception as e:
        logging.error(f"Error getting results for team #{team_num}: {str(e)}")
        results_dict = {}
    for key, value in results_dict.items():
        df.at[index, key] = value
    df.to_csv('dataset_fixed.csv', index=False)

