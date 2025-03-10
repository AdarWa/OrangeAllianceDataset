# Orange Alliance Dataset

Welcome to the Orange Alliance Dataset repository. This dataset was created by scraping the Orange Alliance API, which is a website that contains data about the FTC([FIRST Tech Challenge](https://www.firstinspires.org/robotics/ftc)) teams.

## Dataset Columns
To understand the datset, a basic understanding of the FTC(FIRST Tech Challenge) game of 2024-2025(Into The Deep) is needed.

A link to a 5 minute animation video of the game - [Link](https://www.youtube.com/watch?v=ewlDPvRK4U4)

**Note**: This dataset contains infomation about **teams** and <ins>not</ins> games.

This dataset contains the following columns of data:

### General Team Information

#### <ins>number</ins>
Every team has a unique number that identifies them in the FIRST system.

#### <ins>name</ins>
Every team has a name.
A name might not be unique to a team, and other teams can use the same name.

#### <ins>rookie_year</ins>
The year that the team was established.
A "rookie team" is a team that this season is it's first season.

#### <ins>country</ins>
The country that the team is from.

#### <ins>has_website</ins>
Some teams might have a website. if the teams has a website, this will be TRUE, otherwise, it will be FALSE.

### Team Performance
**Note:** A game consists of two robots, and the score is counted for the two robots combined, later, we can predict the score of only one robot. 

#### <ins>auto_park</ins>
A column that describe the status of the park during the autonomous period of each game the team has played.
An example of the `auto_park` can be:

`True,False,False,True,True,False,True,True,True,False,False,False,True,False,True,True,True,False,False`

In this example in the first game of the team it parked, in the second game it didn't and so on.

#### <ins>tele_ascent</ins>
Describes the ascent status of the robot at the end of TeleOp period.
This is per robot and not per alliance.

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

