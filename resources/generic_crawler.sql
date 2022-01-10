create schema generic_crawler;

create table if not exists generic_crawler.instagram_draws(
    id int auto_increment primary key,
    draw_url varchar(20),
    draw_account varchar(25),
    needs_tagging bool,
    tags_needed smallint,
    needs_message bool,
    message varchar(50),
    needs_post_story bool default false,
    needs_like bool default true,
    needs_follow bool default true,
    accounts_to_follow text,
    expiry_date timestamp,
    expired bool default false,
    won bool,
    extra_info text
);

create table if not exists generic_crawler.instagram_tagging_accounts(
    id int auto_increment primary key,
    group_id smallint not null,
    account varchar(25) not null,
    last_used timestamp not null
);

create table if not exists generic_crawler.instagram_spider_accounts(
    id smallint auto_increment primary key,
    username varchar(15) not null,
    password varchar(15) not null,
    email varchar(30) not null,
    last_used timestamp not null,
    is_banned bool default false
);

create table if not exists generic_crawler.instagram_crawling(
    id int auto_increment primary key,
    crawling_timestamp timestamp default current_timestamp,
    spider_account_id smallint,
    draw_id int,
    tagging_group_id smallint,
    tagging_count varchar(7),
    tagging_percentage decimal(5,2),
    tags_needed int,
    followed bool,
    liked bool,
    foreign key (spider_account_id) references generic_crawler.instagram_spider_accounts(id),
    foreign key (draw_id) references generic_crawler.instagram_draws(id),
    foreign key (tagging_group_id) references generic_crawler.instagram_tagging_accounts(group_id)
);

INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (1, 'jeritisfluffy', 'J3r3mia$123', 'jerepfluger@outlook.com', '2022-01-07 15:24:03', 1);
INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (2, 'jeritisflufy', 'J3r3mia$123', 'jerepfluger@hotmail.com', '2022-01-07 15:24:03', 0);
INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (3, 'jeritis_flufy', 'J3r3mia$123', 'instacrawl_1@hotmail.com', '2022-01-07 15:24:03', 0);
INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (4, 'jeritis_fluffy', 'J3r3mia$123', 'jeritis_fluffy@hotmail.com', '2022-01-07 15:24:03', 0);
INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (5, 'fluffyjeritis', 'J3r3mia$123', 'fluffyjeritis@hotmail.com', '2022-01-07 15:24:03', 0);
INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (6, 'flufyjeritis', 'J3r3mia$123', 'flufyjeritis@hotmail.com', '2022-01-07 15:24:03', 0);
INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (7, 'fluffy_jeritis', 'J3r3mia$123', 'fluffy_jeritis@hotmail.com', '2022-01-07 15:24:03', 0);
INSERT INTO generic_crawler.instagram_spider_accounts (id, username, password, email, last_used, is_banned) VALUES (8, 'flufy_jeritis', 'J3r3mia$123', 'flufy_jeritis@hotmail.com', '2022-01-07 15:24:03', 0);

INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (3, '/p/CYJj9tzLZU2/', 'telefecordoba', 1, 3, 0, '', 0, 1, 1, '2022-01-01 18:00:00', 1, 0, null);
INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (2, '/p/CYHC-etM9gy/', '@ferniplast', 1, 1, 0, '', 0, 1, 1, '2022-01-03 18:00:00', 1, 0, null);
INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (1, '/p/CYDAro9s6Wv/', '@clin.oficial', 1, 3, 0, '', 0, 1, 1, '2022-01-04 19:00:00', 1, 0, null);
INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (5, '/p/CYT4_AbLkqM/', '@maampasteleria', 1, 1, 1, 'yomi yomi! quiero!!', 0, 1, 1, '2022-01-05 18:00:00', 1, 0, null);
INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (8, '/p/CYHJ96MlzkY/', '@megatone.ar', 1, 1, 0, '', 1, 1, 1, '2022-01-05 18:00:00', 1, 0, 'follow also @samsungarg');
INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (6, '/p/CYUMKjLgh2z/', '@olmobikes', 1, 2, 0, '', 0, 1, 1, '2022-01-06 18:00:00', 1, 0, 'need to follow also @grisino.oficial');
INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (7, '/p/CYAQSnXLt0E/', '@valeria.caliva.paintings', 1, 1, 0, '', 1, 1, 1, '2022-01-07 18:00:00', 1, 0, 'need to follow also @filgoargentina');
INSERT INTO generic_crawler.instagram_draws (id, draw_url, draw_account, needs_tagging, tags_needed, needs_message, message, needs_post_story, needs_follow, needs_like, expiry_date, expired, won, extra_info) VALUES (4, '/p/CYRO4wNLXDX/', '@chocolinasok', 1, 3, 1, 'cada paisaje de mis viajes', 0, 1, 1, '2022-01-10 23:59:59', 0, 0, 'need to follow also @fujifilmargentinainstax');

INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (1, 1, '@la.birraa', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (2, 2, '@capturebizarre', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (3, 3, '@c5n', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (4, 4, '@cronicatv', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (5, 4, '@shell_argentina', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (6, 4, '@eltrecetv', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (7, 4, '@telefe', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (8, 4, '@telefecordoba', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (9, 4, '@gambaonline', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (10, 4, '@mia_malkova', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (11, 4, '@100argentinosdicen', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (12, 4, '@masterchefargentina', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (13, 4, '@axion_energy_oficial', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (14, 5, '@aireuropa', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (15, 5, '@aerolineas_argentinas', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (16, 5, '@claroargentina', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (17, 5, '@clarincom', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (18, 5, '@aerolineas_argentinas', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (19, 5, '@jetsmart_argentina', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (20, 5, '@flybondioficial', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (21, 5, '@despegar.ar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (22, 5, '@despegar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (23, 5, '@americanair', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (24, 6, '@latamairlines', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (25, 6, '@afaseleccion', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (26, 6, '@fifaworldcup', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (27, 6, '@turkishairlines', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (28, 6, '@qatarairways', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (29, 6, '@skyteamalliance', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (30, 6, '@skyairline', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (31, 6, '@copaairlines', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (32, 6, '@nuevocentro_shopping', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (33, 6, '@patioolmosshopping', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (34, 7, '@paseodeljockey', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (35, 7, '@cordobashopping', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (36, 7, '@jeffbezos', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (37, 7, '@spidermanmovie', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (38, 7, '@zuck', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (39, 7, '@meta', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (40, 7, '@facebookapp', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (41, 7, '@instagram', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (42, 7, '@instagramforbusiness', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (43, 7, '@twitter', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (44, 8, '@whatsapp', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (45, 8, '@dell', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (46, 8, '@apple', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (47, 8, '@maccosmeticsarg', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (48, 8, '@victoriassecret', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (49, 8, '@camilo', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (50, 8, '@balenciaga', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (51, 8, '@gucci', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (52, 8, '@prada', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (53, 8, '@givenchyofficial', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (54, 9, '@ralphlauren', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (55, 9, '@lacoste', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (56, 9, '@brunomars', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (57, 9, '@madonna', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (58, 9, '@britneyspears', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (59, 9, '@nsync', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (60, 9, '@hm', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (61, 9, '@zara', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (62, 9, '@bershka', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (63, 9, '@pullandbear', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (64, 10, '@discoveryhh', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (65, 10, '@disney', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (66, 10, '@disneyplusla', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (67, 10, '@waltdisneyworld', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (68, 10, '@universaltvla', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (69, 10, '@universalpicturesarg', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (70, 10, '@universalorlando', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (71, 10, '@starplusla', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (72, 10, '@todonoticias', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (73, 10, '@tntlatam', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (74, 11, '@tntsportsbr', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (75, 11, '@starchannellatam', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (76, 11, '@wanda_nara', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (77, 11, '@mauroicardi', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (78, 11, '@samsungarg', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (79, 11, '@xiaomi.argentina.oficial', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (80, 11, '@personalar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (81, 11, '@nokiamobile', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (82, 11, '@motorola_ar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (83, 11, '@cristiano', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (84, 12, '@el_kilombotravel', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (85, 12, '@kyliejenner', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (86, 12, '@natgeo', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (87, 12, '@nike', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (88, 12, '@mileycyrus', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (89, 12, '@adidas', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (90, 12, '@adidasar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (91, 12, '@adidasoriginals', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (92, 12, '@adidasfootball', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (93, 12, '@adidaswomen', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (94, 13, '@nikesportswear', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (95, 13, '@nikefootball', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (96, 13, '@puma', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (97, 13, '@pumaargentina', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (98, 13, '@pumaindia', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (99, 13, '@pumawomen', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (100, 13, '@uniqlo', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (101, 13, '@uniqlousa', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (102, 13, '@topper_argentina', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (103, 13, '@underarmour', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (104, 14, '@underarmourlatam', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (105, 14, '@underarmourwomen', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (106, 14, '@underarmourbrasil', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (107, 14, '@villavicencio', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (108, 14, '@philipsaventar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (109, 14, '@philipsarg', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (110, 14, '@philips', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (111, 14, '@philipshogar.ar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (112, 14, '@sony', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (113, 14, '@sonypictures', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (114, 15, '@sonypicturesarg', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (115, 15, '@sonymusicargentina', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (116, 15, '@lg_uk', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (117, 15, '@lgelectronicsca', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (118, 15, '@panasoniclatino', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (119, 15, '@panasonic', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (120, 15, '@samsung', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (121, 15, '@philco.arg', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (122, 15, '@jeritisfluffy', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (123, 15, '@seagate', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (124, 1, '@assist365ok', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (125, 1, '@ypfoficial', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (126, 1, '@santander_ar', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (127, 1, '@cheeboludo', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (128, 1, '@muybizarra', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (129, 1, '@novalezapegato', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (130, 1, '@marizzadenoche', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (131, 1, '@firucheto', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (133, 2, '@indirectas.arg', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (134, 2, '@losmemesdicen', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (135, 2, '@soybigote', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (136, 2, '@laprevia.ok', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (137, 2, '@soyargentinoh', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (138, 2, '@la100fm', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (139, 2, '@infobae', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (140, 2, '@argentovich', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (142, 3, '@marley_ok', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (143, 3, '@el_kilombo', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (144, 3, '@8fact', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (145, 3, '@willsmith', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (146, 3, '@9gag', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (147, 3, '@cabronazi', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (148, 3, '@justinbieber', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (149, 3, '@pachu_pena', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (150, 3, '@cadena3com', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (151, 1, '@vodafoneit', '0000-00-00 00:00:00');
INSERT INTO generic_crawler.instagram_tagging_accounts (id, group_id, account, last_used) VALUES (152, 2, '@tucumanobasico1', '0000-00-00 00:00:00');