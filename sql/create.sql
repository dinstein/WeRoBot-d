create database if not exists mrobot;
use mrobot;
create table if not exists talk
(
    id int primary key auto_increment,
    match_count int  NOT NULL,
    Q varchar(500)   NOT NULL,
    A varchar(500)   NOT NULL
);

CREATE INDEX talkQues ON talk(Q(200));

CREATE TABLE if not exists talk_e LIKE talk;
