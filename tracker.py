import praw
import config
import MangaTrackerDBOPS as db

MESSAGE_TEMPLATE = 'MangaTrackerBot found a new chapter \n {title} \n {link}'


def main():
    stream, redditor, reddit = setup()
    for submission in stream:
        process_stream(submission, reddit)


def setup():
    # print(config.MANGA_LIST)
    db.main()
    # print(config.MANGA_LIST)

    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         password=config.PASSWORD,
                         user_agent=config.USER_AGENT,
                         username=config.USERNAME)

    subreddit = reddit.subreddit('manga')
    redditor = reddit.redditor(config.REDDITOR)
    stream = subreddit.stream.submissions()
    return stream, redditor, reddit


def process_stream(submission, reddit):
        title = submission.title

        if 'DISC' not in title.upper():
            return

        title = title.upper()
        print(title)
        for manga in db.all_manga():
            if manga in title:
                send_alert(submission, reddit.redditor(config.REDDITOR))
                print("alert {}".format(title))
                # title = manga
                continue

        # subscribers = db.find_subscribers(title)
        # print(subscribers)
        # for redditor in subscribers:
        #     send_alert(submission, reddit.redditor(redditor))
        #     print("alert {}".format(title))
        # for m in manga:
        #     manga_title = m.title
        #     if manga_title in hype_title:
        #         send_alert(submission, redditor)
        #         # print("alert {}".format(manga_title))


def send_alert(submission, redditor):
    msg = MESSAGE_TEMPLATE.format(title=submission.title, link=submission.shortlink)
    redditor.message('MangaTrackerBot Alert', msg)
    # print(msg)


if __name__ == '__main__':
    main()
