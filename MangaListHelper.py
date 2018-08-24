import config

# This file is meant to help maintain the manga list in the config file. For
# privacy reasons the config file will be where I store anything I don't want
# to publish.


def main():
    add_titles(config.INITIAL_TITLES)
    for title in config.INITIAL_TITLES:
        subscribe(title, config.REDDITOR)


# Why is the redditor list in Manga ordered? Because every time a redditor
# subscribes to a Manga title for tracking we need to check that they don't
# already exist in the list. Otherwise we'll be sending multiple alerts.


class Manga:
    def __init__(self, title, description=None):
        self.title = title
        self.description = description
        self.redditor_list = []

    def __str__(self):
        return self.title

    def add_subscriber(self, redditor):
        self.redditor_list.append(redditor)
        self.redditor_list.sort()

    def is_subscribed(self, redditor):
        left = 0
        right = len(self.redditor_list) - 1
        while left <= right:
            middle = (left + right) >> 1

            if self.redditor_list[middle] == redditor:
                return True

            elif self.redditor_list[middle] < redditor:
                left = middle + 1

            else:
                right = middle - 1
        return False

    __repr__ = __str__

# Why is the config.MANGA_LIST sorted? Every time a new chapter is posted we
# will need to search for it through the manga list. Binary search.

# I considered storing every title both in the list and in a HashMap where
# the <key, value> pairs were titles and their index within the MANGA_LIST
# but there are two disadvantages. Hashing a string str is O(len(str)) which
# all the titles can be bounded by some integer so we'd say it's O(1).

# That would mean an O(1en(str)) HashMap lookup, then an O(1) lookup by index
# in the array. But the first disadvantages is that for every Manga object
# we'd have to store an extra integer and string. Along with that these titles
# are really long. If the average length is even something like 12 characters
# we would have to store 2^12 Manga objects in our list before hashing the
# the titles becomes faster than binary search. O(len(title)) > O(log_2(list))
# when the titles are very big.


def sort_ml():
    config.MANGA_LIST.sort(key=lambda ma: ma.title)


def find(title):
    left = 0
    right = len(config.MANGA_LIST) - 1
    title = title.upper()
    while left <= right:
        middle = (left + right) >> 1

        if config.MANGA_LIST[middle].title == title:
            return config.MANGA_LIST[middle]

        elif config.MANGA_LIST[middle].title < title:
            left = middle + 1

        else:
            right = middle - 1
    return -1


def subscribe(title, redditor):
    title = title.upper()
    manga = find(title)

    if manga == -1:
        m = Manga(title)
        m.add_subscriber(redditor)
        config.MANGA_LIST.append(m)
        sort_ml()
        return

    for person in manga.redditor_list:
        if person == redditor:
            return

    manga.add_subscriber(redditor)


def add_titles(titles):
    for title in titles:
        title = title.upper()
        if find(title) == -1:
            config.MANGA_LIST.append(Manga(title))
            sort_ml()


if __name__ == '__main__':
    main()
