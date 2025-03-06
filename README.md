# Orange Alliance Dataset

Welcome to the Orange Alliance Dataset repository. This dataset was created by scraping the Orange Alliance API, which is a website that contains data about the FTC([FIRST Tech Challenge](https://www.firstinspires.org/robotics/ftc)) teams.

## Dataset

The dataset is stored as the `dataset.csv` file. To include it in your project, you can use the following code:

```python
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/AdarWa/OrangeAllianceDataset/refs/heads/main/dataset.csv')
```

## Running the script

To run the script, you can use the following commands:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

It'll ask you for the number of teams you want to process, and then it'll save the selected teams to the `selected_teams.json` file.
After that, it'll process the data for each team and save the results to the `data.csv` file.

