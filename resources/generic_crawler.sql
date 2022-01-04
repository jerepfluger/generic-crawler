create database generic_crawler;

create table if not exists generic_crawler.instagram_crawling(
    id int auto_increment primary key,
    draw varchar(20),
    account_draw varchar(20),
    tagging_count varchar(7),
    tagging_percentage decimal(3,2),
    tags_needed int,
    followed bool,
    liked bool
);
