import subprocess
from datetime import datetime, date
import time
import re
from logging import getLogger

logger = getLogger(__name__)


LOGINCTL_SESSION_ID_REGEX = r' *(\d+) '


def date_string(d: date) -> str:
    """
    Formats a datetime.date in a consistent manner
    """
    return f"{d.year}-{d.month}-{d.day}"


def send_notification(message: str, icon: str = "timer"):
    """
    Sends a notification using the `notify-send` shell command
    """
    logger.debug(f"Sending notification: {message}")

    # TODO: Abstract this out a little
    res = subprocess.run(["notify-user", "pat", "Laptop Timer", message, "-i", icon])

    if res.returncode:
        logger.warning(f"notify-send exited with status {res.returncode}")



def user_is_active(user: str) -> bool:
    """
    Looks up if the named user has an active seesion using the `loginctl` shell command
    """
    # find the session id
    active_sessions_res = subprocess.run([
        "loginctl", "list-sessions",
    ], capture_output=True)

    if active_sessions_res.returncode:
        logger.warning(
            f"loginctl list-sessions exited with return code {active_sessions_res.returncode}"
        )
        return False

    session_id = None
    active_sessions = active_sessions_res.stdout.decode()
    for line in active_sessions.split('\n'):
        if user in line:
            if match := re.match(LOGINCTL_SESSION_ID_REGEX, line):
                session_id = match.groups()[0]
                break

    if not session_id:
        logger.debug(f"user {user} has no sessions")
        return False

    # now find if they're active 
    session_active_res = subprocess.run([
         "loginctl", "show-session", session_id, "-p", "Active"
    ], capture_output=True)

    if session_active_res.returncode:
        logger.warning(
             f"loginctl show-session exited with return code {session_active_res.returncode}"
        )
        return False

    session_active = session_active_res.stdout.decode().strip()
    logger.debug(f"session_active? {session_active}")

    if '=' not in session_active:
        logger.warning(
            f"Unexpected output from loginctl show-session: {session_active}"
        )
        return False
    
    return session_active.endswith("yes")


if __name__ == "__main__":
    active = user_is_active("pat")
    send_notification(f"Is pat active? {active}")
