"""
Handles storing data for the switchtimer.  This includes storing data for every
monitored user for every calendar day.  Data format is:

user:
  2021-08-15:
    minutes_active: 120
    notify_1: no
    notify_2: no
    notify_3: no
    notify_4: no
  2021-08-16: 
    minutes_active: 121
"""
from os import path
import yaml


def load_data(filepath: str) -> dict:
    """
    Loads the yamls file from the given path and sends it back
    """
    if not path.isfile(filepath):
        # if it doesn't exist yet, that's fine - we'll create it
        return {}

    with open(filepath) as f:
        raw = f.read()

    if not raw:
        return {}

    return yaml.safe_load(raw)


def save_data(filepath: str, data: dict):
    """
    Writes the data out to file
    """
    with open(filepath, 'w') as f:
        f.write(yaml.dump(data))


def default_entry() -> dict:
    """
    Returns a default entry for a day
    """
    return {
        "minutes_active": 0,
        "notify_1": False,
        "notify_2": False,
        "notify_3": False,
        "notify_4": False,
    }
