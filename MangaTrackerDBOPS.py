import sqlite3
import config
import os


SUBSCRIPTION_INSERT = '''insert into Subscription 
                select m.ID , ?
                from Manga m 
                where m.Title = ?
                '''
MANGA_INSERT = 'insert into Manga (Title) values (?)'


def empty_file(file):
    try:
        return not (os.path.isfile(file) and os.path.getsize(file) > 0)
    except (FileNotFoundError, OSError):
        return True



def create_tables():
    create_qry = open('create_tables.sql', 'r').read()
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()
    c.executescript(create_qry)
    conn.commit()
    conn.close()


def drop_all():
    drop_qry = open('drop_tables.sql', 'r').read()
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()
    c.executescript(drop_qry)
    conn.commit()
    conn.close()


#   demo purposes
def init_tables():
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()

    for title in config.INITIAL_TITLES:
        title = title.upper()
        c.execute('insert into Manga(Title) values(?)', (title,))
        c.execute(SUBSCRIPTION_INSERT, (config.REDDITOR, title,))

    conn.commit()
    conn.close()


#   inserts manga title into database if it doesn't already exist
def insert_manga(title):
    title = title.upper()
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()

    c.execute('select * from Manga m where m.Title = ?', (title,))
    rows = c.fetchall()

    if len(rows) == 0:
        c.execute(MANGA_INSERT, (title,))
    else:
        conn.close()
        return

    conn.commit()
    conn.close()


def insert_subscription(title, redditor):
    title = title.upper()
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()

    # if the manga doesn't exist in our db we create it.
    c.execute('select m.ID from Manga m where m.Title = ?', (title,))
    rows = c.fetchall()

    if len(rows) == 0:
        c.execute(MANGA_INSERT, (title,))
    else:
        c.execute('select * from Subscription where Redditor = ? and MangaID = ?', (redditor, rows[0][0]))
        rows = c.fetchall()
        if len(rows) > 0:
            return
    try:
        c.execute(SUBSCRIPTION_INSERT, (redditor, title,))
    except sqlite3.IntegrityError:
        conn.close()
        return

    conn.commit()
    conn.close()


def find_subscriptions(redditor):
    subscriptions = []
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()
    sql = '''select m.Title 
            from Manga m 
            where m.ID in (
            select s.MangaID from Subscription s
            where s.Redditor = ?
            )
            '''
    c.execute(sql, (redditor,))
    rows = c.fetchall()

    for data in rows:
        subscriptions.append(data[0])

    conn.close()
    return subscriptions


def all_manga():
    manga = []
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()
    sql = '''select m.Title 
            from Manga m 
            '''
    c.execute(sql)
    rows = c.fetchall()

    for data in rows:
        manga.append(data[0])

    conn.close()
    return manga


def find_subscribers(title):
    title = title.upper()
    subscribers = []
    conn = sqlite3.connect(config.TRACKER_DB)
    c = conn.cursor()
    sql = '''select s.Redditor from Subscription s
            where s.MangaID = (
            select m.ID from Manga m
            where m.Title = ?
            )
            '''
    c.execute(sql, (title,))
    rows = c.fetchall()
    if len(rows) > 0:
        for subscriber in rows[0]:
            subscribers.append(subscriber)

    conn.close()
    return subscribers


def setup():
    if not empty_file(config.TRACKER_DB):
        drop_all()
    create_tables()
    init_tables()


def test():
    find_subscriptions(config.REDDITOR)

    for title in config.INITIAL_TITLES:
        find_subscribers(title)

    insert_subscription('ONE PIECE', 'ThrownAwayAndReborn')
    insert_manga('one piece')
    find_subscribers("nil")

def main():
    setup()
    # test()
    all_manga()

if __name__ == '__main__':
    main()
