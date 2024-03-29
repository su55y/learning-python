import os
from pathlib import Path

DATA_HOME = Path(os.environ.get("XDG_DATA_HOME", Path.home().joinpath(".local/share")))
if not DATA_HOME.exists():
    exit("%s not found" % DATA_HOME)
DB_PATH = DATA_HOME.joinpath("newsboat/cache.db")
if not DB_PATH.exists():
    exit("%s not found" % DB_PATH)

import subprocess as sp
import sqlite3
from threading import Thread


def select_unread_count() -> int:
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM rss_item WHERE unread = 1")
            count, *_ = cur.fetchone()
            return count
    except:
        return -1


if __name__ == "__main__":
    notify = lambda msg: sp.run(["notify-send", "-a", "newsboat updates", msg])
    Thread(target=notify, args=("Start updating...",)).start()
    reload_thread = Thread(target=sp.run, args=("newsboat -x reload".split(),))
    reload_thread.start()

    before = select_unread_count()
    reload_thread.join()
    after = select_unread_count()

    if after < 0 or before < 0 or before > after:
        notify("Something went wrong: before(%s), after(%s)" % (before, after))
        exit(1)
    notify("%d new updates" % new if (new := after - before) else "No updates")
