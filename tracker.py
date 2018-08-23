import praw
import config

MESSAGE_TEMPLATE = 'MangaTrackerBot found a new chapter \n {title} \n {link}'


def main():
    stream, redditor, reddit = setup()
    process_stream(stream, redditor)


def setup():
    reddit = praw.Reddit(client_id=config.CLIENT_ID,
                         client_secret=config.CLIENT_SECRET,
                         password=config.PASSWORD,
                         user_agent=config.USER_AGENT,
                         username= config.USERNAME)

    subreddit = reddit.subreddit('manga')
    redditor = reddit.redditor(config.REDDITOR)
    stream = subreddit.stream.submissions()
    for submission in stream:
        process_stream(submission, redditor)


def process_stream(submission, redditor):
        title = submission.title

        if 'DISC' not in title.upper():
            return

        manga = config.MANGA_LIST
        hype_title = title.upper()

        for manga_title in manga:
            if manga_title in hype_title:
                send_alert(submission, redditor)


def send_alert(submission, redditor):
    redditor.message('MangaTrackerBot Alert',
                     MESSAGE_TEMPLATE.format(title=submission.title, link=submission.shortlink))


if __name__ == '__main__':
    main()
