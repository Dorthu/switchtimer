from datetime import date
from time import sleep
import logging

from switchtimer.util import send_notification, user_is_active, date_string
from switchtimer.data import load_data, save_data, default_entry


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# used to handle day rollover
last_run_date = None
data = None

FILE_PATH = "/etc/switchtimer/data"


def main_loop():
    """
    Runs forever, recording how many minutes active and notifying
    """
    global last_run_date
    while True:
        logger.debug("Checking user status..")

        cur_run = date.today()
        cur_run_str = date_string(cur_run)

        if cur_run != last_run_date:
            logger.info("It's a brand new day!")
            data['pat'][cur_run_str] = default_entry()
            last_run_date = cur_run

        cur_data = data['pat'][cur_run_str]

        if user_is_active('pat'):
            logger.debug("pat is active")
            cur_data["minutes_active"] += 1

        logger.debug(f"{cur_data}")

        if cur_data["minutes_active"] >= 60 and not cur_data["notify_1"]:
            cur_data["notify_1"] = True
            send_notification("One hour left!")

        if cur_data["minutes_active"] >= 110 and not cur_data["notify_2"]:
            cur_data["notify_2"] = True
            send_notification("Ten minutes left!")

        if cur_data["minutes_active"] >= 115 and not cur_data["notify_3"]:
            cur_data["notify_3"] = True
            send_notification("Five minutes left!")

        if cur_data["minutes_active"] >= 120 and not cur_data["notify_4"]:
            cur_data["notify_4"] = True
            send_notification("Time is up!", icon="clock", urgency="critical")

        save_data(FILE_PATH, data)
        sleep(60)



if __name__ == "__main__":
    last_run_date = date.today()
    data = load_data(FILE_PATH)

    if 'pat' not in data:
        data['pat'] = {}

    if date_string(last_run_date) not in data['pat']:
        data['pat'][date_string(last_run_date)] = default_entry()

    main_loop()
