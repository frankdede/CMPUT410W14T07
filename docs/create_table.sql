DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS circle;
DROP TABLE IF EXISTS author;
DROP TABLE IF EXISTS servers;

CREATE TABLE servers(
sid int,
servers_name varchar(128) NOT NULL,
url varchar(128) NOT NULL,
PRIMARY KEY (sid)
);

CREATE TABLE author(
aid varchar(128) NOT NULL UNIQUE,
author_name varchar(128) NOT NULL UNIQUE,
pwd varchar(128) NOT NULL,
sid int default 1,
nick_name varchar(128),
PRIMARY KEY (aid, sid),
FOREIGN KEY (sid) REFERENCES servers (sid)
);

CREATE TABLE post(
pid varchar(128) NOT NULL,
aid varchar(128),
dates date NOT NULL,
title varchar(128) NOT NULL,
message varchar(1024),
type enum('html','txt','markdown') NOT NULL,
permission enum('me', 'user', 'friends', 'friends of friends', 'friends on my host', 'public') NOT NULL,
PRIMARY KEY (pid),
FOREIGN KEY (aid) REFERENCES author (aid)
);

CREATE TABLE circle(
name1 varchar(128),
name2 varchar(128),
sid int,
PRIMARY KEY (name1, name2, sid),
FOREIGN KEY (name1) REFERENCES author (author_name),
FOREIGN KEY (name2) REFERENCES author (author_name),
FOREIGN KEY (sid) REFERENCES servers (sid)
);
INSERT INTO servers values(1,'localhost','localhost')
