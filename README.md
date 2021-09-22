# switchtimer

A Nintendo Switch inspired parental controls laptop timer.

## What's this about?

When we got our son a laptop, my wife and I decided two things up front:

1. Screen time would be limited
2. It would run Ubuntu

Initially, I was looking into Gnome Nanny, but it turns out that was last updated
in 2011, and was no longer supported.

When it comes to parental controls, my philosophy is boundaries and trust.  I
felt that the Nintendo Switch implemented this perfectly with its fair, flexible
timer system.  This is what it does:

* You (the parent) set an allowed amount of play time, per date
* The switch records play time every day
* Warning notifications are shown when you have 1 hour, 30 minutes, and 5 minutes left
* When time is up, a persistent notification is shown

This encourages awareness of time and time management, and doesn't actually boot
you from the system - you can finish that last lap of the race once time is up
if you need to.

I know every kid's different, but this worked well for our son, too - he was often
logging off for the day between the 5 minute warning and the actual time limit,
I assume when he was done what he was doing.

I wanted to bring this same flexibility and sense of autonomy over to his laptop,
so here it is - the switchtimer.

## How To Install

Right now, this is kinda rough.  I'm working on it.

Short version: 

* Clone this repo
* `pip install -r requirements.txt`
* `ln -s /path/to/switchtimer/bin/notify-user.sh /usr/local/bin/notify-user`
* Update switchtimer.service to point to the path you cloned the repo to
* `cp switchtimer.service /etc/systemd/system/`
* `systemctl daemon-reload && systemctl enable switchtimer && systemctl start switchtimer`

This code also has "pat" hardcoded all over; that should be the monitored account's
username.

Again, work in progress.

## How It Works

The `bin/notify-user.sh` script handles all the scaffolding necessary to issue
D-BUS notifications to named, logged in users as root (it's not as easy as you
might hope).  This actually uses `notify-send.py` behind the scenes because, for
whatever reason, `notify-send` doesn't have a `-r` (replace) option.

The switchtimer module is a python program that runs forever, mostly sleeping
but waking up once a minute to see who's logged in using `loginctl`.   If a monitored
user is logged in, they are counted as having been on the machine for one minute.
This should more or less even out, even if it's not precise.

If a user is found to be within a notification threshold, python shells out to
`notify-user` to deliver the notification; notifications are low-urgency for
normal warnings, and critical when time is up.  Critical notifications are
persistent until dismissed, while low-urgency notifications dismiss themselves.

We need to replace notifications to allow them to behave as we want: namely, my
son plays a lot of video games (Steam on Linux is great these days), and they're
always full screened - low-urgency notifications won't show up normally.  However,
it's really lousy to have to pause the game to dismiss a critical notification,
especially if it's only a "one hour left" warning.  Good thing there's a trick:
if you show a critical notification, then immediately replace it with a low-urgency
notification with the same subject and message, the system will show it even over
full screen applications (since it's initially critical), but will then dismiss
it automatically after a few seconds when it becomes low-urgency.  It was a long
and winding road to land on this solution, and it NotifyOSD implemented expiry
it wouldn't've been a problem at all, but that's all behind us now.

## Privacy, etc

This doesn't send data anywhere; everything's stored in `/var/switchtimer`.
You can read the files in there to see how long monitored accounts have been
logged in every day, too.
