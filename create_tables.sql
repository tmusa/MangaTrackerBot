create table Manga(
    ID integer,
    Title text not null,
    primary key(ID)
);


create table Subscription(
    MangaID integer,
    Redditor text,
    primary key (MangaID, Redditor)
);